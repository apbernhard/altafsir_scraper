"""toolset for loading specific passages from the corpus provided on altafsir.com"""


# Creating a Base class
class tafsir_sample:
    def __init__(self, MadhabId, TafsirId, Sura, Aya_init, Aya_end):
        self.MadhabId = MadhabId
        self.TafsirId = TafsirId
        self.Sura = Sura
        self.Aya_init = Aya_init
        self.Aya_end = Aya_end
        self.Code = ""
        self.Text = ""

# Declaring public methods
    def load_data(self):
        """collects given Aya from Sura from a specified Tafsir
           returns: string"""
        import json

        mypath = "C:\\Users\\Adrian\\sciebo\\Masterarbeit\\SFB-Kollaborationsordner\\Korpus\\altafsir\\"

        # check validity of request
        # if sura is represented in korpus_aya_uebersicht.csv:
            # if aya is represented in korpus == True
                # mypath = "C:\\Users\\Adrian\\sciebo\\Masterarbeit\\SFB-Kollaborationsordner\\Korpus\\altafsir\\"
                # with open(mypath + f"altafsir-{self.MadhabId}-{self.TafsirId}-{self.Sura}-{self.Aya}-{self.Aya_end}", encoding="utf8") as f:
                #     self.Text = json.load(f)["text"]
            # else 
                # print("invalid object: check if TafsirId, Sura and Aya are within range!")
                # return "collect not successful"
        # if request is valid proceed

        with open(mypath + f"altafsir-{self.MadhabId}-{self.TafsirId}-{self.Sura}-{self.Aya_init}-{self.Aya_end}.json", encoding="utf8") as f:
            self.Text = json.load(f)["text"]

        return("collected!")
