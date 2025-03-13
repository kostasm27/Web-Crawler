import io
import string
from bs4 import BeautifulSoup
import requests
import re
import lxml.html
import lxml
from MyCrawler import Crawler_Function

UrlFile = 'Url_File.txt'
ParagraphFile = 'Paragraph File.txt'
clean = re.compile('<.*?>|&amp;|\n')


def IsEnglish(html):
    if html == "":
        return None
    try:
        if lxml.html.fromstring(html).get('lang') == 'en':
            return True
        return None
    except lxml.etree.ParserError:
        return None


def Get_data(Url):
    try:
        r = requests.get(Url, timeout=(3, 4.6), headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (XHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
        if r.status_code != 200:
            return None
        if "text/html" in r.headers["content-type"]:
            return r.text
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.Timeout:
        return None


def Is_Html_None(Html):
    if Html is None:
        return True
    else:
        return False


def Get_Dictionary(DictionaryForIndexer, html_data, Link):
    soup = BeautifulSoup(html_data, 'html.parser')
    Doc = ""
    if len(soup.find_all('p')) != 0:
        if Link not in DictionaryForIndexer:
            for data in soup.find_all('p'):
                Doc += str(re.sub(clean, '', str(data)))
                Doc = Doc.lower()
                # remove unicode
                Doc = re.sub(r'[^\x00-\x7F]+', ' ', Doc)
                # remove simeia stixis
                Doc = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', Doc)
            # pernao sto link to keimeno pou exei se lower case gia na mporeso na kano tin sigkrisi meta
            DictionaryForIndexer[Link] = Doc
    return DictionaryForIndexer


def Restart_Files(RestartValue):
    if not RestartValue:
        file = open(UrlFile, 'w')
        file.write('')
        file.close()
        file = open(ParagraphFile, 'w')
        file.write('')
        file.close()


def Write_The_Paragraphs_And_Urls(Paragraphs):
    Url = open(UrlFile, 'a')
    # for link in Set:
    #     F.write(link + '\n')
    # F.close()
    with io.open(ParagraphFile, 'a', encoding="utf-8") as f:
        for i in Paragraphs:
            f.write("\n")
            f.write(i + '\n')
            Url.write(i + '\n')
            f.write(Paragraphs.get(i) + '\n')
    Url.close()

#test
Crawler_Function(Main_Link="https://www.masterstudies.com/Master-of-Science-in-Computational-Science/Switzerland/USI/",Number_Of_Links=200, RestartValue=1, Number_of_Threads=200)
# Crawler_Function(Main_Link="https://www.fluentu.com/blog/english/best-websites-to-learn-english/", Number_Of_Links=200, RestartValue=1, Number_of_Threads=100)
# Crawler_Function(Main_Link= "Wikipedia", Number_Of_Links=200, RestartValue=1, Number_of_Threads=100)
# Crawler_Function(Main_Link= "https://www.espn.com/", Number_Of_Links=200, RestartValue=1, Number_of_Threads=100)


# Crawler_Function(Main_Link="https://www.skroutz.gr/", Number_Of_Links=200, RestartValue=1, Number_of_Threads=100)

# url = "https://www.masterstudies.com/Master-of-Science-in-Computational-Science/Switzerland/USI/"
# url ="https://www.fluentu.com/blog/english/best-websites-to-learn-english/"
# url="https://www.espn.com/"
