from bs4 import BeautifulSoup
from bs4 import NavigableString
import re

CATEGORY_SECTION_TITLE = "In wenigen Klicks zum Stellenangebot"


def _select_one(root_tag, select_string, index):
    """
    Select single tag on None from root tag using selection string
    :param root_tag: Root tag or None to search in
    :param select_string: jQuery like selecting string
    :param index: index of element from selected elements array
    :return: Tag or None
    """
    if root_tag is None:
        return None

    tags = root_tag.select(select_string)
    if len(tags) > index:
        return tags[index]
    else:
        return None


def _select_list(root_tag, select_string):
    """
    Select multiple tags from root tag using selection string
    :param root_tag: Root tag or None to search in
    :param select_string: jQuery like selecting string
    :return: Array of tags or empty array
    """
    if root_tag is None:
        return []

    return root_tag.select(select_string)


def _extract_text(root_tag):
    """
    Extract text from  tag
    :param root_tag: Tag or None to extract text from
    :return: text string (may be empty)
    """
    if root_tag is None:
        return None

    if isinstance(root_tag, NavigableString):
        return root_tag.string.strip()

    # if root_tag.name == 'a':
    #    if 'href' in root_tag.attrs:
    #        return ' ' + root_tag.attrs['href'] + ' '
    #    else:
    #       return " "

    if root_tag.name == 'br':
        return "\n"

    text = ""
    for cn in root_tag.contents:
        text = text + _extract_text(cn)

    return text


def _attr(tag, attr_name):
    if tag is None:
        return None

    if attr_name not in tag.attrs:
        return None

    return tag.attrs[attr_name]


class JobbrosePage:
    """
    Class parse jobbrose page and let to extract data.
    """

    def __init__(self, page_text):
        self.page_dom = BeautifulSoup(page_text, "html.parser")

    def contain_categories(self):
        section_title = _extract_text(_select_one(self.page_dom, 'div.klicksuchenavigation h4', 0))

        return section_title == CATEGORY_SECTION_TITLE

    def get_categories(self):
        categories = []

        if not self.contain_categories():
            return categories

        # Category title contains total number of positions in it
        # This regex allow to remove this number
        number_of_positions_regex=re.compile(r"\(\d+\)$")

        categories_tags = _select_list(self.page_dom, 'div.klicksucheliste ul.liste li span.klicksucheeintrag a')

        for c_tag in categories_tags:
            link = _attr(c_tag, 'href')
            name = number_of_positions_regex.sub("", _extract_text(c_tag)).strip()
            if name:
                categories.append({'name': name, 'link': link})

        return categories
