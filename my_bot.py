# -*- coding: utf-8 -*-

class TextBot():
    def __init__(self, input):
        self.bot_name = 'Jake'
        self.voice = 'no'
        self.input = input
        self.output = ''
        self.bot_wocabulary = []
        self.bot_dialog_memory =''
        self.openent_name =''

    def answer_the_question(self):
        series_init = ['...']
        series_yes = ['да', 'да!', 'yes']
        series_no = ['нет', 'нет!', 'no']
        series_agree = ['ok', 'давай', 'ok!', 'ok', 'да', 'конечно']
        series_hello = ['привет', 'hi', 'здарова']
        series_yana = ['яна', 'yana', 'my name is yana', 'я яна', 'меня зовут яна']
        series_sergey = ['Сергей', 'Sergey', 'my name is Sergey', 'я Сергей', 'меня зовут Сергей', 'Серега']
        series_how_are_you = ['как дела', 'как дела?', 'как твои дела?']
        series_what_abilities = ['что ты умеешь?', 'что ты можешь?', 'что умеешь?', 'что умеешь', 'что ты умеешь', 'что ты можешь']
        known_phrase_counter = 0
        flag_empty = 0

        #Запись фразы в словарь бота
        self.bot_wocabulary.append(self.input.lower())

        #Запись сказанной боту фразы в log память бота
        self.bot_dialog_memory=self.bot_dialog_memory+str(self.openent_name)+':'+self.input.lower()

        #Начальное приветственое слово бота при подаче в текстовый ввод "..."
        for x in range(len(series_init)):
            if self.input.lower() == series_init[x]:
                known_phrase_counter = 1
                self.output = 'Поболтаем?'

        for x in range(len(series_yes)):
            if flag_empty == 1 and self.input.lower() == series_yes[x]:
                known_phrase_counter = 1
                self.output='Меня не надуришь, задницу свою дури, давай спроси что-нибудь толковое'
                flag_empty = 0

        for x in range(len(series_no)):
            if flag_empty == 1 and self.input.lower() == series_no[x]:
                known_phrase_counter = 1
                self.output='ах так ну тогда давай спроси что-нибудь толковое!'
                flag_empty = 0
        if self.input.lower() == '' :
            known_phrase_counter=1
            self.output = 'Ничего не написал, решил надурить меня?'
            flag_empty = 1

        for x in range(len(series_hello)):
            if self.input.lower() == series_hello[x]:
                self.output = 'Привет, как дела?'

        for x in range(len(series_how_are_you)):
            if self.input.lower() == series_how_are_you[x]:
                self.output = 'У мена хорошо'

        for x in range(len(series_what_abilities)):
            if self.input.lower == series_what_abilities[x]:
                known_phrase_counter = 1
                self.output = 'Я умею обрабатывать данные и говорить, что именно вам нужно?'


        # Ответ бота, если с ним захотели с ним поговорить
        if self.output == 'Поболтаем?':
            for x in range(len(series_agree)):
                if self.input.lower() == series_agree[x]:
                    known_phrase_counter = 1
                    self.output = 'начнем с знакомства наверно, я Jake, а как тебя зовут?'
            # Если боту сказали свое имя
        if self.output == 'начнем с знакомства наверно, я Jake, а как тебя зовут?':
            for x in range(len(series_yana)):
                if self.input.lower() == series_yana[x]:
                    known_phrase_counter = 1
                    self.output = 'Яна очень приятно познакомиться, какое красивое имя!'
                    self.oponent_name = 'Яна'
            for x in range(len(series_sergey)):
                if self.input.lower() == series_sergey[x]:
                    known_phrase_counter = 1
                    self.output = 'Сергей привет, как дела?'
                    self.oponent_name = 'Сергей'
            if known_phrase_counter == 0:
                    self.oponent_name = self.input
                    self.output = self.input + ' очень приятно познакомиться, какое красивое имя!'
        else:
            # Ответ бота, если он не увидел знакомых слов
            if known_phrase_counter == 0:
                self.output = 'Я такого не знаю, спроси чего полегче'
            else:
                pass
        # Запись перевода на новую строку и ответа в log память бота
        self.bot_dialog_memory = self.bot_dialog_memory + '\n'
        self.bot_dialog_memory = self.bot_dialog_memory + self.bot_name + ':' + self.output
        self.bot_dialog_memory = self.bot_dialog_memory + '\n'