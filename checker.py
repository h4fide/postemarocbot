from api import Tracker
import database as db

class checker():
    @staticmethod
    def check(userid: int , tcode: str, repeat: int = 1):
        try:
            for index in range(repeat):
                laststatut = Tracker.LastStatus(tcode)
                if laststatut == 'Envoi livré':
                    print("Your Shipment Has Arrived :)")
                    arrived = 'arrived'
                    return arrived
                    
                elif db.read_currentstatus(userid, tcode) != db.read_newstatus(userid, tcode):
                    if laststatut == 'None' or laststatut == 'No response': 
                        pass
                    else:
                        db.create_newtstatus(laststatut, userid, tcode)
                    return True

                else:
                    if laststatut == 'None' or laststatut == 'No response':
                        pass
                    else:
                        db.create_currentstatus(laststatut, userid, tcode)
                    return False
        except:
            pass
