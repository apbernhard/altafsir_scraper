from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
import re


# Declaring public methods
def normalize(string):
    """Wendet die Gewünschten Normalisierungsschritte an"""

    # Unicode-Zeichensatz normalisieren
    str_norm = normalize_unicode(string)
    
    # Diakritika aus dem Text entfernen
    str_norm = dediac_ar(str_norm)

    # Koranzitate, Verweise und Eulogien entfernen
    str_norm = __remove_aya(str_norm)
    str_norm = __remove_ref(str_norm)
    str_norm = __remove_eulogies(str_norm)
    
    # Zeichensatz auf relevante Zeichen reduzieren
    str_norm = __reduce_charset(str_norm)

    return str_norm


def __reduce_charset(text):
    """Entfernt alle Zeichen aus dem Text, die nicht zwischen
    'X' und 'Y' liegen"""

    chars_excluded = '[^\u0621-\u064A ]'
    text = re.sub(chars_excluded, ' ', text)
    
    return text

def __remove_aya(text):
    """Entfernt alle aus dem Koran zitierten Textstellen"""
    
    aya = '\{(.*?)\}'
    text = re.sub(aya, '', text)

    return text

def __remove_ref(text):
    """Entfernt alle Verweise auf weitere Verse im Koran
    aus dem Text"""
    
    ref = '\[(.*?)\]'
    text = re.sub(ref, '', text)
    
    return text

def __remove_eulogies(text):
    """Entfernt Eulogien (Segenssprüche) aus dem Text"""
    
    with open("./assets/filter/eulogies.txt", encoding="utf-8") as f:
        eulogies = f.read().splitlines()
    
    for eulogy in eulogies:
        text = re.sub(eulogy, '', text)
    
    return text