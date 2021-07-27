import requests

class Course:
    def __init__(self):
        super().__init__()
        self.url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        data = requests.get(self.url).json()
        self.course = 0
        for course in data:
            if course["r030"] == 643:
                self.course = course["rate"]
                break
        if self.course==0:
            raise KeyError
    
    def rub_uah(self, rub:int):
        return round(rub*self.course)
    
    def uah_rub(self, uah:int):
        return round(uah/self.course)