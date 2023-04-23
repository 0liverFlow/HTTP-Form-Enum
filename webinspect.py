import requests
from bs4 import BeautifulSoup as bsoup, Comment
import sys
import re

from rich import print as printc

class WebInspect:    
    def __init__(self, url, headers):
        if url.startswith('http'):
            url_parts = url.split('/')
            scheme = url_parts[0]
            authority = url_parts[2]
            self.url = scheme + '//' + authority
            try:
                self.response = requests.get(url, headers=headers)
                self.soup = bsoup(self.response.content, 'html.parser')
                self.headers = headers
            except requests.exceptions.ConnectionError:
                sys.exit(printc("[red1 b][-][/red1 b] Connection error: Make sure you have access to the Internet and that the URL is correct"))
        else:
            sys.exit(printc("[red1 b][-][/red1 b] URL format incorrect (must start with http:// or https://)"))

    @staticmethod
    def double_letter_format(string: str):
        letters = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
        numbers = "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"
        string = string.strip().upper()
        double_string = ''
        for char in string:
            if char in [' ', '-', '°']:
                double_string += char
            else:
                char_dec = ord(char)
                if 48 <= char_dec <= 57:
                    double_string += numbers[char_dec - 48]
                elif  char_dec >= 65 and char_dec <= 90:
                    double_string += letters[char_dec - 65] + ' '
        return double_string

    def get_language(self):
        # Returns the language used by the website
        try:
            webpage_language = self.soup.find('html')['lang']
            self.language = webpage_language
        except KeyError:
            self.language = None
        except TypeError:
            self.language = None

    def get_title(self):
        try:
            webpage_title = self.soup.find('head').find('title').string
            self.title = webpage_title
        except AttributeError:
            self.title = None
    
    def get_comments(self):
        webpage_comments = self.soup.find_all(string=lambda text: isinstance(text, Comment))
        if len(webpage_comments):
            self.comments = webpage_comments
        else:
            self.comments = None
    
    def get_meta_tags(self):
        webpage_meta_tags = self.soup.find('head').find_all("meta")
        if len(webpage_meta_tags):
            self.meta_tags = webpage_meta_tags
        else:
            self.meta_tags = None

    def get_hidden_inputs(self):
        webpage_hidden_inputs = self.soup.find_all("input", type="hidden")
        if len(webpage_hidden_inputs):
            self.hidden_inputs = list(set(webpage_hidden_inputs))
        else:
            self.hidden_inputs = None
    

    def get_display_none_tags(self):
        display_none_tags = self.soup.find_all(style=lambda style_attribute: style_attribute and 'display:none' in style_attribute)
        if len(display_none_tags):
            self.display_none = display_none_tags
        else:
            self.display_none = ""

    def get_forms(self):
        forms = self.soup.find_all("form")
        if len(forms):
            self.forms = forms
        else:
            self.forms = None
        
    def reset_password_link(self):
        # Checking for reset password links
        reset_link = self.soup.find_all("a",text=re.compile("Lost.*Password.*|Reset.*Password.*|Forgot.*Password.*, Mot de passe oublié.*|identifiant oublié.*|mot de passe perdu.*|Réinitialiser mot de passe.*", flags=re.I))
        if len(reset_link):
            self.reset_link = reset_link
        else:
            self.reset_link = None
    
    def get_robots_txt(self):
        try:
            webpage_robots_txt = requests.get(self.url + '/robots.txt')
            webpage_robots_txt_rules = webpage_robots_txt.text.split('\n')
            if len(webpage_robots_txt_rules):
                self.robots_txt = webpage_robots_txt_rules
            elif webpage_robots_txt.ok:
                printc("[red1 b][-][/red1 b] Robots.txt is empty")
            else:
                self.robots_txt = None
        except Exception: #check if user has access to internet.
            self.robots_txt = None

    def get_phpinfo(self):
        # Checking phpinfo file
        phpinfo_url = self.url + '/phpinfo.php'
        phpinfo_response = requests.get(phpinfo_url, headers=self.headers)
        if phpinfo_response.ok:
            self.phpinfo = phpinfo_response.content
        else:
            self.phpinfo = None
           
    def get_cgidir(self):
        default_cgidirs = ['/admin/cgi-bin', '/cgi-bin/admin', '/cgi-bin']
        for cgidir in default_cgidirs:
            cgidir_url = self.url + cgidir
            cgidir_response = requests.get(cgidir_url, headers=self.headers)
            if cgidir_response.ok:
                self.cgidir = cgidir_response.url
                break
        else:
            self.cgidir = None