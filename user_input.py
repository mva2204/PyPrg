import string

def reverse(text):
    return text[::-1]

def delpunctuation(text):
    #Формируем макет для translate всех символов пунктуации string.punctuation
    tt=str.maketrans(dict.fromkeys(string.punctuation))
    print('Dict', dict.fromkeys(string.punctuation))
    print('ее', tt)
    #Удаляем все символы пунктуации и пробелы
    return ''.join(text.translate(tt).split()).lower()


def is_palindrome(text):
    return text == reverse(text)


something = 'А роза упала?, на,. лапу Азора!'
#    input('Введите текст: ')
text=delpunctuation(something)
if (is_palindrome(text)):
    print("Да, это палиндром")
else:
    print("Нет, это не палиндром")
#А роза упала?, на,. лапу Азора!