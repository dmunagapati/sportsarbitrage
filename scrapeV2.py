from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from time import sleep
import time
chrome_options = Options()

chrome_options.add_argument("--headless=new") # for Chrome >= 109

driver = webdriver.Chrome(options=chrome_options)
valid_sports = {
    "NBA",
    "NFL",
    "College Basketball (M)",
}
driver.get("https://sportsbook.draftkings.com/?_gl=1*1ka4n6u*_ga*Nzk3NDQ5NTk4LjE2OTk4NDU2ODU.*_ga_QG8WHJSQMJ*MTcwMTQ4MDY1NS41LjEuMTcwMTQ4MTIzOS42MC4wLjA.&_ga=2.1074993.1249829292.1701406770-797449598.1699845685")
betting_links = driver.find_elements("xpath","//a[starts-with(@href, '/leagues') and @class ='sportsbook-navigation-item-link sportsbook-navigation-item-link--league']")
valid_parents = []
for parent in betting_links:
    child = parent.find_element("xpath",".//span[@class='sportsbook-navitation-item-title-text']")
    if len(valid_sports ) == 0:
        break
    if child.text in valid_sports:
        parent.click()
        valid_parents.append((parent,child.text))
        valid_sports.remove(child.text)
    
draftKings_games = {}
bet_types = ["Spread", "Total", "Moneyline"]
for site, text in valid_parents:
    site.click()
    boxes = site.find_elements("xpath","//th[starts-with(@class, 'sportsbook-table__column-row')] | //td[starts-with(@class, 'sportsbook-table__column-row')] | //th[@class = 'always-left column-header']")
    games, curr, team_bets = [],[], {}
    index =0
    for i in range(len(boxes)):

        curr_box = boxes[i] 

        #Date check
        try:
            lowest = curr_box.find_element(By.CLASS_NAME, "sportsbook-table-header__title")
            date = lowest.get_attribute("textContent")
            continue
        except:
            pass
        if index%4==0:
            team_name = curr_box.find_element(By.CLASS_NAME, "event-cell__name-text").text
            if index%8!=0:
                curr.append(date)
        else:
            bet_types = ["Spread", "Total", "Moneyline"]
            bet_type = bet_types[index%4-1]
            curr_odds = None
            stake = None
            try:
                curr_odds = curr_box.find_element("xpath", ".//span[starts-with(@class, 'sportsbook-odds')]").text
                stake = curr_box.find_element("xpath", ".//span[@class = 'sportsbook-outcome-cell__line']").text
            except:
                pass
            team_bets[bet_type] = (curr_odds, stake)
            if index%8 == 3:
                curr.append([team_name, team_bets])
                team_bets = {}
            if index%8 ==7:
                curr.append([team_name, team_bets])
                team_bets = {}
                games.append(curr)
                curr = []
        index+=1
    draftKings_games[text] = games
print(draftKings_games)
