import json
import dialogs
import settings
from datetime import date
from pathlib import Path


class Diet:
    
    def __init__(self, name):
        self.name = name
        if self.load() is False:
            self.menu = dict()
            for i in settings.amer_diet:
                for k, v in i[0]:
                    self.menu[k] = eval(v)
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
            self.new_day()
            return True
        except FileNotFoundError:
            return False
            
    def save(self):
        with Path(__file__).parent.joinpath(self.name).open("w") as fout:
            json.dump(vars(self), fout, indent=2, sort_keys=True)

    def new_day(self):
        if self.date != date.today().isoformat():
            self.change_factor()
            for i in settings.amer_diet:
                for k, v in i[0].items():
                    if i[2] is None:
                        addition = eval(v)
                    else:
                        addition = eval(v) * i[2] ** self.factor
                    self.menu[k] = self.menu.get(k, 0) + (addition - self.eaten.get(k, 0))
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
            show = False
            for i in settings.amer_diet:
                if dish in i[0]:
                    if i[1] is None:
                        if (set(self.eaten.keys()) & set(i[0].keys())) == set():
                            show = True
                    if (i[1] is False) and (self.left(dish) > 0):
                        show = True
                    if i[1] is True:
                        show = True
            if show:
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
