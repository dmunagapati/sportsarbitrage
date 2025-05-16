from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from date_parsing import standardize_date
from json_formater import format_json

class ESPNScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.valid_sports = { "Football - NFL": "https://espnbet.com/sport/football/organization/united-states/competition/nfl", 
                              "Basketball - NBA": "https://espnbet.com/sport/basketball/organization/united-states/competition/nba",
                              #"Basketball - NCAAM" : "https://espnbet.com/sport/basketball/organization/united-states/competition/ncaab",
                              "Basketball - WNCAAB": "https://espnbet.com/sport/basketball/organization/united-states/competition/wncaab/section/lines",
                              "Basketball - Argentina Liga Nacional De Basquetbol": "https://espnbet.com/sport/basketball/organization/argentina/competition/liga-a",
                              "Basketball - Australia NBL":"https://espnbet.com/sport/basketball/organization/australia/competition/nbl",
                              "Basketball - China WBA":"https://espnbet.com/sport/basketball/organization/china/competition/wcba",
                              "Basketball - Czech Republic NBL": "https://espnbet.com/sport/basketball/organization/czech-republic/competition/nbl",
                              "Basketball - EuroLeague": "https://espnbet.com/sport/basketball/organization/europe/competition/euroleague",
                              "Basketball - Denmark Basketligaen": "https://espnbet.com/sport/basketball/organization/denmark/competition/basketligaen-den",
                              "Basketball - Europe Adriatic League": "https://espnbet.com/sport/basketball/organization/europe/competition/adriatic-league",
                              "Basketball - Greece A1": "https://espnbet.com/sport/basketball/organization/greece/competition/a1",
                              "Basketball - Israel Super League": "https://espnbet.com/sport/basketball/organization/israel/competition/super-league",
                              "Basketball - Italy Serie A": "https://espnbet.com/sport/basketball/organization/italy/competition/serie-a",
                              "Basketball - Lithuania LKL": "https://espnbet.com/sport/basketball/organization/lithuania/competition/lkl",
                              "Basketball - Romania Liga Nationala": "https://espnbet.com/sport/basketball/organization/romania/competition/liga-nationala",
                              "Basketball - Serbia SuperLeague": "https://espnbet.com/sport/basketball/organization/serbia/competition/super-league",
                              "Basketball - Sweden Basketligan": "https://espnbet.com/sport/basketball/organization/sweden/competition/basketligan",
                              "Baseball - CWS": "https://espnbet.com/sport/baseball/organization/united-states/competition/ncaa",
                              "Hockey - NHL": "https://espnbet.com/sport/hockey/organization/united-states/competition/nhl",
                              "Hockey - NCAA": "https://espnbet.com/sport/hockey/organization/united-states/competition/ncaa",
                              "Hockey - Austria Ice Hockey League": "https://espnbet.com/sport/hockey/organization/austria/competition/ice-hockey-league",
                              "Hockey - Finland Liiga": "https://espnbet.com/sport/hockey/organization/finland/competition/liiga",
                              "Hockey - Sweden SHL": "https://espnbet.com/sport/hockey/organization/sweden/competition/shl",
                              "Rugby - NRL": "https://espnbet.com/sport/rugby-league/organization/australia/competition/nrl",
                              "Rugby - European Champions Cup": "https://espnbet.com/sport/rugby-union/organization/europe/competition/champions-cup",
                              "Rugby - France D2": "https://espnbet.com/sport/rugby-union/organization/france/competition/pro-d2",
                              "Rugby - France Top 14": "https://espnbet.com/sport/rugby-union/organization/france/competition/top-14",
                              "Rugby - Six Nations": "https://espnbet.com/sport/rugby-union/organization/international/competition/six-nations-championship",
                              "Rugby - 7s World Series":"https://espnbet.com/sport/rugby-union/organization/international/competition/svns-series",
                              "Rugby - 7s World Series (W)": "https://espnbet.com/sport/rugby-union/organization/international/competition/svns-series-women",
                              "Rugby - Major League Rugby": "https://espnbet.com/sport/rugby-union/organization/united-states/competition/mlr"
                              }
        self.output = {}
        self.extractor = ESPNDataExtractor()

    def _initialize_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        driver = WebDriver(options=options)
        return driver
    


    def scrape_data(self):
        self.driver.implicitly_wait(10)

        for key, val in self.valid_sports.items():
            try:
                self.driver.get(val)
                betting_card = self.driver.find_element("xpath", ".//div[@data-testid='marketplace-shelf-']")
                data = [betting_card.get_attribute("innerHTML")]
                sport = [key]
                sport, games = self.extractor.extract_data(sport, data)
                self.output[sport] = games
            except:
                print(val)
        return self.output

    def close_driver(self):
        self.driver.quit()

class ESPNParser:
    @staticmethod
    def parse_spread_odds(input_string):
        if input_string == "--":
            return [None,None]
        pattern = r'([-+]?\d*\.?\d+)'

        # Use re.findall to extract all matches
        matches = re.findall(pattern, input_string)
        if matches:
            score = matches[0]
            odds = matches[1]
            return [score, odds]
        else:
            return [None, None]

    @staticmethod
    def parse_total_odds(input_string):
        if input_string == "--":
            return [None, None, None]
            
        pattern = r'([UO])\s?(\d+\.\d+)([+-]\d+)'

        match = re.match(pattern, input_string)

        if match:
            groups = match.groups()
            return list(groups)
        else:
            return [None, None, None]


    @staticmethod
    def parse_money_line_odds(input_string):
        if input_string == "--":
            return None
        return input_string

    

    @staticmethod
    def parse_team_names(input_string):
        pattern = re.compile(r'\d|-')
        match = pattern.sub("", input_string)
        return match.strip()
    

    @staticmethod
    def custom_selector(tag):
        return (
             tag.name == "button" and tag.has_attr("data-testid") and "navigate-to-matchup-btn" in " ".join(tag.get("data-testid"))
        ) or (
             tag.name == "div" and tag.has_attr("class") and "text-primary text-description text-primary" in " ".join(tag.get("class"))
        ) or (
             tag.name == "button" and tag.has_attr("class") and "flex w-full items-center justify-between pr-4 pt-2 text-left" not in " ".join(tag.get("class"))
        )

class ESPNDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}
        for j in range(len(sports_list)):
            try:
                soup = BeautifulSoup(sports_html[j], 'html.parser')
                curr_date = "Today"

                information_elements = soup.find_all(ESPNParser.custom_selector)
                games = {}
                i = 0
                while i < len(information_elements):
                    line = information_elements[i].text
                    if "Live" in line:
                        curr_date = "LIVE"
                    else:
                        curr_date = line

                    team1 = information_elements[i + 1].text
                    team2 = information_elements[i + 5].text

                    spread_odds1 = ESPNParser.parse_spread_odds(information_elements[i + 2].text.replace("Even", "+100"))
                    spread_odds2 = ESPNParser.parse_spread_odds(information_elements[i + 6].text.replace("Even", "+100"))

                    
                    total_odds1 = ESPNParser.parse_total_odds(information_elements[i + 3].text.replace("Even", "+100"))
                    total_odds2 = ESPNParser.parse_total_odds(information_elements[i + 7].text.replace("Even", "+100"))
                    moneyline_odds1 =  ESPNParser.parse_money_line_odds(information_elements[i + 4].text.replace("Even", "+100"))
                    moneyline_odds2 = ESPNParser.parse_money_line_odds(information_elements[i + 8].text.replace("Even", "+100"))
                    game = format_json(spread_odds1=spread_odds1, spread_odds2=spread_odds2,
                                    moneyline_odds1=moneyline_odds1, moneyline_odds2=moneyline_odds2,
                                    total_odds1=total_odds1, total_odds2=total_odds2,
                                    bookmaker="espn")  
                    curr_date = standardize_date(curr_date.replace("·",""))
                    if curr_date not in games:
                        games[curr_date] = {}
                    games[curr_date]["{} vs. {}".format(team1, team2)] = game

                        
                    i+=9
                return sports_list[j], games
            except:
                print(sports_list[j])

    def run(self):
        scraper = ESPNScraper()
        data = scraper.scrape_data()
        return data
