import urllib3, ssl
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class HTMLScanConfig:
    search_attributes = ['href', 'src', 'data-src', 'action', 'content']
    extensions = (
                ".php", ".html", ".htm", ".js", ".css", ".xml", ".json",
                ".py", ".java", ".c", ".cpp", ".cs", ".rb", ".go", ".rs",
                ".sql", ".db", ".csv", ".xls", ".xlsx",
                ".jpg", ".jpeg", ".png", ".gif", ".svg", ".mp3", ".mp4", ".mkv",
                ".txt", ".md", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".ico",
                ".zip", ".tar", ".gz", ".rar", ".7z", ".iso", ".exe", ".apk"
            )

class UrlFinder:
    def __init__(self, url, args):
        self.__url = url
        self.__args = args
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode    = ssl.CERT_NONE
        self.__http = urllib3.PoolManager(ssl_context=ssl_context)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.__found_urls = {}  # all osdomain onsdomain hasparams noparams hasext noext keepslash

    def __send_request(self):
        return self.__http.request('GET', self.__url, timeout=10.0)
    
    def __format_html(self, data):          
        return BeautifulSoup(data, "html.parser")
    
    def __url_filtered(self, url, filters):
        for filter in filters:
            if filter not in self.__found_urls:
                self.__found_urls[filter] = []

            match filter:
                case "osdomain":
                    self.__filter_osdomain(filter, url)
                case "onsdomain":
                    self.__filter_onsdomain(filter, url)
                case "hasparams":
                    self.__filter_hasparams(filter, url)
                case "keepslash":
                    self.__filter_keepslash(filter, url)
                case "hasext":
                    self.__filter_hasext(filter, url)
                case "noext":
                    self.__filter_noext(filter, url)
                case "all":
                    self.__found_urls[filter].append(url)
                case _:
                    pass
                
    def __filter_osdomain(self, filter, url):
        if self.__get_domain_from_url(url) == self.__get_domain_from_url(self.__url):
            self.__found_urls[filter].append(url)

    def __filter_onsdomain(self, filter, url):
        if self.__get_domain_from_url(url) not in self.__url:
            self.__found_urls[filter].append(url)

    def __filter_hasparams(self, filter, url):
        if "?" in url:
            self.__found_urls[filter].append(url)

    def __filter_keepslash(self, filter, url):
        if url.endswith("/"):
            self.__found_urls[filter].append(url)

    def __filter_hasext(self, filter, url):
        if url.endswith(HTMLScanConfig.extensions):
            self.__found_urls[filter].append(url)

    def __filter_noext(self, filter, url):
        segments = url.split("/")
        if len(segments) > 1 and segments[-1] and not segments[-1].endswith(HTMLScanConfig.extensions) and not "?" in segments[-1] and not '.' in segments[-1]:
            self.__found_urls[filter].append(url)
        
    def __get_domain_from_url(self, url):
        if url is None:
            return None
        parsed = urlparse(url)
        hostname = parsed.hostname

        if hostname is not None:
            parts = hostname.split(".")
            if len(parts) == 2:
                return "".join(parts[-2]) # letzte zwei Teile
            if len(parts) > 2:
                if(len(parts[-2]) > 1 and len(parts[-2]) < 4 ) and (len(parts[-1]) == 2 ): # z.B. https://example.co.uk/ or https://example.com.au/ 
                    return "".join(parts[-3]) # letzte drei Teile
                else:
                    return "".join(parts[-2]) # letzte zwei Teile
            else:
                return hostname
        
    def search_for_urls(self):
        try:
            response = self.__send_request()
            soup = self.__format_html(response.data)            

            for tag in soup.find_all():
                for attr_config in HTMLScanConfig.search_attributes:
                    try:
                        attr_value = tag[attr_config]
                        if attr_value.startswith('http'):
                            self.__url_filtered(attr_value, self.__args.filters)
                    except:
                        pass  
            response.close()
            return self.__found_urls
        except Exception as e:
            response.close()
            raise Exception(f"[ERROR] {self.__url} nicht erreichbar\n{e}")
