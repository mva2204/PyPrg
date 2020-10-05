from text_operators import read_file, analyse_content, write_result_in_file
from my_bot import TextBot
from tkinter import *


# output_file_path = 'output.txt'
# text_to_analyse = read_file('input_text.txt')
#
# uniq_words, text_units, analyse_result, all_words_count = analyse_content(text_to_analyse)
#
#
# write_result_in_file(output_file_path, analyse_result)
def show_answer():
    jake.input = message_entry.get()
    jake.answer_the_question()
    txt.insert(END, '\n')
    txt.insert(END, jake.output)


jake = TextBot('...')
jake.answer_the_question()

root = Tk(screenName='Бот', baseName='Имя бота Джейк' )
txt = Text(root, width=50, height=50, font=12)
txt.pack()

txt.insert(END, jake.output)

message_entry = Entry()
message_entry.place(relx=.5, rely=0.9, anchor='c')

message_button = Button(text='Answer', command=show_answer)
message_button.place(relx=.7, rely=0.9, anchor='c')

root.mainloop()
