"""toolset for extracting specific passages from the corpus provided on altafsir.com"""


# Creating a Base class
class altafsir_extractor:
    def __init__(self, TafsirId, Sura, Aya):
        self.TafsirId = TafsirId
        self.Sura = Sura
        self.Aya = Aya
        self.Code = ""
        self.Text = ""

# Declaring public methods
    def collect_data(self):
        """collects given Aya from Sura from a specified Tafsir
           returns: string"""

        # check validity of request
        if self.__get_soup(1).select_one("#SearchResults div") == None:
            print("invalid object: check if TafsirId, Sura and Aya are within range!")
            return "collect not successful"

        # if request is valid proceed
        else:
            self.Code = self.__tafsir_entry_pager()
            # join list entries to plain text
            self.Text = "\n".join(
                [i for i in [i.get_text().strip() for i in self.Code]])

            return self.Text

    def write_data(self, path="./"):
        """extracts scraping result to text file
           returns: None"""

        # Extracts Text from HTML and saves to file
        print(f"Writing to {self.TafsirId}_{self.Sura}_{self.Aya}.txt")
        with open(f"{path}{self.TafsirId}_{self.Sura}_{self.Aya}.txt", "w", encoding="utf-8") as f:
            f.write(self.Text)
        print("Saved file successfully")
        return None

# Declaring private method
    def __get_soup(self, page=1):
        """Fetch source code for any given page for TafsirID, Sura and Aya
           returns: bs4.BeautifulSoup object"""

        from bs4 import BeautifulSoup
        from requests import get

        link = f"https://www.altafsir.com/Tafasir.asp?tMadhNo=0&tTafsirNo={self.TafsirId}&tSoraNo={self.Sura}&tAyahNo={self.Aya}&tDisplay=yes&Page={page}&UserProfile=0&LanguageId=1"
        # get link and soupify
        response = get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # returns soup
        return soup

    def __tafsir_getter(self, page):
        """filters source code for actual tafsir content
           returns: bs4.element.Tag object """
        from bs4 import BeautifulSoup

        # retreive Data
        soup = self.__get_soup(page).select_one("#SearchResults div")

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

    def __tafsir_entry_pager(self):
        """tool needed to paginate through the JavaScript generated subpages for each SearchResult for a given passage
           returns: list object containing all subpages"""

        list = []
        i = 1
        while True:
            x = self.__tafsir_getter(i)
            # if return value of tafsir_getter == "Last Page"
            if x != "Last Page":
                list.append(x)
                i += 1
            else:
                break
        return list


def runscript():
    # User prompt
    print("Please give following values:")
    TafsirId = input("TafsirId: ")
    Sura = input("Sura: ")
    Aya = input("Aya: ")

    # Fetch data
    print(f"fetching Tafsir {TafsirId}, Sura {Sura}, Aya {Aya}")
    object = altafsir_extractor(TafsirId, Sura, Aya)
    object.collect_data()

    # Output
    object.write_data()


if __name__ == "__main__":
    runscript()
