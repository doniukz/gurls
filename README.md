gurls.py – Simple URL Finder in HTML Pages
===============================

Description:
------------
This tool fetches a given URL, parses its HTML content, and extracts URLs found within specific HTML attributes.
It supports multiple filters to refine the results, such as filtering by domain, URL parameters, file extensions, and more.

Features:
---------
- Filter URLs by:
  - Same domain (osdomain)
  - Other domains (onsdomain)
  - URLs with query parameters (hasparams)
  - URLs with file extensions (hasext)
  - URLs without file extensions (noext)
  - Preserve trailing slash (keepslash)
  - Show all URLs (all, default)
- Handles common URL-containing attributes (href, src, action, content, data-src)
- Ignores SSL certificate errors (useful for testing)
- Colored terminal output for better readability
- Optional output to a file

Requirements:
-------------
- Python 3.x
- Libraries:
  - argparse
  - urllib3
  - beautifulsoup4
  - colorama

Install Dependencies:
---------------------
pip install urllib3 beautifulsoup4 colorama

Usage:
------
python gurls.py -u <URL> [-f <filters>] [-o <output_file>]

Arguments:
----------
-u, --url       Target URL to scan (e.g. https://example.com)
-f, --filters   Space-separated list of filters to apply (default: all)
-o, --output    Optional output file to save found URLs

Examples:
---------
1) Scan all URLs found at https://www.example.com (default: all)
   python gurls.py -u https://www.example.com
2) Scan only URLs from the same domain:
   python gurls.py -u https://www.example.com -f osdomain
3) Scan only external domains:
   python gurls.py -u https://www.example.com -f onsdomain
4) Scan same domain URLs that have query parameters:
   python gurls.py -u https://www.example.com -f osdomain hasparams
5) Scan URLs with or without file extensions and keep trailing slashes:
   python gurls.py -u https://www.example.com -f osdomain hasext noext keepslash

Filters Explained:
------------------
osdomain   : URLs only from the same domain as the input URL (e.g. example.com)
onsdomain  : URLs only from other (external) domains
hasparams  : URLs containing query parameters (?id=123)
hasext     : URLs ending with common file extensions (e.g. .php, .html)
noext      : URLs without file extensions
keepslash  : Preserve trailing slash at the end of URLs
all        : Include all URLs (default)

Notes:
------
- SSL verification is disabled to allow scraping from sites with self-signed or invalid certificates. Use with caution.
- Output can be saved to a file using the -o argument.
- The list of recognized file extensions is configurable in the source code (HTMLScanConfig.extensions).
- Extracts URLs from common HTML attributes like href, src, data-src, action, and content.

License:
--------
Open source, free to use.


Author: doniukz
