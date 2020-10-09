import threading
import time
import datetime
from validate_email import validate_email


class function1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self, df):
        self.startTime = datetime.now()
        for index, row in self.df.iterrows():
            is_valid = validate_email(self.df.iat[index, 0], verify=True)
            self.df.iat[index, 1] = is_valid
            print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[index, 0], index,
                                                                        self.df.iat[index, 1], is_valid,
                                                                        len(self.df.index) - 1))
            # Количество строк DataFrame len(self.df.index)-1
            # Текущий обрабатываемы элемент
            self.index_cur = index
            # Всего обрабатываемых элементов
            self.index_max = len(self.df.index) - 1

#            self.label_state.setText("{0} из {1}".format(index, len(self.df.index) - 1))
        #            model = PandasModel(self.df)
        #            self.tableView.setModel(model)
        #            self.tableView.update()
        self.save_table_to_excel()
        self.endTime = datetime.now()

    def get_index_cur(self):
        return self.index_cur
