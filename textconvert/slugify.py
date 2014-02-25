import re
import unicodedata
import types
import sys
from unidecode import unidecode

def smart_truncate(string, max_length=0, word_boundaries=False, separator=' '):
    """ Truncate a string """

    string = string.strip(separator)

    if not max_length:
        return string

    if len(string) < max_length:
        return string

    if not word_boundaries:
        return string[:max_length].strip(separator)

    if separator not in string:
        return string[:max_length]

    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word) + len(separator)
            if next_len <= max_length:
                truncated += '{0}{1}'.format(word, separator)
    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)


def slug(text, entities=True,  max_length=0, word_boundary=False, separator='-'):
    REPLACE1_REXP = re.compile(r'[\']+')
    REPLACE2_REXP = re.compile(r'[^-a-z0-9]+')
    REMOVE_REXP = re.compile('-{2,}')

    # translate
    text = unicodedata.normalize('NFKD', text)
    if sys.version_info < (3,):
        text = text.encode('ascii', 'ignore')

    # replace unwanted characters
    text = REPLACE1_REXP.sub('', text.lower()) # replace ' with nothing instead with -
    text = "-".join(text.split(" "))
    text = REPLACE2_REXP.sub('', text.lower())

    # remove redundant -
    text = REMOVE_REXP.sub('-', text).strip('-')

    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, '-')

    if separator != '-':
        text = text.replace('-', separator)

    return text
