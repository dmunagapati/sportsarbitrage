from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from date_parsing import standardize_date
import time

from json_formater import format_json
class PinnacleScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.valid_sports = { "Football - NFL": "https://www.pinnacle.com/en/football/nfl/matchups", 
                              "Basketball - NBA": "https://www.pinnacle.com/en/basketball/nba/matchups",
                              #"Basketball - NCAAM" : "https://www.pinnacle.com/en/basketball/ncaa/matchups",
                              "Basketball - Europe Adriatic League": "https://www.pinnacle.com/en/basketball/aba-adriatic-league/matchups",
                              "Basketball - Albania Superleague": "https://www.pinnacle.com/en/basketball/albania-superleague/matchups",
                              "Basketball - Argentina Torneo Federal": "https://www.pinnacle.com/en/basketball/argentina-torneo-federal/matchups",
                              "Basketball - Argentina LLF Women Betting": "https://www.pinnacle.com/en/basketball/argentina-llf-women/matchups",
                              "Basketball - Argentina Liga de Basquetbol": "https://www.pinnacle.com/en/basketball/argentina-llf-women/matchups",
                              "Basketball - Argentina Liga Nacional de Basquetbol": "https://www.pinnacle.com/en/basketball/argentina-liga-nacional/matchups",
                              "Basketball - Australia WNBL": "https://www.pinnacle.com/en/basketball/australia-wnbl/matchups",
                              "Basketball - Australia NBL": "https://www.pinnacle.com/en/basketball/australia-nbl/matchups",
                              "Basketball - Austria SuperLiga": "https://www.pinnacle.com/en/basketball/austria-superliga/matchups",
                              "Basketball - Brazil NBB": "https://www.pinnacle.com/en/basketball/brazil-novo-basquete-brasil/matchups",
                              "Basketball - Chile LNB": "https://www.pinnacle.com/en/basketball/chile-lnb/matchups",
                              "Basketball - China WBA":"https://www.pinnacle.com/en/basketball/china-wcba-women/matchups",
                              "Basketball - China Taipei SBL": "https://www.pinnacle.com/en/basketball/chinese-taipei-sbl/matchups",
                              "Basketball - China Taipei WSBL": "https://www.pinnacle.com/en/basketball/chinese-taipei-wsbl-women/matchups",
                              "Basketball - Croatia A1 League": "https://www.pinnacle.com/en/basketball/croatia-a1-liga/matchups",
                              "Basketball - Czech Republic ZBL": "https://www.pinnacle.com/en/basketball/czech-republic-zbl-women/matchups",
                              "Basketball - Czech Republic NBL": "https://www.pinnacle.com/en/basketball/czech-republic-nbl/matchups",
                              "Basketball - Czech Republic 1st Liga": "https://www.pinnacle.com/en/basketball/czech-republic-1-liga/matchups",
                              "Basketball - Demark Basketligaen": "https://www.pinnacle.com/en/basketball/denmark-basketligaen/matchups",
                              "Basketball - British BBL": "https://www.pinnacle.com/en/basketball/england-bbl-championship/matchups",
                              "Basketball - Estonia Latvian Basketball League": "https://www.pinnacle.com/en/basketball/estonian-latvian-basketball-league/matchups",
                              "Basketball - EuroLeague": "https://www.pinnacle.com/en/basketball/europe-euroleague/matchups",
                              "Basketball - Finland D1":"https://www.pinnacle.com/en/basketball/finland-division-1/matchups",
                              "Basketball - Finland Korisliiga": "https://www.pinnacle.com/en/basketball/finland-korisliiga/matchups",
                              "Basketball - France Champ B": "https://www.pinnacle.com/en/basketball/france-championnat-pro-b/matchups",
                              "Basketball - Germany Pro A": "https://www.pinnacle.com/en/basketball/germany-pro-a/matchups",
                              "Basketball - Germany A1": "https://www.pinnacle.com/en/basketball/greece-a1/matchups",
                              "Basketball - Iceland Premier League": "https://www.pinnacle.com/en/basketball/iceland-premier-league/matchups/",
                              "Basketball - Indonesia Basketball League": "https://www.pinnacle.com/en/basketball/indonesia-basketball-league/matchups/",
                              "Basketball - Israel National League": "https://www.pinnacle.com/en/basketball/israel-national-league/matchups",
                              "Basketball - Israel Super League": "https://www.pinnacle.com/en/basketball/israel-premier-league/matchups",
                              "Basketball - Italy Serie A2": "https://www.pinnacle.com/en/basketball/italy-serie-a2/matchups/",
                              "Basketball - Japan B3 League": "https://www.pinnacle.com/en/basketball/japan-b3-league/matchups",
                              "Basketball - Japan B2 League": "https://www.pinnacle.com/en/basketball/japan-b2-league/matchups",
                              "Basketball - Japan WJB League": "https://www.pinnacle.com/en/basketball/japan-wjb-league-women/matchups",
                              "Basketball - Lebanon LBL": "https://www.pinnacle.com/en/basketball/lebanon-lebanese-basketball-league/matchups",
                              "Basketball - Lithuania NBL": "https://www.pinnacle.com/en/basketball/lithuania-national-basketball-league/matchups",
                              "Basketball - Lithuania LKL": "https://www.pinnacle.com/en/basketball/lithuania-lietuvos-krepsinio-lyga/matchups",
                              "Basketball - Poland Basket Liga": "https://www.pinnacle.com/en/basketball/poland-basket-liga/matchups",
                              "Basketball - Poland 1 Liga": "https://www.pinnacle.com/en/basketball/poland-1-liga/matchups",
                              "Basketball - Spain LEB": "https://www.pinnacle.com/en/basketball/spain-leb-gold/matchups",
                              "Basketball - Sweden Basketligan (W)": "https://www.pinnacle.com/en/basketball/sweden-basketligan-women/matchups",
                              "Basketball - Sweden Basketligan": "https://www.pinnacle.com/en/basketball/sweden-basketligan/matchups",
                              "Basketball - Switzerland LNA": "https://www.pinnacle.com/en/basketball/switzerland-lna/matchups/",
                              "Basketball - Turkey BSL": "https://www.pinnacle.com/en/basketball/turkey-super-league/matchups",
                              "Basketball - Turkey TBL": "https://www.pinnacle.com/en/basketball/turkey-tbl-first-league/matchups",
                              "Basketball - Turkey TKBL (W)": "https://www.pinnacle.com/en/basketball/turkey-tkbl-women/matchups",
                              "Basketball - WNCAAB": "https://www.pinnacle.com/en/basketball/wncaa/matchups"
                              }
        self.output= {}
        self.extractor = PinnacleDataExtractor()

    def _initialize_driver(self):
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('start-maximized')

        options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = WebDriver(options=options)
        return driver
    


    def scrape_data(self):
        self.driver.implicitly_wait(10)

        for key, val in self.valid_sports.items():
            try:
                self.driver.get(val)
                time.sleep(10)
                betting_card = self.driver.find_element("xpath","//div[@class='style_container__2aQG5']")
                data = [betting_card.get_attribute("innerHTML")]
                sport = [key]
                sport, games = self.extractor.extract_data(sport, data)
                self.output[sport] = games
            except:
                print(val)
        return self.output

    def close_driver(self):
        self.driver.quit()

class PinnacleParser:
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
            return groups
        else:
            return [None, None, None]


    @staticmethod
    def parse_money_line_odds(input_string):
        if input_string == "--":
            return None

    

    @staticmethod
    def parse_team_names(input_string):
        pattern = re.compile(r'\d|-')
        match = pattern.sub("", input_string)
        return match.strip()
    

    @staticmethod
    def custom_selector(tag):
        return (
             tag.name == "div" and tag.has_attr("class") and "ellipsis style_gameInfoLabel__2m_fI" in " ".join(tag.get("class"))
        ) or (
            tag.name == "div" and tag.has_attr("class") and "contentBlockHeading borderGreen style_header__3JCuz" in " ".join(tag.get("class"))
        )or (
            tag.name == "div" and tag.has_attr("class") and "style_dateBar__1adEH" in " ".join(tag.get("class"))
        ) or (
           tag.name == "span" and tag.has_attr("class") and "style_label__3BBxD"  in " ".join(tag.get("class"))
        )or (
            tag.name == "span" and tag.has_attr("class") and "style_price__3Haa9"  in " ".join(tag.get("class"))
        )or (
            tag.name == "button" and tag.has_attr("class") and "market-btn style_button__G9pbN style_pill__2U30o style_vertical__2J4sL style_disabled__wy6pl" in " ".join(tag.get("class"))
        ) or (
            tag.name == "div" and tag.has_attr("class") and "style_matchupDate__UG-mT" in tag.get("class")
        )
    @staticmethod
    def decimal_to_american(decimal_odds):
        try:
            decimal_odds = float(decimal_odds)
        
            if decimal_odds >= 2.0:
                american_odds = int((decimal_odds - 1) * 100)
                return f"+{american_odds}"
            else:
                american_odds = int(-100 / (decimal_odds - 1))
                return f"{american_odds}"
        except:
            return "Market Offline"



class PinnacleDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}
        for j in range(len(sports_list)):
            try:
                soup = BeautifulSoup(sports_html[j], 'html.parser')
                curr_date = "Today"
                information_elements = soup.find_all(PinnacleParser.custom_selector)
                games = {}
                i = 0
                while i < len(information_elements):
                    flag = False
                    line = information_elements[i].text
                    for d in {"Today", "Tomorrow", "Jan ", "Feb", "Mar ", "Apr ", "May ", "Jun ", "Jul ","Aug ", 
                            "Sep ", "Oct ","Nov ","Dec ", "Live"}:
                        if d in line:
                            curr_date = line
                            flag = True
                            break     
                    if flag:
                        i+=1
                        continue
                    team1 = information_elements[i].text
                    team2 = information_elements[i + 1].text
                    time = information_elements[i+2].text
                    spread_odds1 = [information_elements[i +3].text, 
                                    PinnacleParser.decimal_to_american(information_elements[i + 4].text)]
                    if spread_odds1[0] == "Market Offline":
                        spread_odds1 = [None, None]
                        i-=1

                    spread_odds2 = [information_elements[i + 5].text, 
                                    PinnacleParser.decimal_to_american(information_elements[i + 6].text)]
                    if spread_odds2[0] == "Market Offline":
                        spread_odds2 = [None, None]
                        i-=1

                    moneyline_odds1 = PinnacleParser.decimal_to_american(information_elements[i + 7].text)
                    if moneyline_odds1 == "Market Offline":
                        moneyline_odds1 = None

                    moneyline_odds2 = PinnacleParser.decimal_to_american(information_elements[i + 8].text)
                    if moneyline_odds2 == "Market Offline":
                        moneyline_odds2 = None
                    

                    total_odds1 = ["O", information_elements[i + 9].text, 
                                PinnacleParser.decimal_to_american(information_elements[i + 10].text)]
                    if total_odds1[1] == "Market Offline":
                        total_odds1 = [None, None, None]
                        i-=1

                    total_odds2 = ["U", information_elements[i + 11].text, 
                                PinnacleParser.decimal_to_american(information_elements[i + 12].text)]
                    if total_odds2[1] == "Market Offline":
                        total_odds2 = [None, None, None]
                        i-=1
                    
                    game = format_json(spread_odds1=spread_odds1, spread_odds2=spread_odds2,
                                    moneyline_odds1=moneyline_odds1, moneyline_odds2=moneyline_odds2,
                                    total_odds1=total_odds1, total_odds2=total_odds2,
                                    bookmaker="pinnacle")  
                    curr_date = standardize_date(curr_date, time)
                    if curr_date not in games:
                        games[curr_date] = {}
                    games[curr_date]["{} vs. {}".format(team1, team2)] = game

                    i+=13
                return sports_list[j], games
            except:
                print(sports_list[j])

    def run(self):
        scraper = PinnacleScraper()
        data = scraper.scrape_data()
        return data
