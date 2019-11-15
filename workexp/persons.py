import sys
import datetime

class person:

    def __init__( self):
        pass

    def get_details( self, person_type, roles, types):
        self.pfirst_name = raw_input("Enter persons first name: ")
        self.plast_name = raw_input("Enter persons last name: ")
        self.pemail = raw_input("Enter persons email: ")

        print("Available roles: "+ str( roles))
        persons_role = raw_input("Enter the person's role: ")
        i=1
        for role in roles:
            if role == persons_role:
                self.ptrainee_position = i
                self.pperson_id = i
            i += 1

        self.pcurrent_position = raw_input("Enter persons current position: ")
        self.pstate = raw_input("Enter persons state of residence: ")
        self.pincome = raw_input("Enter persons total monthly income before taxes: ")
        self.prelocation = raw_input("Will this person relocate (y/n): ")

        print("Available Types: "+ str( types))
        persons_type = raw_input("Enter the person's type: ")
        j=1
        for type in types:
            if type == persons_type:
                self.ptype = j
            j += 1

        self.profile_picture = " "
        self.paystub         = " "

        while True:
            self.pstart_date = raw_input("Enter persons start date as YYYY-MM-DD: ")
            self.pgraduation_date = raw_input("Enter persons graduation date as YYYY-MM-DD: ")
            self.plast_verification = raw_input("Enter graduation date as last verification date as YYYY-MM-DD: ")
            if self.validate_input( 'date', self.pstart_date) and self.validate_input( 'date', self.pgraduation_date):
                break

        self.person = {'first_name':       self.pfirst_name,
                       'last_name':        self.plast_name,
                       'email':            self.pemail,
                       'profile_picture':  self.profile_picture,
                       'paystub':          self.paystub,  
                       'trainee_position': self.ptrainee_position,
                       'person_id':        self.pperson_id,
                       'current_position': self.pcurrent_position,
                       'state':            self.pstate,
                       'income':           self.pincome,
                       'relocation':       self.prelocation,
                       'start_date':       self.pstart_date,
                       'graduation_date':  self.pgraduation_date,
                       'last_verification':self.plast_verification,
                       'type':             self.ptype
                      }

    def get_profile_picture( self):
        return self.person['profile_picture']
    def get_paystub( self):
        return self.person['paystub']
    def get_first_name( self):
        return self.person['first_name']
    def gett_first_name( self):
        return self.first_name
    def get_last_name( self):
        return self.person['last_name']
    def gett_last_name( self):
        return self.last_name
    def get_email(  self):
        return self.person['email']
    def gett_email(  self):
        return self.email
    def get_trainee_position( self):
        return self.person['person_id']
    def gett_trainee_position( self):
        return self.person_id
    # return numeric of student, trainee, graduated, verified etc
    def get_person_id( self):
        return self.person['person_id']
    def get_current_position( self):
        return self.person['current_position']
    def get_state( self):
        return self.person['state']
    def get_income( self):
        return self.person['income']
    def get_relocation( self):
        return self.person['relocation']
    def get_start_date( self):
        return self.person['start_date']
    def gett_start_date( self):
        if self.start_date is None:
            self.start_date = datetime.datetime.strptime('1-1-1970', '%m-%d-%Y')
        return self.start_date
    def get_graduation_date( self):
        return self.person['graduation_date']
    def gett_graduation_date( self):
        if self.graduation_date is None:
            self.graduation_date = self.gett_start_date() #datetime.datetime.strptime('1-1-1970', '%Y-%m-%d')
        return self.graduation_date
    def get_last_verification( self):
        return self.person['last_verification']
    def gett_last_verification( self):
        if self.last_verification is None:
            self.last_verification = self.gett_graduation_date() #datetime.datetime.strptime('1-1-1970', '%Y-%m-%d')
        return self.last_verification
    # return devops, aws, linux etc
    def gett_role( self):
        return self.type
    def get_type( self):
        return self.person['type']

    def validate_input(self, input_type, input_value):
        if input_type == 'string':
            return ( isinstance(input_value, basestring))
        if input_type == 'date':
            try:
                datetime.datetime.strptime(input_value, '%Y-%m-%d')
                return True
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
                return False

    def set_user( self, user_details):
        keys = ['self.ID', 'self.first_name', 'self.last_name', 'self.email', 'self.person_id', 'self.current_position', 'self.state', 'self.income', 'self.relocation', 'self.last_verification', 'self.start_date', 'self.graduation_date', 'self.type']
        i = 0
        for entry in user_details:
            if keys[i] == 'self.first_name':
                self.first_name = entry
            if keys[i] == 'self.last_name':
                self.last_name = entry
            if keys[i] == 'self.email':
                self.email = entry
            if keys[i] == 'self.person_id':
                self.person_id = entry
            if keys[i] == 'self.current_position':
                self.current_position = entry
            if keys[i] == 'self.state':
                self.state = entry
            if keys[i] == 'self.income':
                self.income = entry
            if keys[i] == 'self.relocation':
                self.relocation = entry
            if keys[i] == 'self.last_verification':
                self.last_verification = entry
            if keys[i] == 'self.start_date':
                self.start_date = entry
            if keys[i] == 'self.graduation_date':
                self.graduation_date = entry
            if keys[i] == 'self.type':
                self.type = entry
            i += 1

