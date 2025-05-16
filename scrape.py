from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep
import time
start = time.time()

chrome_options = Options()

#chrome_options.add_argument("--headless=new") # for Chrome >= 109

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
    

#print([parent.get_attribute("outerHTML") for parent,text in valid_parents] )

draftKings_games = {}
bet_types = ["Spread", "Total", "Moneyline"]


for site, text in valid_parents:
    site.click()
    tables = site.find_elements("xpath", "//tbody[@class = 'sportsbook-table__body']")
    games = []
    curr = []
    for table in tables:
        rows = table.find_elements("xpath", ".//tr")
        parity = 0

        for row in rows:
            
            team_name = row.find_element("xpath", ".//div[@class = 'event-cell__name-text']")
            odds = row.find_elements("xpath", ".//div[@role= 'button' or @class = 'sportsbook-empty-cell']")

            team_bets = {}

            for i in range(len(bet_types)):
                curr_bet = odds[i]
                curr_odds = None
                stake = None
                try:
                    curr_odds = curr_bet.find_element("xpath", ".//span[starts-with(@class, 'sportsbook-odds')]").text
                    stake = curr_bet.find_element("xpath", ".//span[@class = 'sportsbook-outcome-cell__line']").text
                except:
                    pass
                team_bets[bet_types[i]] = (curr_odds,stake)
            
            add = [team_name.text, team_bets]
            if parity % 2 == 0:
                curr.append(add)
            else:
                curr.append(add)
                games.append(curr)
                curr = []
            parity+=1
    draftKings_games[text] = games
print(draftKings_games)
end = time.time()

print()
print(end-start)
