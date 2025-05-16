from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from date_parsing import standardize_date
from json_formater import format_json
class CaesarsScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.valid_sports = { "Football - NFL": "https://sportsbook.caesars.com/us/pa/bet/americanfootball/events/all?id=007d7c61-07a7-4e18-bb40-15104b6eac92", 
                              "Basketball - NBA": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=5806c896-4eec-4de1-874f-afed93114b8c",
                              #"Basketball - NCAAM" : "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=d246a1dd-72bf-45d1-bc86-efc519fa8e90",
                              "Basketball - WNCAAB": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=e95700bc-4ed2-466c-bc32-b584530ea563",
                              "Basketball - EuroLeague": "https://sportsbook.caesars.com/us/pa/bet/basketball?id=2f09984a-0d36-4326-b6c1-7903df16fa79",
                              "Basketball - British BBL": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=9c7512a0-bfc0-47cb-9147-871535fe69df",
                              "Basketball - Poland Basket Liga": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=f154cff4-2564-4b8a-a1c7-690215d1be30",
                              "Basketball - Israel Super League": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=43ee2dc0-6bfd-4f81-b7b5-43e9a07af4e2",
                              "Basketball - Brazil NBB": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=4ca3ff89-cfe9-430e-b441-4a1d4f645db5",
                              "Basketball - Argentia Liga Nacional De Basquetbol": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=348b827c-2bc6-475d-b2cc-1f76964366d1",
                              "Basketball - Australia NBL" :"https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=72c1cde6-400d-4ffc-877a-c8f47bb8dd0a",
                              "Basketball - Athletes Unlimited": "https://sportsbook.caesars.com/us/pa/bet/basketball/events/all?id=e1609f3d-64cf-4a4b-ba5f-2b5b33ccfe46",
                              "Hockey - NHL": "https://sportsbook.caesars.com/us/pa/bet/icehockey?id=b7b715a9-c7e8-4c47-af0a-77385b525e09",
                              "Hockey - NCAA": "https://sportsbook.caesars.com/us/pa/bet/icehockey/events/all?id=726c21e9-e9f7-433b-9f4f-27e80bc0228f",
                              "Hockey - Czech Republic ExtraLiga": "https://sportsbook.caesars.com/us/pa/bet/icehockey/events/all?id=bfd1a683-445c-4e4c-b1a4-0bcc002ef5c5",
                              "Hockey - Finland Liiga": "https://sportsbook.caesars.com/us/pa/bet/icehockey/events/all?id=fc4c833a-9fa3-4078-b75c-9404601c66a1",
                              "Hockey - Sweden SHL": "https://sportsbook.caesars.com/us/pa/bet/icehockey/events/all?id=8b16f227-9840-4a42-bc2a-55d84da1371d",
                              "Lacrosse - NCAA": "https://sportsbook.caesars.com/us/pa/bet/lacrosse/events/all?id=ddfc6382-8dde-4efa-99bc-8f823fa1623e"
                              }
        self.output = {}
        self.extractor = CaesarsDataExtractor()

    def _initialize_driver(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = WebDriver(options=options)
        return driver

    def scrape_data(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(10)
    
        for key, val in self.valid_sports.items():
            try:
                self.driver.get(val)
                time.sleep(0.5)
                self.scroll_down()
                betting_card = self.driver.find_element("xpath", ".//div[@class='eventList']")
                data = [betting_card.get_attribute("innerHTML")]
                sport = [key]
                sport, games = self.extractor.extract_data(sport, data)
                self.output[sport] = games
            except:
                print(val)
        return self.output
    def scroll_down(self):
        """A method for scrolling the page."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.1)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight-1500);")
            time.sleep(.1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(.3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def close_driver(self):
        self.driver.quit()

class CaesarsParser:
    @staticmethod
    def parse_spread_odds(input_string):
        pattern = re.compile(r'([+-]?\d*\.?\d+)([+-−]\d+)?')
        match = pattern.match(input_string)
        if match:
            return [match.group(1), match.group(2)]
        else:
            return [None, None]

    @staticmethod
    def parse_total_odds(input_string):

        if input_string == None:
            return [None, None, None]
        input_string = input_string.get("aria-label")

        pattern = re.compile(r'.*?odds at ([+\-]\d+) with a (\d+\.*\d+) (under|over)')

        match = pattern.match(input_string)

        if match and match != "":
            odds, number, bet_type = match.groups()
            
            odds = odds
            
            number = number
            
            return ['U' if bet_type == 'under' else 'O', number, odds]
        else:
            return [None,None,None]

    @staticmethod
    def custom_selector(tag):
        return (
            tag.name == "div" and tag.has_attr("class") and "header selectionHeader truncate3Rows col" in " ".join(tag.get("class"))
        )or (
            tag.name == "a" and tag.has_attr("class") and "competitor" in tag.get("class")
        ) or (
            tag.name == "div" and tag.has_attr("class") and "selectionContainer" in tag.get("class")
        ) or (
            tag.name == "div" and tag.has_attr("class") and "dateContainer" in tag.get("class")
        ) 

class CaesarsDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}
        
        
        for j in range(len(sports_list)):
            try:
                soup = BeautifulSoup(sports_html[j], 'html.parser')
                curr_date = "Today"
                information_elements = soup.find_all(CaesarsParser.custom_selector)
                games = {}
                
                i = 0
                while i < len(information_elements):
                    line = information_elements[i].text
                    
                    months = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}
                    if line[:3] in months:
                        curr_date = line
                    else:
                        curr_date = "LIVE"

                    team1 = re.sub(r"[0-9]", "",information_elements[i + 1].text)
                    team2 = re.sub(r"[0-9]", "",information_elements[i + 2].text)
                    operations = {}
                    for index in range(3, 10,3):
                        operations[information_elements[i + index].text.replace(" Live", "").replace(" ", "")] = index//3 - 1
                    try:
                        moneyline_odds1 = information_elements[i + operations["MoneyLine"]*3+4].text
                        moneyline_odds2 = information_elements[i + operations["MoneyLine"]*3+5].text
                    except:
                        moneyline_odds1 = information_elements[i + operations["Money"]*3+4].text
                        moneyline_odds2 = information_elements[i + operations["Money"]*3+5].text 


                    spread_odds1 = CaesarsParser.parse_spread_odds(information_elements[i + operations["Spread"]*3+4].text)
                    spread_odds2 = CaesarsParser.parse_spread_odds(information_elements[i + operations["Spread"]*3+5].text)
                    total_odds1 = CaesarsParser.parse_total_odds(information_elements[i + operations["TotalPoints"]*3+4].find('button', {'aria-label': lambda x: x and 'odds at' in x}))
                    total_odds2 = CaesarsParser.parse_total_odds(information_elements[i + operations["TotalPoints"]*3+5].find('button', {'aria-label': lambda x: x and 'odds at' in x}))
                    
                    game = format_json(spread_odds1=spread_odds1, spread_odds2=spread_odds2,
                                    moneyline_odds1=moneyline_odds1, moneyline_odds2=moneyline_odds2,
                                    total_odds1=total_odds1, total_odds2=total_odds2,
                                    bookmaker="caesars")  
                    curr_date = standardize_date(curr_date.replace("|",""))
                    if curr_date not in games:
                        games[curr_date] = {}
                    games[curr_date]["{} vs. {}".format(team1, team2)] = game

                    i+=12

                return sports_list[j], games
            except:
                print(sports_list[j])

    def run(self):
        url = "https://sportsbook.caesars.com/us/pa/bet/"
        scraper = CaesarsScraper()
        data = scraper.scrape_data(url)
       
        return data