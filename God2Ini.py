import os
import requests

template = """
[{itemTitle}]
itemTitle={itemTitle}
itemAuthor=by kastro <3
itemSize={itemSize}
path=Hdd1:\\Content\\0000000000000000\\{first_subfolder_encoded}\\{second_subfolder}\\{third_subfolder}\\
{part_paths}
dataurl=http://192.168.1.38/{first_subfolder_encoded}/{second_subfolder}/{third_subfolder}/{file_name}
{dataurl_parts}
"""
base_url = "http://192.168.1.38" # Change with your url

def fetch_titles_by_item_title(item_title):
    url = f"https://xboxunity.net/Resources/Lib/TitleList.php?page=0&count=10&search={item_title}&sort=3&direction=1&category=0&filter=0"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get('Items', [])

def generate_dataurl_parts(base_path, first_subfolder_encoded, second_subfolder, third_subfolder, next_subfolder, file_name):
    dataurl_parts = []
    part_paths = []

    if next_subfolder is not None:
        search_path = os.path.join(base_path, next_subfolder)
        subfolder_segment = next_subfolder
    else:
        search_path = base_path
        subfolder_segment = ''

    if os.path.isdir(search_path):
        files = [f for f in os.listdir(search_path) if os.path.isfile(os.path.join(search_path, f))]
    else:
        files = []

    for idx, _ in enumerate(files[1:], start=1):
        data_file_name = f"Data{idx:04d}"
        part_paths.append(
            f"part{idx + 1}path=Hdd1:\\Content\\0000000000000000\\{first_subfolder_encoded}\\{second_subfolder}\\{third_subfolder}\\{subfolder_segment}"
        )
        path_segments = [base_url, first_subfolder_encoded, second_subfolder, third_subfolder]
        if subfolder_segment:
            path_segments.append(subfolder_segment)
        path_segments.append(data_file_name)
        dataurl_path = "/".join(path_segments)
        dataurl_parts.append(
            f"dataurlpart{idx + 1}={dataurl_path}"
        )

    if not dataurl_parts:
        dataurl_parts.append("dataurlpart2=")

    return dataurl_parts, part_paths

def format_item_size(item_size):
    item_size_mb = item_size / (1024 * 1024)
    if item_size_mb >= 1024:
        item_size_gb = item_size_mb / 1024
        return f"{item_size_gb:.2f}GB"
    else:
        return f"{item_size_mb:.0f}MB"

def create_ini_file(base_dir, output_file):
    ini_data = {}

    for first_subfolder in os.listdir(base_dir):
        first_subfolder_path = os.path.join(base_dir, first_subfolder)
        if os.path.isdir(first_subfolder_path):

            api_items = fetch_titles_by_item_title(first_subfolder.replace(' ', '%20'))
            if api_items:
                api_item_title = api_items[0].get('Name', first_subfolder)
            else:
                api_item_title = first_subfolder

            for second_subfolder in os.listdir(first_subfolder_path):
                second_subfolder_path = os.path.join(first_subfolder_path, second_subfolder)
                if os.path.isdir(second_subfolder_path):

                    # Trova primi file nella seconda sottocartella
                    second_files = [f for f in os.listdir(second_subfolder_path) if os.path.isfile(os.path.join(second_subfolder_path, f))]

                    for third_subfolder in os.listdir(second_subfolder_path):
                        third_subfolder_path = os.path.join(second_subfolder_path, third_subfolder)
                        if os.path.isdir(third_subfolder_path):
                            next_subfolder = None

                            for next_subfolder_candidate in os.listdir(third_subfolder_path):
                                next_subfolder_path = os.path.join(third_subfolder_path, next_subfolder_candidate)
                                if os.path.isdir(next_subfolder_path):
                                    next_subfolder = next_subfolder_candidate
                                    break

                            item_size = 0
                            for root, _, files in os.walk(third_subfolder_path):
                                for file in files:
                                    item_size += os.path.getsize(os.path.join(root, file))

                            item_size_str = format_item_size(item_size)

                            files_in_third = [f for f in os.listdir(third_subfolder_path) if os.path.isfile(os.path.join(third_subfolder_path, f))]
                            if files_in_third:
                                file_name = files_in_third[0].replace('.data', '')
                            else:
                                file_name = ''

                            dataurl_parts, part_paths = generate_dataurl_parts(
                                third_subfolder_path,
                                first_subfolder.replace(' ', '%20'),
                                second_subfolder.replace(' ', '%20'),
                                third_subfolder.replace(' ', '%20'),
                                next_subfolder,
                                file_name
                            )

                            part_num_start = len(dataurl_parts) + 2

                            for idx, sec_file in enumerate(second_files, start=part_num_start):
                                encoded_first = first_subfolder.replace(' ', '%20')
                                encoded_second = second_subfolder.replace(' ', '%20')
                                part_paths.append(f"part{idx}path=Hdd1:\\Content\\0000000000000000\\{encoded_first}\\{encoded_second}\\")
                                dataurl_parts.append(f"dataurlpart{idx}={base_url}/{encoded_first}/{encoded_second}/{sec_file}")

                            ini_entry = template.format(
                                itemTitle=api_item_title,
                                first_subfolder_encoded=first_subfolder.replace(' ', '%20'),
                                second_subfolder=second_subfolder.replace(' ', '%20'),
                                third_subfolder=third_subfolder.replace(' ', '%20'),
                                file_name=file_name,
                                itemSize=item_size_str,
                                dataurl_parts='\n'.join(dataurl_parts),
                                part_paths='\n'.join(part_paths)
                            )

                            ini_data[api_item_title] = ini_entry

    with open(output_file, 'w', encoding='utf-8') as ini_file:
        for entry in ini_data.values():
            ini_file.write(f"{entry}\n")

    print(f"Created INI file: {output_file}")

if __name__ == "__main__":
    base_directory = r"D:\Iso2God\GOD_GAMES"  # Change with your path
    output_file = os.path.join(base_directory, "all_configs.ini")
    create_ini_file(base_directory, output_file)
