#X360Store

Automatically generates an `all_configs.ini` file for your Xbox 360 GOD-format games library, including metadata and local/HTTP paths for easy server access and management.

***

## 📋 Overview

This Python script scans your local Xbox 360 library (in GOD format), fetches readable game titles using the [XboxUnity API](https://xboxunity.net), computes total game sizes, and builds an INI file mapping local Xbox paths (e.g., `Hdd1:\Content\...`) and HTTP URLs for LAN streaming or downloads.

***

## 🚀 Requirements

- Python 3.9 or newer
- Python `requests` module (`pip install requests`)
- Xbox 360 games **already converted to GOD format**
- A local HTTP server serving the same folder structure (e.g., `http://192.168.1.38`)
- Internet connection for querying XboxUnity API

> **Important:**
> Before using this script, convert your ISO files to GOD format using [iso2god-rs-GUI](https://github.com/ItsDeidara/iso2god-rs-GUI).

***

## 📂 Expected Folder Structure

```
D:\Iso2God\GOD_GAMES\
└── FirstLevel\
    └── SecondLevel\
        └── ThirdLevel\
            ├── Data0000
            ├── Data0001
            └── ...
             
```

The HTTP server should serve files at URLs like:
`http://192.168.1.38/FirstLevel/SecondLevel/ThirdLevel/` or with https if you have an SSL Certificate.

***

## ⚙️ Configuration

Edit these values at the top of your script:

- `base_directory`: path to your local collection (default: `D:\Iso2God\GOD_GAMES`)
- `base_url`: your local HTTP server address (default: `http://192.168.1.38`)

***

## 🛠 Usage

1. Install dependencies:

```bash
pip install requests
```

2. Run the script:

```bash
python God2Ini.py
```

3. Find the final `all_configs.ini` file in your collection root folder.

***

## 📝 Output Format

Each INI entry includes:

- Readable game title (`itemTitle`)
- Static author tag (`itemAuthor=by kastro <3`)
- Total size of the third-level folder (in MB or GB)
- Local Xbox path to the third level (and beyond, if present)
- HTTP URLs for LAN access, with multiple `dataurlpartN` entries for extra file parts

Folder names containing spaces are automatically encoded as `%20` in URLs where required.

***

## 🐞 Troubleshooting \& Tips

- If a title isn’t found via API, the first folder-level name is used as a fallback.
- Make sure the HTTP server accurately mirrors your local structure and uses correct URL encoding.
- The script sums file sizes recursively under the third level—keep only relevant files in that hierarchy.

***

## 📜 License \& Legal

Use this script only with content you own the rights to. Do not distribute protected material illegally or violate software licenses.
For GOD conversion, use the recommended tool and respect all applicable software licenses.

***

## ❤️ Thanks

For ISO → GOD conversion, see:
[https://github.com/ItsDeidara/iso2god-rs-GUI](https://github.com/ItsDeidara/iso2god-rs-GUI)

***

## ❤️ Donate

If you want to support the project, you can do it here: https://ko-fi.com/kastrodev
