from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import urllib

DELICIOUS_USERNAME = 'oramartindale'
DATE_REGEX = re.compile('This link recently saved by oramartindale on ([A-Za-z,\s0-9]*)')
BOOKMARKS_FILE = 'bookmarks.json'


def main():
    data = {}

    for i in xrange(1, 53):
        response = urllib.urlopen('https://del.icio.us/{}?&page={}'.format(
            DELICIOUS_USERNAME,
            i
        ))
        soup = BeautifulSoup(response.read(), 'html.parser')
        print soup
        divs = soup.find_all('div', class_='articleThumbBlock')
        if not divs:
            break
        for div in divs:
            key = div.find_all('div', class_='articleInfoPan')[0].a.get_text()
            for li in div.find_all('ul', class_='tagName'):
                tags = [b.get_text() for b in li.find_all('a')]
            description_paragraphs = div.find_all('div', class_='thumbTBriefTxt')[0].find_all('p')
            if description_paragraphs:
                description = '\n'.join((p.get_text() for p in description_paragraphs))
            else:
                description = ''
            dt_paragraphs = div.find_all('div', class_='articleInfoPan')[0].find_all('p')
            for p in dt_paragraphs:
                match = DATE_REGEX.match(p.get_text())
                if match:
                    dt = match.groups()[0]
                    dt = datetime.strptime(dt, '%B %d, %Y').date().isoformat()
                    break
            else:
                dt = None

            data[key] = {
                'title': div.h3.get_text(),
                'tags': tags,
                'description': description,
                'added_dt': dt
            }

    with open(BOOKMARKS_FILE, 'w') as out_file:
        json.dump(data, out_file)

if __name__ == '__main__':
    main()
