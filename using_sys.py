# Это мой список покупок
shoplist = ['яблоки', 'манго', 'морковь', 'бананы']
print('Я должен сделать', len(shoplist), 'покупки.')
print('Покупки:', end=' ')
for item in shoplist:
    if shoplist.__getitem__(len(shoplist)-1) == item:
        print(item, end='. ')
    else:
        print(item, end=', ')

print('\nТакже нужно купить риса.')
shoplist.append('рис')
print('Теперь мой список покупок таков:', shoplist)
print('Отсортирую-ка я свой список')
shoplist.sort()
print('Отсортированный список покупок выглядит так:', shoplist)
print('Первое, что мне нужно купить, это', shoplist[0])
olditem = shoplist[0]
del shoplist[0]
print('Я купил', olditem)
print('Теперь мой список покупок:')
for item in shoplist:
    if shoplist.__getitem__(len(shoplist)-1) == item:
        print(item, end='. ')
    else:
        print(item, end=', ')

# 'ab' - сокращение от 'a'ddress'b'ook
ab = { 'Swaroop' : 'swaroop@swaroopch.com',
        'Larry' : 'larry@wall.org',
        'Matsumoto' : 'matz@ruby-lang.org',
        'Spammer' : 'spammer@hotmail.com'
    }
print("Адрес Swaroop'а:", ab['Swaroop'])
# Удаление пары ключ-значение
del ab['Spammer']
print('\nВ адресной книге {0} контакта\n'.format(len(ab)))
for n, a in ab.items():
    print('Контакт {0} с адресом {1}'.format(n, a,))
# Добавление пары ключ-значение
if 'Larry' in ab:
    print('Такой уже ест!')
else:
    ab['Larry'] = 'guido@python.org'
if 'Larry' in ab:
    print("\nАдрес Larry:", ab['Larry'])