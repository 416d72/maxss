# Description

This script injects your blind XSS payload into a set of URLs.

## Requirements

- Linux shell (bash/zsh)
- Python 3.7+
- [XSShunter account](https://xsshunter.com) (or your custom blind xss payload)

## Installation

- `git clone https://github.com/ShogunExecutioner/maxss.git && cd maxss`
- Install a virtual environment (Optional) `python -m venv .env`
- `pip install -r requirements.txt`

## Configuration

- Add your blind XSS payloads in `static/payloads.txt`. **Note: the more payloads you add, the more time this script will consume**
- Check `static/config.json` if you want to add an HTTP proxy (Like Burp) or edit other stuff.
    > - Proxy should be like `http://proxy.com`.
    > - If you use credentials you can pass them in proxy URL e.g `http://user:pass@some.proxy.com`
    > - Timeout must be float number

- Check `static/extensions.json` file if you want to add/remove extensions which will be removed from URL list.

## Usage

- `python3 maxss.py -d <domain>`

> Fetch a URL list related to the target domain from _archive.org_ 
>
> By default it will use cached file if found.
>
> To force fetch the newest list, add `-a`
- `python3 maxss.py [-f <file path>]` 
> Skip scrapping and work on URLs in the provided file. 

## Known bugs

- Lack of `socks` proxy because `aiohttp` doesn't support it yet.

## TODO

☐ Better redirection handling

☐ Adding more scrappers

🗹 WAF detector

🗹 Proxy

🗹 Advanced Logging

## Inspiration

- [Mohamed Noir's post](https://www.facebook.com/groups/pentesting4arabs/?post_id=989611208161843)
- [XSStrike](https://github.com/s0md3v/XSStrike/blob/master/core/wafDetector.py)

## Special thanks

- [Zigoo0](https://github.com/zigoo0)
- Sohib Atef
