"""toolset for extracting specific passages from the corpus provided on altafsir.com"""


def get_soup(TafsirId, Sura, Aya, page=1):
    """Fetch source code for any given page for TafsirID, Sura and Aya
       returns: bs4.BeautifulSoup object"""

    from bs4 import BeautifulSoup
    from requests import get

    link = f"https://www.altafsir.com/Tafasir.asp?tMadhNo=0&tTafsirNo={TafsirId}&tSoraNo={Sura}&tAyahNo={Aya}&tDisplay=yes&Page={page}&UserProfile=0&LanguageId=1"
    # get link and soupify
    response = get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # returns soup
    return soup


def tafsir_getter(TafsirId, Sura, Aya, page):
    """filters source code for actual tafsir content
       returns: bs4.element.Tag object """

    # retreive Data
    soup = get_soup(TafsirId, Sura, Aya, page).select_one("#SearchResults div")

    # filter soup for desired content
    if soup.find("center") != None:
        soup.center.decompose()

    soup.label.decompose()

    # break if last page
    if len(soup.text) == 2:
        return "Last Page"

    # return soup
    else:
        return soup


def tafsir_entry_pager(TafsirId, Sura, Aya):
    """tool needed to paginate through the JavaScript generated subpages for each SearchResult for a given passage
       returns: list object containing all subpages"""

    list = []
    i = 1
    while True:
        x = tafsir_getter(TafsirId, Sura, Aya, i)
        # if return value of tafsir_getter == "Last Page"
        if x != "Last Page":
            list.append(x)
            i += 1
        else:
            break
    return list


def collect_data(TafsirId, Sura, Aya):
    """collects given Aya from Sura from a specified Tafsir
       returns: string"""

    import pandas as pd

    # check validity of request
    if get_soup(TafsirId, Sura, Aya, 1).select_one("#SearchResults div") == None:
        print("invalid object: check if TafsirId, Sura and Aya are within range!")
        return None

    # if request is valid proceed
    else:
        data = tafsir_entry_pager(TafsirId, Sura, Aya)
        # join list entries to plain text
        data = "\n".join([i for i in [i.get_text().strip() for i in data]])
        # returns list
        return data


def write_data(data, TafsirId, Sura, Aya):
    """extracts scraping result to text file
       returns: None"""

    # Extracts Text from HTML and saves to file
    print(f"Writing to {TafsirId}_{Sura}_{Aya}.txt")
    with open(f"{TafsirId}_{Sura}_{Aya}.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("Saved file successfully")
    return None


def runscript():
    # Input prompt
    TafsirId = int(input("Input TafsirId: "))
    Sura = int(input("Input Sura: "))
    Aya = int(input("Input Aya: "))

    print(f"fetching Sura {Sura}, Aya {Aya} from Tafsir {TafsirId}...")
    data = collect_data(TafsirId, Sura, Aya)

    print("writing data to file...")
    write_data(data, TafsirId, Sura, Aya)
    return data


if __name__ == "__main__":
    runscript()
