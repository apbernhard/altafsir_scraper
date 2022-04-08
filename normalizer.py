from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
import re


# Declaring public methods
def normalize(string):
    """Applies defined normalization functions"""

    # normalize Unicode
    str_norm = normalize_unicode(string)
    
    # remove diacritics
    str_norm = dediac_ar(str_norm)

    # remove Quranic citations, references and eulogies
    str_norm = __remove_aya(str_norm)
    str_norm = __remove_ref(str_norm)
    str_norm = __remove_eulogies(str_norm)
    
    # reduce character encoding to relevant characters
    str_norm = __reduce_charset(str_norm)

    return str_norm


def __reduce_charset(text):
    """Removes all the characters from the text that are not between
    hamza and ya"""

    chars_excluded = '[^\u0621-\u064A ]'
    text = re.sub(chars_excluded, ' ', text)
    
    return text

def __remove_aya(text):
    """Removes all Quranic citations"""
    
    aya = '\{(.*?)\}'
    text = re.sub(aya, '', text)

    return text

def __remove_ref(text):
    """removes all Quranic references"""
    
    ref = '\[(.*?)\]'
    text = re.sub(ref, '', text)
    
    return text

def __remove_eulogies(text):
    """Removes eulogies"""
    
    with open("./assets/filter/eulogies.txt", encoding="utf-8") as f:
        eulogies = f.read().splitlines()
    
    for eulogy in eulogies:
        text = re.sub(eulogy, '', text)
    
    return text