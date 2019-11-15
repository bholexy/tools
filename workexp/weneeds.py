import sys
from datetime import datetime

class needs:

    def __init__( self):
        pass

    def income_verification(self, last_verification_date, graduation_date, role):
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime( today, "%Y-%m-%d")
        if graduation_date:
            graduation_date = graduation_date.strftime("%Y-%m-%d")
            graduation_date = datetime.strptime( graduation_date, "%Y-%m-%d")
            diff = (graduation_date - today).days

            needsEmailRoles = ['breach', 'graduated']
            #User hasnt graduated if diff > 0
            if diff > 0:
                print("User does not graduate until: "+ str(graduation_date.date()))
                return False

            #user has graduated
            elif role in needsEmailRoles:
                #last verification date is empty, that means user hasnt uploaded pay stub after graduating
                if last_verification_date == None:
                    return True
                else:
                    last_verification_date = last_verification_date.strftime("%Y-%m-%d")
                    last_verification_date = datetime.strptime( last_verification_date, "%Y-%m-%d")
                    diff = (last_verification_date - today).days
                    print( "Time since last verification: " + str( diff))
                    if diff < -30:
                        return True
                    else:
                        print("User has been verified within 30 days, no need for verification")
                        return False

            #user has graduated and income is verified
            elif role == 'verified':
                print( "User graduated. Income verified")
            else:
                print( "User graduated. User is job hunting")

        else:
            print("User does not graduate until: "+ str(graduation_date.date()))
            return False
       
        
        

    def graduation_reminder(self, graduation_date):
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime( today, "%Y-%m-%d")
        if graduation_date == None:
            print( "There has not been any graduation date for this user")
            return False
        graduation_date = graduation_date.strftime("%Y-%m-%d")
        graduation_date = datetime.strptime( graduation_date, "%Y-%m-%d")
        diff = (graduation_date - today).days
        if diff > 0:
            print( "Days before graduation: " + str( diff))
            return True
        else:
            print( "Days since graduation: " + str( abs(diff)))
            return False


    def status(self,graduation_date,last_verification_date):
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime( today, "%Y-%m-%d")
        
        if last_verification_date == None:
            print( "Default")
        else:
            print( "In Compliance")

        if graduation_date == None:
            print( "There has not been any graduation date for this user")
            return False
        

        graduation_date = graduation_date.strftime("%Y-%m-%d")
        graduation_date = datetime.strptime( graduation_date, "%Y-%m-%d")

        if graduation_date < today:
            print( "Job Searching")
        else:
            print("In Training")

    def needs_role_change(self, last_verification_date, graduation_date, role):
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime( today, "%Y-%m-%d")
        if graduation_date:
            graduation_date = graduation_date.strftime("%Y-%m-%d")
            graduation_date = datetime.strptime( graduation_date, "%Y-%m-%d")
            diff = (graduation_date - today).days

            learnerRoles = ['trainee', 'student']
            #User has graduated if diff < 0 but the role still says the user is learning
            if diff < 0 and role.upper().lower() in learnerRoles:
                print("User graduated on: "+ str(graduation_date.date())+", role change needed")
                return True
