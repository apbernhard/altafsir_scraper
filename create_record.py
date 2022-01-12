"""toolset for extracting specific passages from the corpus provided on altafsir.com"""


def get_soup(TafsirId, Sura, Aya, page=1):
    """Fetch source code for any given page for TafsirID, Sura and Aya
       returns bs4.BeautifulSoup object"""

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
       returns bs4.element.Tag object """

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
       returns list object"""

    list = []
    i = 1
    while True:
        x = tafsir_getter(TafsirId, Sura, Aya, i)
        # if return value of tafsir_getter == "Last Page"
        if x != "Last Page":
            list.append(x)
            i +=1
        else:
            break
    return list


def tafsir_metadata(TafsirId, Sura, Aya):
    """Tool fetching metadata on entry
       returns pandas.Series object"""

    import pandas as pd

    soup = get_soup(TafsirId, Sura, Aya, 1)

    # Receive data and store in dict
    metadata = {}
    metadata["TafsirId"] = TafsirId
    metadata["Sura"] = Sura
    metadata["Aya"] = Aya
    metadata['Description'] = soup.find("meta", attrs={'name': 'description'})['content']
    metadata['Keywords'] = soup.find("meta", attrs={'name': 'keywords'})['content'].strip().split(",")[1:]

    # convert dict to 
    data = pd.Series(metadata)
    
    # returns pd.Series
    return data


def collect_data(TafsirId, Sura, Aya):
    """collects metadata and contents for given Sura and Aya from a specified Tafsir
       returns pandas.Series object with SoupContent as list of bs4.element.Tag objects"""
    
    # check validity of request
    if get_soup(TafsirId, Sura, Aya, 1).select_one("#SearchResults div") == None:
        print("invalid object: check if TafsirId, Sura and Aya are within range!")
        return None

    # if request is valid save in Dataframe
    else:
        data = tafsir_metadata(TafsirId, Sura, Aya)
        data["SoupContent"] = tafsir_entry_pager(TafsirId, Sura, Aya)
                
        # returns Series
        return data


def runscript():
    print("fetching exemplary data...")
    return collect_data(1, 1, 7)


if __name__ == "__main__":
    runscript()

