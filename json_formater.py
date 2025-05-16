from datetime import datetime
def format_json(spread_odds1, spread_odds2, moneyline_odds1, moneyline_odds2, 
                    total_odds1, total_odds2, bookmaker):

        spread_odds1, spread_odds2, moneyline_odds1,\
        moneyline_odds2, total_odds1, total_odds2, bookmaker = edit_odds(spread_odds1, spread_odds2, moneyline_odds1, 
                                                                           moneyline_odds2, total_odds1, total_odds2, bookmaker)
        return  {"team1_moneyline": moneyline_odds1,
                 "team1_moneyline_book": bookmaker,
                 "team2_moneyline": moneyline_odds2,
                 "team2_moneyline_book": bookmaker,
                 "team1_spread": {
                        spread_odds1[0]: {
                                "team1_spread_odds": spread_odds1[1],
                                "team1_spread_book": bookmaker}},
                "team2_spread": {
                        spread_odds2[0]: {
                                "team2_spread_odds": spread_odds2[1],
                                "team2_spread_book": bookmaker}},
                "over": {
                    total_odds1[1]: {
                            "total_over_odds": total_odds1[2], 
                            "total_over_book": bookmaker}},
                "under": {
                    total_odds2[1]: {
                            "total_under_odds": total_odds2[2],
                            "total_under_book": bookmaker}},
                "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}



def edit_odds(spread_odds1, spread_odds2, moneyline_odds1, moneyline_odds2, 
                    total_odds1, total_odds2, bookmaker):
        if moneyline_odds1:
            moneyline_odds1 = moneyline_odds1.replace("−","-")
        if moneyline_odds2:
               moneyline_odds2 = moneyline_odds2.replace("−","-")

        for i in range(len(spread_odds1)):
            if spread_odds1[i]:
                spread_odds1[i] = spread_odds1[i].replace("−","-")

        for i in range(len(spread_odds2)):
            if spread_odds2[i]:
                spread_odds2[i] = spread_odds2[i].replace("−","-")
        
        for i in range(len(total_odds1)):
            if total_odds1[i]:
                total_odds1[i] = total_odds1[i].replace("−","-")
        
        for i in range(len(total_odds2)):
            if total_odds2[i]:
                total_odds2[i] = total_odds2[i].replace("−","-")

        return spread_odds1, spread_odds2, moneyline_odds1, moneyline_odds2, total_odds1, total_odds2, bookmaker
        




        return {"team_1": {
                    "name": team1,
                    "moneyline": moneyline_odds1,
                    "spread": {
                        "difference":spread_odds1[0],
                        "odds": spread_odds1[1]
                    }
                },"team_2": {
                    "name": team2,
                    "moneyline": moneyline_odds2,
                    "spread": {
                        "difference":spread_odds2[0],
                        "odds": spread_odds2[1]
                        }
                },"over": {
                    "total": total_odds1[1],
                    "odds": total_odds1[2]
                },"under": {
                    "total": total_odds2[1],
                    "odds": total_odds2[2]
                }, "bookmaker":bookmaker, 
                   "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
        
