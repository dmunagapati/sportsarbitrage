from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from date_parsing import standardize_date
from json_formater import format_json
import time

class MGMScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.valid_sports = { "Football - NFL": "https://sports.nj.betmgm.com/en/sports/football-11/betting/usa-9/nfl-35", 
                              "Basketball - NBA": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/usa-9/nba-6004",
                              #"Basketball - NCAAM" : "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/usa-9/college-264",
                              "Basketball - WNCAAB": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/usa-9/college-women-5241",
                              "Basketball - China WBA": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/china-57/women-s-chinese-basketball-association-32406",
                              "Basketball - Israel Super League": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/israel-62/premier-league-3705",
                              "Basketball - Argentina Liga Nacional De Basquetbol": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/argentina-38/liga-nacional-4980",
                              "Basketball - Australia NBL": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/australia-60/nbl-857",
                              "Basketball - Brazil NBB": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/brazil-33/nbb-17287",
                              "Basketball - Korea Basketball League": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/korea-south-198/korean-basketball-league-9235",
                              "Basketball - Lithuania LKL": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/lithuania-151/lkl-league-2317",
                              "Basketball - Sweden Basketligan": "https://sports.nj.betmgm.com/en/sports/basketball-7/betting/sweden-29/basketligan-861"
                              }
        self.output = {}
        self.extractor = MGMDataExtractor()

    def _initialize_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = WebDriver(options=options)
        return driver


    def scrape_data(self):
        self.driver.implicitly_wait(10)

        for key, val in self.valid_sports.items():
            try:
                self.driver.get(val)
                # time.sleep(4)
                # try:
                #     print("TRYING")
                #     more = self.driver.find_element("xpath", "//div[contains(@class, 'grid-footer show-more ng-star-inserted')]")
                #     print("Found")
                #     more.click()
                #     print("CLIKCED")
                #     time.sleep(1200)
                # except:
                #     print("FAILED")
                #     pass
                betting_card = self.driver.find_element("xpath", ".//ms-event-group[contains(@class, 'six-pack-groups event-group')]")
                data = [betting_card.get_attribute("innerHTML")]
                sport = [key]
                sport, games = self.extractor.extract_data(sport, data)
                self.output[sport] = games
            except:
                print(val)
        return self.output
        

    def close_driver(self):
        self.driver.quit()

class MGMParser:
    @staticmethod
    def parse_spread_odds(input_string):
        match = re.findall(r'[-+]?\d*\.?\d+', input_string)
    
        if match and len(match)>3:
            return [match[0], match[1]],  [match[2], match[3]]
        return [None, None], [None, None]

    @staticmethod
    def parse_total_odds(input_string):
        
        if input_string == None or input_string == "":
            return [None for i in range(3)], [None for i in range(3)]
        output = input_string.split(" ")[1:]

        if len(output)<6:
            return [None for i in range(3)], [None for i in range(3)]

        team1_dir, team1_stake, team1_odds, team2_dir, team2_stake, team2_odds = output
        return [team1_dir, team1_stake, team1_odds], [team2_dir, team2_stake, team2_odds]
    @staticmethod
    def parse_money_line_odds(input_string):
        pattern = r'([-+]?\d+)'
        match = re.findall(pattern, input_string)
        if match:
            return match
        return None, None
    

    @staticmethod
    def parse_team_names(input_string):
        pattern = re.compile(r'\d|-')
        match = pattern.sub("", input_string)
        return match.strip()
    

    @staticmethod
    def custom_selector(tag):
        return (
            tag.name == "ms-event-timer"
        )or (
            tag.name == "div" and tag.has_attr("class") and "participant-container" in tag.get("class")
        ) or (
            tag.name == "ms-option-group" and tag.has_attr("class") and "grid-option-group grid-group" in " ".join(tag.get("class"))
        )
    

class MGMDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}

        for j in range(len(sports_list)):
            try:
                curr_date = "Today"
                soup = BeautifulSoup(sports_html[j], 'html.parser')
                information_elements = soup.find_all(MGMParser.custom_selector)

                games = {}
                
                i = 0
                while i < len(information_elements):
                    line = information_elements[i].text
                    dates = {"Today", "Tomorrow", "/"}
                    flag = False
                    for date in dates:
                        if date in line:
                            curr_date = line
                            flag = True
                    if not flag:
                        curr_date = "LIVE"
                    team1 = MGMParser.parse_team_names(information_elements[i + 1].text)
                    team2 = MGMParser.parse_team_names(information_elements[i + 2].text)
                    if team1 == "" or team2 == "":
                        i+=4
                        continue
                    spread_odds1, spread_odds2 = MGMParser.parse_spread_odds(information_elements[i + 3].text)
                    total_odds1, total_odds2 = MGMParser.parse_total_odds(information_elements[i + 4].text)
                    moneyline_odds1, moneyline_odds2 = MGMParser.parse_money_line_odds(information_elements[i + 5].text)

                    game = format_json(spread_odds1=spread_odds1, spread_odds2=spread_odds2,
                                    moneyline_odds1=moneyline_odds1, moneyline_odds2=moneyline_odds2,
                                    total_odds1=total_odds1, total_odds2=total_odds2,
                                    bookmaker="betmgm")
                    curr_date = standardize_date(curr_date.replace("•", ""))
                    if curr_date not in games:
                        games[curr_date] = {}
                    games[curr_date]["{} vs. {}".format(team1, team2)] = game

                    i+=6
                return sports_list[j], games
            except:
                print(sports_list[j])

        return output
    def run(self):
        scraper = MGMScraper()
        data = scraper.scrape_data()
        
        return data
