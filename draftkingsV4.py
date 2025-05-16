from bs4 import BeautifulSoup
import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from date_parsing import standardize_date
from json_formater import format_json
class DraftKingsScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.valid_sports = { "Football - NFL": "https://sportsbook.draftkings.com/leagues/football/nfl", 
                              "Basketball - NBA": "https://sportsbook.draftkings.com/leagues/basketball/nba",
                              #"Basketball - NCAAM" : "https://sportsbook.draftkings.com/leagues/basketball/ncaab",
                              "Hockey - NHL": "https://sportsbook.draftkings.com/leagues/hockey/nhl",
                              "MMA - UFC": "https://sportsbook.draftkings.com/leagues/mma/ufc",
                              "Baseball - CWS": "https://sportsbook.draftkings.com/leagues/baseball/ncaa-baseball",
                              "Baseball - MLB Preseason": "https://sportsbook.draftkings.com/leagues/baseball/mlb-preseason",
                              "Basketball - WNCAAB": "https://sportsbook.draftkings.com/leagues/basketball/wncaab",
                              "Basketball - Argentina Liga Nacional De Basquetbol": "https://sportsbook.draftkings.com/leagues/basketball/argentina---liga-nacional-de-basquetbol",
                              "Basketball - Australia NBL": "https://sportsbook.draftkings.com/leagues/basketball/australia---nbl",
                              "Basketball - BNXT": "https://sportsbook.draftkings.com/leagues/basketball/bnxt-league",
                              "Basketball - Brazil NBB": "https://sportsbook.draftkings.com/leagues/basketball/brazil---nbb",
                              "Basketball - Croatia A1 League": "https://sportsbook.draftkings.com/leagues/basketball/croatia---a1-league",
                              "Basketball - England BBL": "https://sportsbook.draftkings.com/leagues/basketball/british-basketball-league",
                              "Basketball - Finland Korisliiga": "https://sportsbook.draftkings.com/leagues/basketball/finland---korisliiga",
                              "Basketball - France Pro A": "https://sportsbook.draftkings.com/leagues/basketball/france---pro-a",
                              "Basketball - Germany Bundesliga": "https://sportsbook.draftkings.com/leagues/basketball/germany---bundesliga",
                              "Basketball - Iceland Division 1": "https://sportsbook.draftkings.com/leagues/basketball/iceland---division-1",
                              "Basketball - Israel Super League": "https://sportsbook.draftkings.com/leagues/basketball/israel---super-league",
                              "Basketball - Italy Serie A": "https://sportsbook.draftkings.com/leagues/basketball/italy---lega-1",
                              "Basketball - Japan B League": "https://sportsbook.draftkings.com/leagues/basketball/japan---b-league",
                              "Basketball - Korea Basketball League": "https://sportsbook.draftkings.com/leagues/basketball/kbl",
                              "Basketball - Lithuania LKL": "https://sportsbook.draftkings.com/leagues/basketball/lithuania---lkl",
                              "Basketball - Poland Basket Liga": "https://sportsbook.draftkings.com/leagues/basketball/poland---basket-liga",
                              "Basketball - Spain ACB League": "https://sportsbook.draftkings.com/leagues/basketball/spain---acb-league",
                              "Basketball - EuroLeague": "https://sportsbook.draftkings.com/leagues/basketball/euroleague",
                              "Basketball - Serbia SuperLeague": "https://sportsbook.draftkings.com/leagues/basketball/serbia---superleague",
                              "Basketball - Sweden Basketligan": "https://sportsbook.draftkings.com/leagues/basketball/sweden---basketligan",
                              "Basketball - Turkey BSL": "https://sportsbook.draftkings.com/leagues/basketball/turkey---bsl",
                              "Basketball - Turkey BSL (W)": "https://sportsbook.draftkings.com/leagues/basketball/turkey---bsl-women",
                              "Darts - Premier League": "https://sportsbook.draftkings.com/leagues/darts/premier-league",
                              "Darts - Modus Super Series": "https://sportsbook.draftkings.com/leagues/darts/modus-super-series",
                              "Esports - League of Legends Champ Series": "https://sportsbook.draftkings.com/leagues/esports/league-of-legends-championship-series",
                              "Esports - League of Legends European Champ": "https://sportsbook.draftkings.com/leagues/esports/league-of-legends-european-championship",
                              "Esports - Call of Duty League": "https://sportsbook.draftkings.com/leagues/esports/call-of-duty-league",
                              "Esports - Valorant Champions Tour": "https://sportsbook.draftkings.com/leagues/esports/valorant-champions-tour",
                              "Handball - Germany Bundesliga": "https://sportsbook.draftkings.com/leagues/handball/germany-bundesliga",
                              "Handball - Poland Superliga": "https://sportsbook.draftkings.com/leagues/handball/poland-superliga",
                              "Handball - Swedish Elitserien": "https://sportsbook.draftkings.com/leagues/handball/swedish-elitserien",
                              "Hockey - NCAA": "https://sportsbook.draftkings.com/leagues/hockey/ncaa-hockey",
                              "Hockey - Sweden SHL": "https://sportsbook.draftkings.com/leagues/hockey/swedish-hockey-league",
                              "Hockey - Demark Metal Ligaen": "https://sportsbook.draftkings.com/leagues/hockey/denmark-metal-ligaen",
                              "Hockey - Switzerland NLA": "https://sportsbook.draftkings.com/leagues/hockey/swiss-nationalliga",
                              "Lacrosse - NCAA": "https://sportsbook.draftkings.com/leagues/lacrosse/ncaa-lacrosse",
                              "MMA - PFL": "https://sportsbook.draftkings.com/leagues/mma/pfl",
                              "Rugby - NRL": "https://sportsbook.draftkings.com/leagues/rugbyleague/nrl-premiership",
                              "Rugby - Super League": "https://sportsbook.draftkings.com/leagues/rugbyleague/super-league",
                              "Rugby - Major League Rugby": "https://sportsbook.draftkings.com/leagues/rugbyunion/major-league-rugby",
                              "Rugby - France Top 14": "https://sportsbook.draftkings.com/leagues/rugbyunion/france-top-14",
                              "Rugby - 7s World Series": "https://sportsbook.draftkings.com/leagues/rugbyunion/sevens-world-series",
                              "Rugby - 7s World Series (W)": "https://sportsbook.draftkings.com/leagues/rugbyunion/sevens-world-series",
                              "Rugby - European Champions Cup": "https://sportsbook.draftkings.com/leagues/rugbyunion/european-champions-cup",
                              "Rugby - Six Nations": "https://sportsbook.draftkings.com/leagues/rugbyunion/six-nations",
                              "Snooker - World Masters of Snooker": "https://sportsbook.draftkings.com/leagues/snooker/world-masters-of-snooker",
                              "Football - Aussie AFL": "https://sportsbook.draftkings.com/leagues/aussierules/afl"
                              }

        self.extractor = DraftKingsDataExtractor()
        self.output = {}

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
                betting_card = self.driver.find_element("xpath", "//div[@class = 'sportsbook-offer-category-card']")
                data = [betting_card.get_attribute("innerHTML")]
                sport = [key]
                sport, games = self.extractor.extract_data(sport, data)
                self.output[sport] = games
            except:
                print(val)
        return self.output

    def close_driver(self):
        self.driver.quit()

class DraftKingsParser:
    @staticmethod
    def parse_spread_odds(input_string):
        pattern = re.compile(r'([+-]?\d*\.?\d+)([+-−]\d+)?')
        match = pattern.match(input_string)
        if match:
            return [match.group(1), match.group(2)]
        else: return [None, None]

    @staticmethod
    def parse_total_odds(input_string):
        pattern = re.compile(r'([A-Z])\s(\d*\.?\d+)([+-−]\d+)')
        match = pattern.match(input_string)
        if match:
            return [match.group(1), match.group(2), match.group(3)]
        else:
            return [None, None, None]

    @staticmethod
    def custom_selector(tag):
        return (
            tag.name == "div" and tag.has_attr("class") and "event-cell__name-text" in tag.get("class")
        ) or (
            tag.name == "td" and tag.has_attr("class") and "sportsbook-table__column-row" in tag.get("class")
        ) or (
            tag.name == "th" and tag.has_attr("class") and "always-left" in tag.get("class") and "column-header" in tag.get("class")
        ) or (
            tag.name == "div" and tag.has_attr("class") and "event-cell__status event-cell__status__position" in " ".join(tag.get("class"))
        )

            

class DraftKingsDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}
        for j in range(len(sports_list)):
            try:
                soup = BeautifulSoup(sports_html[j], 'html.parser')
                curr_date = "LIVE"
                information_elements = soup.find_all(DraftKingsParser.custom_selector)
                games = {}
                live_flag = False
                i = 0
                while i < len(information_elements):
                    line = information_elements[i].text
                    flag = False
                    if live_flag:
                        curr_date = "Today"
                    live_flag = False
                    for d in {"Today", "Tomorrow", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}:
                        if d in line:
                            curr_date = line
                            flag = True
                            break

                    if flag:
                        i += 1
                        continue
                    time = line 

                    for d in {"HALF", "ND", "RD", "ST", "TH"}:
                        if d in time.upper() or len(time)>8:
                            curr_date = "LIVE"
                            live_flag = True
                            break

                    team1 = information_elements[i + 1].text
                    spread_odds1 = DraftKingsParser.parse_spread_odds(information_elements[i + 2].text)
                    total_odds1 = DraftKingsParser.parse_total_odds(information_elements[i + 3].text)
                    moneyline_odds1 = information_elements[i + 4].text

                    team2 = information_elements[i + 6].text
                    spread_odds2 = DraftKingsParser.parse_spread_odds(information_elements[i + 7].text)
                    total_odds2 = DraftKingsParser.parse_total_odds(information_elements[i + 8].text)
                    moneyline_odds2 = information_elements[i + 9].text
                    game = format_json(spread_odds1=spread_odds1, spread_odds2=spread_odds2,
                                    moneyline_odds1=moneyline_odds1, moneyline_odds2=moneyline_odds2,
                                    total_odds1=total_odds1, total_odds2=total_odds2,
                                    bookmaker="draftkings")  
                    curr_date = standardize_date(curr_date, time)
                    if curr_date not in games:
                        games[curr_date] = {}
                    games[curr_date]["{} vs. {}".format(team1, team2)] = game

                    i += 10
                return sports_list[j], games
            except:
                print(sports_list[j])

    def run(self):
        scraper = DraftKingsScraper()
        data = scraper.scrape_data()
        return data

