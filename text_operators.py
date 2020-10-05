from datetime import datetime


def read_file(input_file_txt):
    file = open(input_file_txt, "r", encoding='utf-8')
    red_lines = file.readlines()
    processing_data = ''
    for x in range(len(red_lines)):
        processing_data = processing_data + ' ' + red_lines[x]
    #    print(processing_data)
    file.close()
    return processing_data


def analyse_content(text):
    delimetr = ' '
    # Получаем спиок слов разделенных пробелом
    text_units = text.split(delimetr)
    # Получаем список уникальных слов из текста
    uniq_words = filtr_uniq(text_units)
    word_count = []
    all_words_count = len(text_units)
    uniq_words_count = len(uniq_words)
    word_count.append(all_words_count)
    word_count.append(uniq_words_count)
    print("Всего слов = "+str(all_words_count))
    print("Уникальных слов = "+str(uniq_words_count))
    analyse_result = []
    for word in range(len(uniq_words)):
        analyse_result.append(
            'количесвто включений слова"' + str(uniq_words[word]) + '" =' + str(text_units.count(uniq_words[word])))
    return uniq_words, text_units, analyse_result, all_words_count


def filtr_uniq(spisok):
    spisok_unik = []
    for x in range(len(spisok)):
        if spisok_unik.count(spisok[x]) < 1:
            spisok_unik.append(spisok[x])
    return spisok_unik


def write_result_in_file(file_path_to_write, content_data):
    date = datetime.now()
    #Если вместо "w" поставить "а", то будет добавлять в файл, а не перезаписывать
    file = open(file_path_to_write, "w", encoding='utf-16')
    file.write('дата записи: ' + str(date) + '\n')
    for e in range(len(content_data)):
        file.write(content_data[e] + '\n')
    file.close()
