from transitions import Machine


class FoodAsking():
    states=[
        {"name": "askingType"},
        {"name": "askingName"},
        ("name": "askingAddress"),
        {"name": "askingPhoneNumber"},
        {"name": "askingMap"},
        {"name": "askingFB"},
        {"name": "askingBussinessHour"},
    ]

    transitions=[
        {"trigger": "address",      "source":"*",   "dest": "askingAddress" },
        {"trigger": "phoneNumber",  "source":"*",   "dest": "askingPhoneNumber" },
        {"trigger": "map",          "source":"*",   "dest": "askingMap"},
        {"trigger": "fb",           "source":"*",   "dest": "askingFB"},
        {"trigger": "bussinessHour","source":"*",   "dest": "askingBussinessHour" },
        {"trigger": "tpye",         "source":"*",   "dest": "askingType" },
    ]
    def __init__(self,initState):
        # create a machine
        self.machine=Machine(model=self,states=FoodAsking.states,initial=initState)
        



# food=Foodasking("askingName")