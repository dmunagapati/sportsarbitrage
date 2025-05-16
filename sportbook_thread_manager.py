import json
import logging
from betMGM import MGMDataExtractor
from bovada import BovadaDataExtractor
from caesarsV1 import CaesarsDataExtractor
from draftkingsV4 import DraftKingsDataExtractor
from espn import ESPNDataExtractor
from pinnacle import PinnacleDataExtractor

class SportbookThreadManager:
    def __init__(self):
        self.map = {
             "betmgm": MGMDataExtractor(),
             "bovada": BovadaDataExtractor(),
             "caesars": CaesarsDataExtractor(),
             "draftkings": DraftKingsDataExtractor(),
             "espn": ESPNDataExtractor(),
             "pinnacle": PinnacleDataExtractor()
        }
        self.update_num = 0

    def dump_data(self, bookmaker):
        data_extractor = self.map[bookmaker]
        data = data_extractor.run()
        json_object = json.dumps(data, indent=4)
        with open("sportbook_odds/{}.json".format(bookmaker), "w") as outfile:
                outfile.write(json_object)

    def continual_update(self, bookmaker):
         print("{}: Update #{}".format(bookmaker,self.update_num))
         while True:
            try:
                self.dump_data(bookmaker)
            except Exception as e:
                #print(e)
                 pass
            self.update_num+=1
    
    def start_sportsbook_thread(self, thread_num, bookmaker):
        logging.info("Thread %s (%s): starting", thread_num, bookmaker)
        self.continual_update(bookmaker)
        


    
            






