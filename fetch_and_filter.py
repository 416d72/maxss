from helpers import *
import requests


class FetchAndFilter:
    file_path = ''
    BASE_URL = "https://web.archive.org/cdx/search/cdx?url=*.{domain}&output=text&fl=original&collapse=urlkey"
    RAW_URLS = ""
    FINAL_URLS = []
    STATIC_FILES = []

    def __init__(self, target_domain: str):
        """
        Search Archive.org for all links that includes provided domain name
        and apply sanitizing filter to those links, then export to a text file.
        :param target_domain: [Optional]
        """
        self.TARGET_DOMAIN = target_domain
        update_status('Starting requester')
        self.load_extensions()
        self.fetch_url_list()
        self.sanitize_urls()
        self.create_output_dir()
        self.export_data()

    def load_extensions(self):
        try:
            with open(f"{sys.path[0]}/static_file_extensions.json") as file:
                self.STATIC_FILES = json.load(file)  # Add more as you like
        except FileNotFoundError:
            failure("Couldn't find static_file_extensions.json")
        except Exception as e:
            failure(f"static_file_extensions.json file is corrupted\nFull details:\t{e.__str__()}")

    def fetch_url_list(self):
        """
        Fetch archived links from archive.org
        :return:
        """
        try:
            response = requests.get(self.BASE_URL.format(domain=self.TARGET_DOMAIN))
            assert response.status_code == 200
            assert len(response.text) > len(self.TARGET_DOMAIN)
            self.RAW_URLS = response.text
            self.RAW_URLS = list(set(map(str.strip, self.RAW_URLS.split('\n'))))
            self.FINAL_URLS = self.RAW_URLS.copy()
        except requests.exceptions.RequestException:
            failure("Couldn't connect to archive.org")
        except AssertionError:
            failure(f"Nothing found about {self.TARGET_DOMAIN}")

    def sanitize_urls(self):
        """
        Remove unnecessary links like css, jpg files
        :return:
        """
        for url in self.RAW_URLS:
            for extension in self.STATIC_FILES:
                if url.find(f'.{extension}?') > 0 or url.endswith(f'.{extension}'):
                    self.FINAL_URLS.remove(url)
        self.FINAL_URLS = list(filter(None, self.FINAL_URLS))  # To remove empty strings

    @staticmethod
    def create_output_dir():
        try:
            os.mkdir('output')
        except FileExistsError:
            pass

    def export_data(self):
        try:
            self.file_path = f"{sys.path[0]}/output/{self.TARGET_DOMAIN}.txt"
            with open(self.file_path, 'w') as output_file:
                output_file.write('\n'.join(self.FINAL_URLS))
        except (FileNotFoundError, PermissionError, IOError) as e:
            failure(f"Couldn't write results to the target directory output/{self.TARGET_DOMAIN}\n{e}")


if __name__ == '__main__':
    test_url = FetchAndFilter(target_domain="video.techcrunch.com")
