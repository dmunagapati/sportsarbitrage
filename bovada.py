from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from date_parsing import standardize_date
from json_formater import format_json

class BovadaScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.valid_sports = { "Football - NFL": "https://www.bovada.lv/sports/football/nfl", 
                              "Basketball - NBA": "https://www.bovada.lv/sports/basketball/nba",
                              #"Basketball - NCAAM" : "https://www.bovada.lv/sports/basketball/college-basketball",
                              "Basketball - Australia NBL": "https://www.bovada.lv/sports/basketball/asia/australia/nbl",
                              "Basketball - Argentina Liga Nacional De Basquetbol": "https://www.bovada.lv/sports/basketball/americas/argentina/liga-nacional-de-basquet",
                              "Basketball - Brazil NBB": "https://www.bovada.lv/sports/basketball/americas/brazil/nbb",
                              "Basketball - China WBA":"https://www.bovada.lv/sports/basketball/asia/china/wcba-women",
                              "Basketball - Iran D1": "https://www.bovada.lv/sports/basketball/asia/iran/division-1",
                              "Basketball - Poland 1 Liga": "https://www.bovada.lv/sports/basketball/europe/poland/1-liga",
                              "Basketball - Poland Basket Liga": "https://www.bovada.lv/sports/basketball/europe/poland/orlen-basket-liga",
                              "Basketball - Korea Basketball League":"https://www.bovada.lv/sports/basketball/asia/south-korea/kbl",
                              "Hockey - NHL": "https://www.bovada.lv/sports/hockey/nhl",
                              "Hockey - Canada WHL": "https://www.bovada.lv/sports/hockey/canada/whl",
                              "Hockey - Austria Ice Hockey League": "https://www.bovada.lv/sports/hockey/europe/austria/ehl",
                              "Hockey - Belarus Extraliga": "https://www.bovada.lv/sports/hockey/europe/belarus/extraliga",
                              "Hockey - Czech Republic 1st Liga": "https://www.bovada.lv/sports/hockey/europe/czech-republic/1st-liga",
                              "Hockey - Demark Metal Ligaen": "https://www.bovada.lv/sports/hockey/europe/denmark/superisligaen",
                              "Hockey - England Elite League": "https://www.bovada.lv/sports/hockey/europe/england/elite-league",
                              "Hockey - Finland Liiga": "https://www.bovada.lv/sports/hockey/europe/finland/liiga",
                              "Hockey - Finaland Mestis": "https://www.bovada.lv/sports/hockey/europe/finland/mestis",
                              "Hockey - Hungary Erste Liga": "https://www.bovada.lv/sports/hockey/europe/hungary/erste-liga",
                              "Hockey - Latvia LHL": "https://www.bovada.lv/sports/hockey/europe/latvia/latvian-hockey-league",
                              "Hockey - Sweden Allsvenskan": "https://www.bovada.lv/sports/hockey/europe/sweden/allsvenskan",
                              "Hockey - Sweden SDLH (W)": "https://www.bovada.lv/sports/hockey/europe/sweden/sdhl-women",
                              "Hockey - Czech Republic ExtraLiga":" https://www.bovada.lv/sports/hockey/europe/czech-republic/extraliga",
                              "Hockey - Sweden SHL": "https://www.bovada.lv/sports/hockey/europe/sweden/shl",
                              "Hockey - Switzerland NLA": "https://www.bovada.lv/sports/hockey/europe/switzerland/national-league",
                              "Hockey - NCAA": "https://www.bovada.lv/sports/hockey/united-states/ncaa-hockey",
                              "Hockey - AHL": "https://www.bovada.lv/sports/hockey/united-states/ahl",
                              "Baseball - MLB Preseason": "https://www.bovada.lv/sports/baseball/mlb-spring-training",
                              "Football - Aussie AFL": "https://www.bovada.lv/sports/aussie-rules/afl",
                              "Darts - Premier League": "https://www.bovada.lv/sports/darts/premier-league-2024",
                              "Darts - Modus Super Series": "https://www.bovada.lv/sports/darts/online-live-league",
                              "Esports - Call of Duty League": "https://www.bovada.lv/sports/esports/call-of-duty/cdl-major-2",
                              "Esports - Counter Strike 2 Blast Premier Spring": "https://www.bovada.lv/sports/esports/counter-strike-2",
                              "Esports - ESL Challenger League ": "https://www.bovada.lv/sports/esports/counter-strike-2/esl-challenger-league",
                              "Esports - League of Legends LCK Challenger Leageue": "https://www.bovada.lv/sports/esports/league-of-legends/lck-challenger-spring",
                              "Esports - League of Legends LCS Spring": "https://www.bovada.lv/sports/esports/league-of-legends/lcs-spring",
                              "Esports - League of Legends LCK Spring": "https://www.bovada.lv/sports/esports/league-of-legends/lck-spring",
                              "Esports - League of Legends LDL 2024": "https://www.bovada.lv/sports/esports/league-of-legends/ldl-2024",
                              "Esports - Rainbow Six Malta Cyber Series": "https://www.bovada.lv/sports/esports/rainbow-six/malta-cyber-series-vii/futures-odd",
                              "Rugby - NRL": "https://www.bovada.lv/sports/rugby-league/nrl",
                              "Rugby - Super League": "https://www.bovada.lv/sports/rugby-league/super-league",
                              "Table Tennis - Czech Republic Pro League": "https://www.bovada.lv/sports/table-tennis/additional-table-tennis/czech-republic/pro-league",
                              "Volleyball - Italy Super Lega": "https://www.bovada.lv/sports/volleyball/italy/italy-superlega",
                              "Volleyball - Brazil Super Liga": "https://www.bovada.lv/sports/volleyball/brazil/brazil-superliga",
                              "Volleyball - Brazil Super Liga (W)": "https://www.bovada.lv/sports/volleyball/brazil/brazil-superliga-women",
                              "Volleyball - Italy A1 (W)": "https://www.bovada.lv/sports/volleyball/italy/italy-a1-women",
                              "Volleyball - Poland Plus Liga": "https://www.bovada.lv/sports/volleyball/poland/poland-plus-liga",
                              "Volleyball - Turkey Efeler League": "https://www.bovada.lv/sports/volleyball/turkey/efeler-league"
                              }
        self.output = {}
        self.extractor = BovadaDataExtractor()

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
                betting_card = self.driver.find_element("xpath", ".//div[@class='bucket__collapsableSection']")
                data = [betting_card.get_attribute("innerHTML")]
                sport = [key]
                sport, games = self.extractor.extract_data(sport, data)
                self.output[sport] = games
            except:
                print(val)
        return self.output
    
    def close_driver(self):
        self.driver.quit()

class BovadaParser:
    @staticmethod
    def parse_spread_odds(input_string):

        pattern = r'([-+]?\d+(\.\d+)?)\s*\(([-+]?\w+|\d+)\)\s*([-+]?\d+(\.\d+)?)\s*\(([-+]?\w+|\d+)\)'

        matches = re.match(pattern, input_string)   

        if matches:
            score1 = matches.group(1)
            odds1 = matches.group(3)
            score2 = matches.group(4)
            odds2 = matches.group(6)
            return [score1, odds1], [score2, odds2]
        else:
            return [None, None], [None, None]

    @staticmethod
    def parse_total_odds(input_string):

        pattern = r'([OU])\s*([\d.]+)\s*\(([-+]?\w+)\)\s*([OU])\s*([\d.]+)\s*\(([-+]?\w+)\)'

        matches = re.match(pattern, input_string)

        if matches:
            team1_dir, team1_stake, team1_odds, team2_dir, team2_stake, team2_odds, = matches.groups()
            team1 = [team1_dir, team1_stake, team1_odds,]
            team2 = [team2_dir, team2_stake, team2_odds,]
            if None in team1:
                team1 = [None for i in range(3)]
            if None in team2:
                team2 = [None for i in range(3)]
            return team1, team2
        else:
            return [None for i in range(3)], [None for i in range(3)]


    @staticmethod
    def parse_money_line_odds(input_string):
        pattern = r'\s*([-+]?\d+(\.\d+)?)\s*([-+]?\d+(\.\d+)?)\s*'
        matches = re.match(pattern, input_string)
        if matches:
            odds1 = matches.group(1)
            odds2 = matches.group(3)
            return odds1, odds2
        else:
            return None, None

    

    @staticmethod
    def parse_team_names(input_string):
        pattern = re.compile(r'\d|-')
        match = pattern.sub("", input_string)
        return match.strip()
    

    @staticmethod
    def custom_selector(tag):
        return (
             tag.name == "sp-score-coupon" and tag.has_attr("class") and "scores" in " ".join(tag.get("class"))
        ) or (
             tag.name == "h4" and tag.has_attr("class") and "competitor-name" in " ".join(tag.get("class"))
        ) or (
             tag.name == "sp-outcomes" and tag.has_attr("class") and "markets-container" in " ".join(tag.get("class"))
        )

class BovadaDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}

        for j in range(len(sports_list)):
            try:
                soup = BeautifulSoup(sports_html[j], 'html.parser')
                curr_date = "Today"
                information_elements = soup.find_all(BovadaParser.custom_selector)
                games = {}
                
                i = 0
                while i < len(information_elements):
                    curr_date = information_elements[i].text
                    
                    team1 = information_elements[i + 1].text
                    team2 = information_elements[i + 2].text
                    score_box = information_elements[i+3]
                    div_tag = score_box.findChildren("ul")
                    odds = []
                    for item in div_tag:
                        if item.has_attr('class') or item.text == "":
                            odds.append("")
                        else:
                            odds.append(item.text.replace("EVEN", "+100"))
                    
                    spread_odds1, spread_odds2 = BovadaParser.parse_spread_odds(odds[0])
                    total_odds1, total_odds2 = BovadaParser.parse_total_odds(odds[2])
                    moneyline_odds1, moneyline_odds2 = BovadaParser.parse_money_line_odds(odds[1])

                    
                    game = format_json(spread_odds1=spread_odds1, spread_odds2=spread_odds2,
                                    moneyline_odds1=moneyline_odds1, moneyline_odds2=moneyline_odds2,
                                    total_odds1=total_odds1, total_odds2=total_odds2,
                                    bookmaker="bovada")  
                    curr_date = standardize_date(curr_date)
                    if curr_date not in games:
                        games[curr_date] = {}
                    games[curr_date]["{} vs. {}".format(team1, team2)] = game

                    i+=4
                return sports_list[j], games
            except:
                print(sports_list[j])

    def run(self):
        scraper = BovadaScraper()
        data = scraper.scrape_data()
        return data
