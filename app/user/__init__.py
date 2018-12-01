from app.stateMachine.foodAsking import FoodAsking

class User():
    def __init__(self,psid):
        self.psid=psid
        self.foodAsking=FoodAsking()