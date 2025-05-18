import os
import json
import pickle
import smtplib

class ArbTracker():
    def __init__(self):
        self.arbs = {}
        self.HOST = "smtp-mail.outlook.com"
        self.PORT = 587
        self.FROM_EMAIL = "sports_arbing@outlook.com"
        self.TO_EMAIL = "ayushp802@gmail.com"
        self.PASSWORD = "$portsBets123"

    def track(self):
        if os.path.exists("possible_arbs"):
            with open("possible_arbs", "r") as file:
                json_data = json.load(file)
        new_arbs = {}
        for game_name, game_data in json_data.items():
            game_name, arb_type, number, sport  = game_name.split("//")

            if arb_type == "moneyline":
                new_arbs[(game_name, "moneyline", sport)] = [game_data["team1_moneyline"], game_data["team1_moneyline_book"],
                                                       game_data["team2_moneyline"], game_data["team2_moneyline_book"], 
                                                       game_data["last_updated"]]
            if arb_type == "spread":
                new_arbs[(game_name, "spread", number, sport)] = [game_data["team1_spread"][number]["team1_spread_odds"], 
                                                            game_data["team1_spread"][number]["team1_spread_book"],
                                                            game_data["team2_spread"][number]["team2_spread_odds"], 
                                                            game_data["team2_spread"][number]["team2_spread_book"],
                                                            game_data["last_updated"]]
            if arb_type == "total":
                new_arbs[(game_name, "spread", number, sport)] = [game_data["over"][number]["total_over_odds"], 
                                                            game_data["over"][number]["total_over_book"],
                                                            game_data["under"][number]["total_under_odds"], 
                                                            game_data["under"][number]["total_under_book"],
                                                            game_data["last_updated"]]
        self.arbs = new_arbs
    def send_mail(self, tuples):

        message = """Subject: ARB FOUND

        """
        for tup in tuples:
            message += str(tup)+ "\n"


        smtp = smtplib.SMTP(self.HOST, self.PORT)
        status_code, response = smtp.ehlo()
        print("Echoing Server: ", status_code, response)

        status_code, response = smtp.starttls()
        print("Starting TLS: ", status_code, response)

        status_code, response = smtp.login(self.FROM_EMAIL, self.PASSWORD)
        print("Logging In: ", status_code, response)

        smtp.sendmail(self.FROM_EMAIL, self.TO_EMAIL, message)
        smtp.quit()


    def update(self):
        self.track()
        send_message = []
        if os.path.exists("old_arbs.pkl"):
            with open("old_arbs.pkl", "rb") as infile:
                old_arbs = pickle.load(infile)

            for tup in self.arbs.keys():
                if tup not in old_arbs:
                    send_message.append(tup) 
        else:
            for tup in self.arbs.keys():
                send_message.append(tup)
            
        if len(send_message) > 0:
            print("NEW ARBITRAGE FOUND:")
            for arb in send_message:
                print(arb)
                self.send_mail(send_message)

        with open("old_arbs.pkl", "wb") as outfile:
            pickle.dump(self.arbs, outfile)


    
   