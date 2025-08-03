import argparse, sys, urllib3, ssl, urls_finder
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from urllib.parse import urlparse

# Init Colorama
init(autoreset=True)
# Argument Parser
title = r"""
   ___     _     _   _ ___ _       
  / __|___| |_  | | | | _ \ |   ___
 | (_ / -_)  _| | |_| |   / |__(_-<
  \___\___|\__|  \___/|_|_\____/__/                           
"""

exp = """
################ Examples:
gurls.py -u https://www.example.com
gurls.py -u https://www.example.com -f osdomain
gurls.py -u https://www.example.com -f onsdomain
gurls.py -u https://www.example.com -f osdomain hasparams
gurls.py -u https://www.example.com -f osdomain noparams
gurls.py -u https://www.example.com -f osdomain hasext noext keepslash
...

################ Explanations:
osdomain:   (Only same domain) e.g. http://example.com/... but not e.g. http://google.com/
onsdomain:  (Only other domains) e.g. search on http://example.com/... but show all external URLs, e.g. http://google.com/, NOT http://example.com/...
hasparams:  Show only URLs with query parameters, e.g. http://example.com/page.php?id=
hasext:     Show only URLs with file extensions, e.g. http://example.com/page.php
noext:      Show only URLs without file extensions, e.g. http://example.com/page
keepslash:  Do not remove the trailing slash from URLs, e.g. http://example.com/page/
"""
parser = argparse.ArgumentParser(f"""Simple URL finder in HTML page\n
{title}
{exp}
"""
)
parser.add_argument("-u", "--url", type=str, action="store", help="Examples: -u https://www.example.com")
parser.add_argument("-o", "--output", type=str, action="store", help="Examples: -o result.txt")
parser.add_argument(
    "-f", "--filters",
    type=str,
    nargs='+',
    default=["all"],  # als Liste, nicht als String
    help=("Examples: -f all(Default) or osdomain onsdomain hasparams noparams hasext noext keepslash\n")
)

# Debug: falls kein Parameter angegeben wird, Standard-URL anhängen
# if len(sys.argv) == 1:
#     sys.argv += ["-h"]
#     # sys.argv += ["-u", "https://example.com"] #osdomain
#     # sys.argv += ["-f", "noext", "osdomain"]

try:
    args = parser.parse_args()
    print(title)

    print(Style.BRIGHT + Fore.CYAN + "\n========== Arguments ==========")
    try:
        print(Fore.YELLOW + f"URL: {args.url}")
    except:
        pass
    try:
        filters = {f: [] for f in args.filters}
        filter_text = ", ".join(args.filters)
        print(Fore.YELLOW + f"Filter: {filter_text}")
    except:
        pass
    try:
        print(Fore.YELLOW + f"Output file: {args.output}")
    except:
        pass
    print(Style.BRIGHT + Fore.CYAN + "====================================\n\n")

    print(Fore.CYAN + f"[INFO] Send request to: {args.url}")
    urls = urls_finder.UrlFinder(args.url.strip(), args=args).search_for_urls()

    print(Fore.GREEN + "[INFO] Connection successful, processing HTML..")
    print(Style.BRIGHT + Fore.CYAN + "\n========== FOUND LINKS ==========")

    for filter, urls in urls.items():
        print(Fore.CYAN + f"[FILTER] {filter}:")
        print(Fore.YELLOW + f"[RESULT] {len(urls)} URLs found.")
        for i, url in enumerate(urls, start=1):
            print(Fore.WHITE + f"[{i}] " + Fore.GREEN + url)
    print(Style.BRIGHT + Fore.CYAN + "====================================\n")
except Exception as e:
    print(Fore.RED + f"{e}")
    sys.exit(1)
except KeyboardInterrupt:
    print(Fore.RED + "Finished")
    sys.exit(1)