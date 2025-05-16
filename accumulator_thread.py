import os
import json
from word_process import select_word
import nltk
from datetime import datetime
import fuzzywuzzy
class accumulator:
    def __init__(self):
        self.sports = {"NFL":None, "NBA":None, "NCAAM":None}
        self.arbs  = {}
        nltk.download('punkt')
        nltk.download('stopwords')
    def start_accumulator_thread(self):
        directory_path = 'sportbook_odds/'
        files = os.listdir(directory_path)
        self.arbs = {}
        # Loop through each file in the directory
        for file_path in files:
            bookmaker = file_path.replace(".json","")
            with open(os.path.join(directory_path,file_path), "r") as file:
                json_data = json.load(file)
                
                for sport, new_dates in json_data.items():
                    if self.sports.get(sport, None) == None:
                        self.sports[sport] = new_dates
                    else:
                        self.update_sport(new_dates = new_dates, curr_dates= self.sports[sport], bookmaker = bookmaker, sport=sport)

        json_object = json.dumps(self.arbs, indent=4)
        with open("possible_arbs", "w") as outfile:
                outfile.write(json_object)
                


    def update_sport(self, new_dates, curr_dates, bookmaker,sport):
        for date, games in curr_dates.items():
            if date == "Live":
                continue
            if date in new_dates:
                new_games = new_dates[date]
                for game_name, game_data in games.items():
                    match, team1, team2 = self.find(date, game_name, new_games)
                    if match:
                        new_game_data = new_games[match]

                        self.update_record_bookeeper(game_data, new_game_data, team1, team2)
                        game_data["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        self.find_arb(game_data, game_name,sport)
                    else:
                        if game_data["team1_moneyline_book"] == bookmaker:
                            game_data["team1_moneyline_book"] = ''
                        if game_data["team2_moneyline_book"] == bookmaker:
                            game_data["team2_moneyline_book"] = ''
                        for spread, spread_data in game_data["team1_spread"].items():
                            if spread_data["team1_spread_book"] == bookmaker:
                                del game_data["team1_spread"][spread]
                        for spread, spread_data in game_data["team2_spread"].items():
                            if spread_data["team2_spread_book"] == bookmaker:
                                del game_data["team2_spread"][spread]
                        for over, over_data in game_data["over"].items():
                            if over_data["total_over_book"] == bookmaker:
                                del game_data["over"][over]
                        for under, under_data in game_data["under"].items():
                            if under_data["total_under_book"] == bookmaker:
                                del game_data["under"][under]
                        game_data["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        json_object = json.dumps(self.sports, indent=4)
        with open("output", "w") as outfile:
            outfile.write(json_object)

    def find(self, date, game_name, possible_games):
        names = list(possible_games.keys())
        team1, team2 = "team1", "team2"

        curr_first_team, _ = game_name.split(" vs. ")
        ans = select_word(input_word=game_name, word_list=names)

        if ans:
            match, score = ans
            if score <60:
                return None, None, None
            new_first_team, new_second_team = match.split(" vs. ")

            _, new_first_score = select_word(input_word=curr_first_team, word_list=[new_first_team])
            _, new_second_score = select_word(input_word=curr_first_team, word_list=[new_second_team])
            if new_second_score > new_first_score:
                team1, team2 = "team2", "team1"
                return None, None, None
            return match, team1, team2
        else:
            return None, None, None
        

    def update_record_bookeeper(self, curr_game_data, new_game_data, team1, team2):

        if new_game_data['{}_moneyline'.format(team1)]:
            if (curr_game_data['team1_moneyline'] == '' or curr_game_data['team1_moneyline'] == None or float(new_game_data['{}_moneyline'.format(team1)]) > float(curr_game_data['team1_moneyline'])):
                curr_game_data['team1_moneyline'] = new_game_data['{}_moneyline'.format(team1)]
                curr_game_data['team1_moneyline_book'] = new_game_data['{}_moneyline_book'.format(team1)]
            elif curr_game_data["team1_moneyline_book"] == new_game_data["{}_moneyline_book".format(team1)]:
                curr_game_data['team1_moneyline'] = new_game_data['{}_moneyline'.format(team1)]

        
        if new_game_data['{}_moneyline'.format(team2)]:
            if (curr_game_data['team2_moneyline'] == '' or curr_game_data['team2_moneyline'] == None or float(new_game_data['{}_moneyline'.format(team2)]) > float(curr_game_data['team2_moneyline'])):
                curr_game_data['team2_moneyline'] = new_game_data['{}_moneyline'.format(team2)]
                curr_game_data['team2_moneyline_book'] = new_game_data['{}_moneyline_book'.format(team2)]
            elif curr_game_data["team2_moneyline_book"] == new_game_data["{}_moneyline_book".format(team2)]:
                curr_game_data['team2_moneyline'] = new_game_data['{}_moneyline'.format(team2)]

        #Team 1 Spread Updating
        
        for curr_spread, curr_spread_dict in curr_game_data["team1_spread"].items():
            if curr_spread == "null":
                continue
            if curr_spread in new_game_data["{}_spread".format(team1)]:
                new_spread_dict = new_game_data["{}_spread".format(team1)][curr_spread]

                if float(curr_spread_dict["team1_spread_odds"]) < float(new_spread_dict["{}_spread_odds".format(team1)]) or \
                    curr_spread_dict["team1_spread_book"] == new_spread_dict["{}_spread_book".format(team1)]:

                    curr_spread_dict["team1_spread_odds"] = new_spread_dict["{}_spread_odds".format(team1)]
                    curr_spread_dict["team1_spread_book"] = new_spread_dict["{}_spread_book".format(team1)]
                
                del new_game_data["{}_spread".format(team1)][curr_spread]

        for new_spread, new_spread_dict in new_game_data["{}_spread".format(team1)].items():
            if new_spread== "null":
                continue
            curr_game_data["team1_spread"][new_spread] = new_spread_dict    

        #Team 2 Spread Updating
        for curr_spread, curr_spread_dict in curr_game_data["team2_spread"].items():
            if curr_spread == "null":
                continue
            if curr_spread in new_game_data["{}_spread".format(team2)]:
                new_spread_dict = new_game_data["{}_spread".format(team2)][curr_spread]

                if float(curr_spread_dict["team2_spread_odds"]) < float(new_spread_dict["{}_spread_odds".format(team2)]) or \
                    curr_spread_dict["team2_spread_book"] == new_spread_dict["{}_spread_book".format(team2)]:
                    
                    curr_spread_dict["team2_spread_odds"] = new_spread_dict["{}_spread_odds".format(team2)]
                    curr_spread_dict["team2_spread_book"] = new_spread_dict["{}_spread_book".format(team2)]

                del new_game_data["{}_spread".format(team2)][curr_spread]
        for new_spread, new_spread_dict in new_game_data["{}_spread".format(team2)].items():
            if new_spread== "null":
                continue
            curr_game_data["team2_spread"][new_spread] = new_spread_dict    

        

        #Team 1 Over Updating
        
        for curr_over, curr_over_dict in curr_game_data["over"].items():
            if curr_over == "null":
                continue
            if curr_over in new_game_data["over"]:
                new_over_dict = new_game_data["over"][curr_over]

                if float(curr_over_dict["total_over_odds"]) < float(new_over_dict["total_over_odds"]) or \
                    curr_over_dict["total_over_book"] == new_over_dict["total_over_book"]:

                    curr_over_dict["total_over_odds"] = new_over_dict["total_over_odds"]
                    curr_over_dict["total_over_book"] = new_over_dict["total_over_book"]
                
                del new_game_data["over"][curr_over]

        for new_over, new_over_dict in new_game_data["over"].items():
            if new_over== "null":
                continue
            curr_game_data["over"][new_over] = new_over_dict    

        #Team 2 Under Updating
        
        for curr_under, curr_under_dict in curr_game_data["under"].items():
            if curr_under == "null":
                continue
            if curr_under in new_game_data["under"]:
                new_under_dict = new_game_data["under"][curr_under]

                if float(curr_under_dict["total_under_odds"]) < float(new_under_dict["total_under_odds"]) or \
                    curr_under_dict["total_under_book"] == new_under_dict["total_under_book"]:

                    curr_under_dict["total_under_odds"] = new_under_dict["total_under_odds"]
                    curr_under_dict["total_under_book"] = new_under_dict["total_under_book"]
                
                del new_game_data["under"][curr_under]

        for new_under, new_under_dict in new_game_data["under"].items():
            if new_under== "null":
                continue
            curr_game_data["under"][new_under] = new_under_dict    
    def find_arb(self, game_data, game_name, sport):
        
        if game_data['team1_moneyline'] != "" and game_data['team2_moneyline'] != "" and \
                self.is_arb(float(game_data['team1_moneyline']), float(game_data['team2_moneyline'])):
            self.arbs[game_name + "//moneyline//None//{}".format(sport)]=  game_data

        for spread, spread_data in game_data["team1_spread"].items():
            if spread == None or spread == "null":
                continue
            if spread in game_data["team2_spread"]:
                if self.is_arb(float(game_data["team1_spread"][spread]["team1_spread_odds"]), 
                            float(game_data["team2_spread"][spread]["team2_spread_odds"])):
                    self.arbs[game_name + "//spread//{}//{}".format(spread,sport)]=  game_data

            
        for total, over_data in game_data["over"].items():
            if total == None or total == "null":
                continue
            if total in game_data["under"]:
                if self.is_arb(float(game_data["over"][total]["total_over_odds"]), 
                               float(game_data["under"][total]["total_under_odds"])):
                    self.arbs[game_name + "//total//{}//{}".format(total,sport)]=  game_data
                    
    def is_arb(self, odds1, odds2):
        implied_prob1, implied_prob2 = None, None
        if odds1 == None or odds2 == None:
            return False
        if odds1>0:
            implied_prob1 = 100/(odds1+100)*100
        else:
            implied_prob1= -100*odds1/(-1*odds1+100)
        if odds2>0:
            implied_prob2 = 100/(odds2+100)*100
        else:
            implied_prob2= -100*odds2/(-1*odds2+100)
        if implied_prob2+implied_prob1 < 100:
            return True
        return False

        
        


if __name__ == "__main__":
    a = accumulator()
    a.start_accumulator_thread()
    

    

        
