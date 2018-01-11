import Diet
import ui


class Interface(object):
    
    def __init__(self, diet_name):
        self.view = ui.TableView()
        self.view.present(style='full_screen', hide_title_bar=False)
        self.diet = Diet.Diet(diet_name)
        self.view.name = 'Фактор диеты - ' + str(self.diet.factor)
        self.can_be_eaten = self.diet.can_be_eaten()
        items = [''.join(i) for i in self.can_be_eaten]
        self.datasource = ui.ListDataSource(items)
        self.datasource.delete_enabled = False
        self.datasource.action = self.row_tapped
        self.view.data_source = self.datasource
        self.view.delegate = self.datasource
        self.view.reload()
        
    def row_tapped(self, sender):
        dish = self.can_be_eaten[sender.selected_row][0]
        self.diet.eat(dish)
        self.can_be_eaten = self.diet.can_be_eaten()
        sender.items = [''.join(i) for i in self.can_be_eaten]
        

if __name__ == '__main__':
    Interface('DayMenu.json')
