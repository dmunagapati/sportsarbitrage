from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

import pyautogui
import undetected_chromedriver as uc
from fake_useragent import UserAgent


class FanDuelScraper:
    def __init__(self, valid_sports):
        self.valid_sports = valid_sports
        self.driver = self._initialize_driver()
        self.sports_list = []
        self.valid_parents = []
        self.sports_html = []

    def _initialize_driver(self):
        options = uc.ChromeOptions()
        #options.add_argument( '--headless=new' )
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--incognito")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--disable-blink-features=AutomationControlled")

        ua = UserAgent()
        user_agent = ua.random        
        options.add_argument(f"user-agent={user_agent}")

        return uc.Chrome()

    def bot_detection(self):
        element = self.driver.find_element(By.ID,'px-captcha')
        point= element.location
        pyautogui.moveTo(point['x']+100, point['y']+200)

        pyautogui.mouseDown()
        time.sleep(10.5)
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        time.sleep(1000)

    def scrape_data(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(2)
        betting_links = self.driver.find_elements("xpath", "//a")
    
        try: 
            self.driver.find_elements("xpath", "//h1[@text = 'Please verify you are a human']")
            self.bot_detection()
            betting_links = self.driver.find_elements("xpath", "//a")
        except:
            pass

        for parent in betting_links:
            if not self.valid_sports:
                break
            team_name = parent.get_attribute("title")
            if team_name in self.valid_sports:
                self.valid_parents.append(parent)
                self.sports_list.append(team_name)
                self.valid_sports.remove(team_name)

        for site in self.valid_parents:
            site.click()
            time.sleep(1.5)
            betting_card = site.find_elements("xpath", "//ul[@style = 'flex-direction: column; overflow: hidden auto; display: flex; min-width: 0px;']")
            self.sports_html.append(betting_card[-1].get_attribute("innerHTML"))

    def close_driver(self):
        self.driver.quit()

class FanDuelParser:
    @staticmethod
    def parse_spread_odds(input_string):
        pattern = re.compile(r'([+-]?\d*\.?\d+)([+-−]\d+)?')
        match = pattern.match(input_string)
        if match:
            return [match.group(1), match.group(2)]

    @staticmethod
    def parse_total_odds(input_string):
        pattern = re.compile(r'([A-Z])\s(\d*\.?\d+)([+-−]\d+)')
        match = pattern.match(input_string)
        if match:
            return [match.group(1), match.group(2), match.group(3)]
    @staticmethod
    def custom_selector(tag):
        return (
            tag.name == "div" and tag.has_attr("role") and "button" == tag.get("role")
        ) or (
            tag.name == "span" and tag.has_attr("role") and "text" == tag.get("role") 
        ) or (
            tag.name == "time"
        )

    

class FanDuelDataExtractor:
    @staticmethod
    def extract_data(sports_list, sports_html):
        output = {}
        
        for j in range(len(sports_list)):

            soup = BeautifulSoup(sports_html[j], 'html.parser')
            information_elements = soup.find_all(FanDuelParser.custom_selector)
            
            games = []

            i = 0
            while i < len(information_elements):
                line = information_elements[i].text
                
                if "Anytime" in line:
                    break

                team1 = line
                if (not information_elements[i+1].text.replace(" ","").isalpha() and len(information_elements[i+1].text) <=4):
                    team2 = information_elements[i+2].text
                    i+=2
                else:
                    team2 = information_elements[i+1].text

                spread_odds1 = FanDuelParser.parse_spread_odds(information_elements[i + 2].text)
                moneyline_odds1 = information_elements[i + 3].text
                total_odds1 = FanDuelParser.parse_total_odds(information_elements[i + 4].text)

                spread_odds2 = FanDuelParser.parse_spread_odds(information_elements[i + 5].text)
                moneyline_odds2 = information_elements[i + 6].text
                total_odds2 = FanDuelParser.parse_total_odds(information_elements[i + 7].text)
                if information_elements[i+8].has_attr("datetime"):
                    curr_date = information_elements[i+8].get("datetime")
                else:
                    curr_date = "LIVE"

                if moneyline_odds1== "":
                    moneyline_odds1 = None
                if moneyline_odds2 == "":
                    moneyline_odds2 = None
                    
                game = [curr_date,
                        [team1, {"Spread": spread_odds1,
                                 "Total": total_odds1,
                                 "Moneyline": moneyline_odds1}],
                        [team2, {"Spread": spread_odds2,
                                 "Total": total_odds2,
                                 "Moneyline": moneyline_odds2}]
                        ]
                i += 9

                games.append(game)
            output[sports_list[j]] = games

        return output
if __name__ == "__main__":
    valid_sports = ["NBA", "NFL", "NCAAB"]

    apikey = '76d1d89d03503e1c9a5454370a5b390c68b8393b'
    url = "https://sportsbook.fanduel.com/"

    params = {
        'url': url,
        'apikey': apikey,
        'antibot': 'true',
        'premium_proxy': 'true',
    }
    start = time.time()
    import requests

    response = requests.get('https://api.zenrows.com/v1/', params=params)
    print(response.text)

    '''

    from sbrscrape import Scoreboard

    import time

    s = time.time()
    games = Scoreboard(sport="NFL").games

    t = time.time()

    print(t-s)

    for key, val in games[0].items():
        print(key, val)

    scraper = FanDuelScraper(valid_sports)
    scraper.scrape_data(url)

    parser = FanDuelParser()
    extractor = FanDuelDataExtractor()  
    
    data = extractor.extract_data(scraper.sports_list, scraper.sports_html)
    end = time.time()
    print(data)
    print(end-start)'''
    #scraper.close_driver()
