import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
from dateutil import parser as dt_parser


# Загружаем данные из csv файла
# sep - формат данных на основе регулярных выражений, чтобы не быдо ошибок
data = pd.read_csv('./input.csv',sep=r'\s*,\s*', header=0, encoding='utf8', engine='python')

# стиль графика
style.use('ggplot')

# преобразуем значения из csv в понятный для библиотеки формат
x = data['Date'].to_numpy()
y = data['Sales'].to_numpy()


# даем название осям и графику
plt.xlabel('Дата')
plt.ylabel('Продажи')
plt.title('Анализ продаж за 2019 год')

# рисуем точки
plt.plot(x, y)

# показываем график
plt.show()