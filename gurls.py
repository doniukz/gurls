import argparse, sys, urls_finder, os
from colorama import Fore, Style, init


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
        if args.output is not None:
            args.output = args.output.strip()
            print(Fore.YELLOW + f"Output file: {args.output}")
            # Ordner vom Skript selbst ermitteln # Pfad für Datei im gleichen Ordner bauen
            output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
            f = open(output_file, "w", encoding="utf-8")
    except Exception as e:
        sys.stderr.write(f"Fehler: {e}\n")

    print(Style.BRIGHT + Fore.CYAN + "====================================\n\n")
    if args.output is not None:
        f.write("====================================\n\n")

    print(Fore.CYAN + f"[INFO] Send request to: {args.url}")
    if args.output is not None:
        f.write(f"[INFO] Send request to: {args.url}\n")
    urls = urls_finder.UrlFinder(args.url.strip(), args=args).search_for_urls()

    print(Fore.GREEN + "[INFO] Connection successful, processing HTML..")
    if args.output is not None:
        f.write(f"[INFO] Connection successful, processing HTML..\n")
    print(Style.BRIGHT + Fore.CYAN + "\n========== FOUND LINKS ==========")
    if args.output is not None:
        f.write(f"\n========== FOUND LINKS ==========\n")

    for filter, urls in urls.items():
        print(Fore.CYAN + f"[FILTER] {filter}:")
        if args.output is not None:
            f.write(f"[FILTER] {filter}:\n")
        print(Fore.YELLOW + f"[RESULT] {len(urls)} URLs found.")
        if args.output is not None:
            f.write(f"[RESULT] {len(urls)} URLs found.\n")
        for i, url in enumerate(urls, start=1):
            print(Fore.WHITE + f"[{i}] " + Fore.GREEN + url)
            if args.output is not None:
                f.write(f"[{i}] " + url + "\n")
    print(Style.BRIGHT + Fore.CYAN + "====================================\n")
    if args.output is not None:
        f.write("====================================\n")
except Exception as e:
    print(Fore.RED + f"{e}")
    if args.output is not None:
        f.write(f"{e}\n")
    sys.exit(1)
except KeyboardInterrupt:
    print(Fore.RED + "Finished")
    if args.output is not None:
        f.write("Finished\n")
    sys.exit(1)
finally:
    if args.output is not None:
        f.close()