import json
from pprint import pprint
import sys

from delicious_download import BOOKMARKS_FILE

HEADING_RANK = 1
DEFAULT_FORMAT = 'html'


class InvalidFormatError(Exception):
    pass


def main(format_=DEFAULT_FORMAT):
    bookmarks = _get_bookmarks()
    if format_ not in FUNC_MAP:
        raise InvalidFormatError
    output = FUNC_MAP.get(format_)(bookmarks)
    pprint(output)

def _get_bookmarks():
    with open(BOOKMARKS_FILE, 'r') as in_file:
        return json.load(in_file)

def _format_as_html(bookmarks):
    template = _get_html_template()
    output = []

    for url, details in bookmarks.items():
        output.append(template.format(
            heading_rank=HEADING_RANK,
            title=details.get('title'),
            description=details.get('description'),
            url=url,
            tags=u' '.join(details.get('tags', []))
        ))

    return ''.join(output)

def _get_html_template():
    return (u''
        '<h{heading_rank}>{title}</h{heading_rank}>'
        '<p>{description}</p>'
        '<a href="{url}">{url}</a>'
        '<p>{tags}</p>'
    )

def _format_as_json(bookmarks):
    return json.dumps(bookmarks)

def _format_as_markdown(bookmarks):
    template = _get_markdown_template()
    output = []

    for url, details in bookmarks.items():
        output.append(template.format(
            octothorps=u'#' * HEADING_RANK,
            title=details.get('title'),
            description=details.get('description'),
            url=url,
            tags=u'\n'.join([u'*  {0}'.format(tag) for tag in details.get('tags', [])])
        ))

    return u''.join(output)

def _get_markdown_template():
    return (u''
        '{octothorps} {title}\n'
        '{description}\n'
        '[{url} {url}]\n'
        '{tags}\n\n'
    )

FUNC_MAP = {
    'html': _format_as_html,
    'json': _format_as_json,
    'markdown': _format_as_markdown
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output_format = sys.argv[1]
    else:
        output_format = 'markdown'

    main(output_format)
