from transitions import Machine
# from transitions.extensions import GraphMachine as Machine
from mydb.getFromDB import connect,getAllNames,getAddress,getAllNamesOfCertainType,getBussinessHour,getFB,getMap,getPhoneNumber
class FoodAsking():
    states=[
        {"name": "dummy"},
        {"name": "askingType"},
        {"name": "askingName"},
        {"name": "askingAddress"},
        {"name": "askingPhoneNumber"},
        {"name": "askingMap"},
        {"name": "askingFB"},
        {"name": "askingBussinessHour"},
    ]

    transitions=[
        {
            "trigger": "gotoAddress",
            "source":"*",   
            "dest": "askingAddress",
            "after": "transitAddress"
        },
        {
            "trigger": "gotoPhoneNumber",
            "source":"*", 
            "dest": "askingPhoneNumber",
            "after": "transitPhoneNumber"
        },
        {
            "trigger": "gotoMap",
            "source":"*",   
            "dest": "askingMap",
            "after": "transitMap"
        },
        {
            "trigger":"gotoFB",
            "source":"*",
            "dest": "askingFB",
            "after": "transitFB"
        },
        {
            "trigger": "gotoBussinessHour",
            "source":"*",
            "dest": "askingBussinessHour",
            "after": "transitBussinessHour"
        },
        {
            "trigger": "gotoName",
            "source":"*",
            "dest": "askingName",
            "after": "transitName"
        },
        {
            "trigger": "gotoType",
            "source": "dummy",
            "dest": "askingType",
            "after": "transitType"
        }
    ]

    def __init__(self):
        # create a machine
        self.machine=Machine( model=self,
                              states=FoodAsking.states,
                              transitions=FoodAsking.transitions,
                              initial="dummy" )
        self.client=connect() # get client
        
        self.ncku=self.client.region.ncku

        self.machine.get_graph().draw('my_state_diagram.png', prog='dot')


    def transitType(self,requestType):
        print("in transitType")
        self.allNames=getAllNamesOfCertainType(self.ncku,requestType)
    
    def transitName(self):
        print(f"now enter name state!")

    def transitAddress(self):
        print("in addressType")
        self.address=getAddress(self.ncku,self.resturantName)

    def transitFB(self):
        print("in fbType")
        self.fb=getFB(self.ncku,self.resturantName)
    
    def transitBussinessHour(self):
        print("in hour")
        self.hour=getBussinessHour(self.ncku,self.resturantName)
    
    def transitMap(self):
        print("in map")
        self.map=getMap(self.ncku,self.resturantName)
    
    def transitPhoneNumber(self):
        print("in contact info")
        self.phone=getPhoneNumber(self.ncku,self.resturantName)

