import csv
import os.path
#import pandas as pd
from csv import DictReader, DictWriter
from datetime import datetime


class TitleError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NoteTextError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    is_valid_title = False
    while not is_valid_title:
        try:
            title = input("Введите тему заметки: ")
            if len(title) < 1:
                raise TitleError("Заметка должна иметь тему")
            else:
                is_valid_title = True
        except TitleError as err:
            print(err)
            continue

    is_valid_note_text = False
    while not is_valid_note_text:
        try:
            note_text = input("Введите текст заметки: ")
            if len(note_text) < 1:
                raise NoteTextError("Заметка не содержит информации")
            else:
                is_valid_note_text = True
        except NoteTextError as err:
            print(err)
            continue

    note_time = str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    return [title, note_text, note_time]


def create_file(file_name):
    with open(file_name, "w", encoding='utf-8') as notes:
        f_writer = DictWriter(notes, fieldnames=['ID', 'Topic', 'Note', 'Date'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_note(file_name, lst):
    res = read_file(file_name)
    if(len(res)==0):
        id_of_note = 1
    else:
        id_of_note = int(get_last_id(file_name)) + 1

    new_note = {'ID': id_of_note, 'Topic': lst[0], 'Note': lst[1], 'Date': lst[2]}
    res.append(new_note)
    with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
        f_writer = DictWriter(csvfile, fieldnames=['ID', 'Topic', 'Note', 'Date'])
        f_writer.writeheader()
        for row in res:
            f_writer.writerow(row)


def get_last_id(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            last_id = row['ID']
    return last_id

def find_note_id(file_name, find_by):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['ID']==find_by):
                return row

def find_notes_by_topic(file_name, topic_to_find):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        notes_with_topic=[]
        for row in reader:
            if (row['Topic'] == topic_to_find):
                notes_with_topic.append(row)
        return notes_with_topic




def main():
    file_name = 'List_of_notes.csv'
    if not os.path.exists(file_name):
        create_file(file_name)
    print("Программа для работы с заметками")
    while True:
        print("Команды:"
              "\n1 - создать заметку"
              "\n2 - показать все заметки"
              "\n3 - найти заметку по ID"
              "\n4 - показать все заметки по теме"
              "\n5 - редактировать заметку"
              "\n6 - удалить заметку"
              "\n7 - завершить работу")
        command = input("Введите команду: ")
        if command == "7":
            break
        elif command == '1':
            write_note(file_name, get_info())
        elif command == '2':
            print("ID    Topic        Note          Date   ")
            with open(file_name, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row['ID'], row['Topic'], row['Note'], row['Date'])
        elif command == '3':
            id_to_find = input("Укажите ID: ")
            note_with_id = find_note_id(file_name, id_to_find)
            if(note_with_id == None):
                print(f"Заметка с ID {id_to_find} не найдена!")
            else:
                print(note_with_id)

        elif command == '4':
            topic_to_find = input("Укажите тему заметки: ")
            notes_with_topic = find_notes_by_topic(file_name, topic_to_find)
            if(len(notes_with_topic)==0):
                print(f"Заметок по теме {topic_to_find} не найдено")
            else:
                print("ID    Topic        Note          Date   ")
                with open(file_name, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for note in notes_with_topic:
                        print(note['ID'], note['Topic'], note['Note'], note['Date'])


        elif command == '5':
            note_to_change = input("Укажите ID заметки, которую требуетмя отредактировать: ")
            list_of_notes = read_file(file_name)
            for note in list_of_notes:
                if (note['ID']==note_to_change):
                    note['Topic'] = input("Укажите тему заметки: ")
                    note['Note'] = input("Введите текст заметки: ")
                    note['Date'] = str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

            with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
                f_writer = DictWriter(csvfile, fieldnames=['ID', 'Topic', 'Note', 'Date'])
                f_writer.writeheader()
                for row in list_of_notes:
                    f_writer.writerow(row)

        elif command == '6':
            note_to_del = input("Укажите ID заметки, которую требуетмя удалить: ")
            list_of_notes = read_file(file_name)
            for note in list_of_notes:
                if(note['ID']==note_to_del):
                    list_of_notes.remove(note)
                    print(f"Заметка с ID {note_to_del} удалена")
            with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
                f_writer = DictWriter(csvfile, fieldnames=['ID', 'Topic', 'Note', 'Date'])
                f_writer.writeheader()
                for row in list_of_notes:
                    f_writer.writerow(row)


main()
