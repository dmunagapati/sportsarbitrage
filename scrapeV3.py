from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from time import sleep
import time

chrome_options = Options()

chrome_options.add_argument("--headless=new") # for Chrome >= 109
driver = webdriver.Chrome(options=chrome_options)
valid_sports = [
    "NBA",
    "NFL",
    "College Basketball (M)",
]
driver.get("https://sportsbook.draftkings.com/?_gl=1*1ka4n6u*_ga*Nzk3NDQ5NTk4LjE2OTk4NDU2ODU.*_ga_QG8WHJSQMJ*MTcwMTQ4MDY1NS41LjEuMTcwMTQ4MTIzOS42MC4wLjA.&_ga=2.1074993.1249829292.1701406770-797449598.1699845685")
start = time.time()
driver.implicitly_wait(4)
betting_links = driver.find_elements("xpath","//a[starts-with(@href, '/leagues') and @class ='sportsbook-navigation-item-link sportsbook-navigation-item-link--league']")


sports_list = []
valid_parents = []
for parent in betting_links:
    child = parent.find_element("xpath",".//span[@class='sportsbook-navitation-item-title-text']")
    if len(valid_sports ) == 0:
        break
    if child.text in valid_sports:
        parent.click()
        valid_parents.append(parent)
        sports_list.append(child.text)
        valid_sports.remove(child.text)
    
sports_html = []


betting_card = None
for site in valid_parents:
    site.click()
    betting_card = site.find_element("xpath", "//div[@class = 'sportsbook-offer-category-card']")
    sports_html.append(betting_card.get_attribute("innerHTML"))


date = {"Today", "Tomorrow", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}
def custom_selector(tag):
    return (
        tag.name == "div" and tag.has_attr("class") and "event-cell__name-text" in tag.get("class")
    ) or (
        tag.name == "td" and tag.has_attr("class") and "sportsbook-table__column-row" in tag.get("class")
    ) or (
        tag.name == "th" and tag.has_attr("class") and "always-left" in tag.get("class") and "column-header" in tag.get("class")
    )


def parse_spread_odds(input_string):
    pattern = re.compile(r'([+-]?\d*\.?\d+)([+-−]\d+)?')
    match = pattern.match(input_string)
    if match:
        return [match.group(1), match.group(2)]


def parse_total_odds(input_string):
    pattern = re.compile(r'([A-Z])\s(\d*\.?\d+)([+-−]\d+)')
    match = pattern.match(input_string)
    if match:
        return [match.group(1), match.group(2), match.group(3)]



curr_date = "Today"

end = time.time()

from bs4 import BeautifulSoup
output = {}
for j in range(len(sports_list)):
    soup = BeautifulSoup(sports_html[j], 'html.parser')
    information_elements = soup.find_all(custom_selector)
    games = []

    i = 0
    while i < len(information_elements):

        line = information_elements[i].text
        flag = False

        for d in date:
            if d in line:
                curr_date = line
                flag = True
                break

        if flag:
            i+=1
            continue

        team1 = line
        spread_odds1 = parse_spread_odds(information_elements[i+1].text) 
        total_odds1 = parse_total_odds(information_elements[i+2].text)
        moneyline_odds1 = information_elements[i+3].text

        team2 = information_elements[i+4].text
        spread_odds2 = parse_spread_odds(information_elements[i+5].text)
        total_odds2 = parse_total_odds(information_elements[i+6].text)
        moneyline_odds2 = information_elements[i+7].text

        game = [curr_date, 
                [team1, {"Spread": spread_odds1, 
                         "Total": total_odds1, 
                         "Moneyline":moneyline_odds1}],
                [team2, {"Spread": spread_odds2, 
                         "Total": total_odds2, 
                         "Moneyline":moneyline_odds2}]
                ]
        i+=8

        
        games.append(game)
    output[sports_list[j]] = games





print(end-start)
end = time.time()
print(end-start)