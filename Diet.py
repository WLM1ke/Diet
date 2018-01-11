import json
import dialogs
from datetime import date
from pathlib import Path


ALFA = 0.91
ALCO = 'Alc, 28g/200cal'
AMER_DIET = {  # 2600
    'Veg Green, 1c':      '2.5/7*2',  # Чашка зелени равна 2 чашкам
    'Veg Orange, 1c':     '7/7',
    'Veg Legumes, 1c':    '2.5/7',
    'Veg Starchy, 1c':    '7/7/10',  # Спринт по отказу от крахмалестых овощей
    'Veg Other, 1c':      '5.5/7',
    'Fruits, 1c':         '2.5',
    'Grain Whole, 30g':   '4.5/10',  # Спринт по отказу от зерновых
    'Grain Refined, 30g': '4.5/10',  # Спринт по отказу от зерновых
    'Dairy, 150g':        '2.5*50/150',
    'Prot Seafood, 100g': '17/7*30/100',
    'Prot Meats, 100g':   '31/7*30/100',
    'Nuts, 30g':          '5/7*15/30',
    'Oils, 17g':          '34/34',
    ALCO:                 '330/200'
    }


class Diet:
    
    def __init__(self, name):
        self.name = name
        if self.load() is False:
            self.menu = {k: eval(v) for k, v in AMER_DIET.items()}
            self.eaten = {}
            self.factor = 0
            self.date = date.today().isoformat()
            self.save()
    
    def load(self):
        try:
            with Path(__file__).parent.joinpath(self.name).open() as fin:
                dump = json.load(fin)
            for k, v in dump.items():
                setattr(self, k, v)
            self.newday()
            return True
        except FileNotFoundError:
            return False
            
    def save(self):
        with Path(__file__).parent.joinpath(self.name).open("w") as fout:
            json.dump(vars(self), fout, indent=2, sort_keys=True)

    def newday(self):
        if self.date != date.today().isoformat():
            self.change_factor()
            for k, v in AMER_DIET.items():
                addition = eval(v) * ALFA ** self.factor
                self.menu[k] += (addition - self.eaten.get(k, 0))
            self.eaten = {}
            self.date = date.today().isoformat()
            self.save()
                
    def change_factor(self):
        ans = dialogs.alert(
            title='Фактор диеты - ' + str(self.factor),
            message='Вес в норме?',
            button1='Да',
            button2='Нет',
            hide_cancel_button=True)
        if ans == 1:
            self.factor = max(0, self.factor - 1)
        else:
            self.factor += 1

    def left(self, dish):
        self.load()
        return int(self.menu[dish] - self.eaten.get(dish, 0))
                
    def can_be_eaten(self):
        self.load()
        items = []
        menu = self.menu
        eaten = self.eaten
        for dish in sorted(menu):
            if (self.left(dish) > min(0, self.left(ALCO))) | (dish == ALCO):
                item = [
                    dish,
                    ' - ',
                    str(eaten.get(dish, 0)),
                    '/',
                    str(int(menu[dish]))]
                items.append(item)
        return items
              
    def eat(self, dish):
        self.load()
        self.eaten[dish] = self.eaten.get(dish, 0) + 1
        self.save()
