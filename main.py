from datetime import datetime, timedelta
import main
import pytest
import tempfile
import os

def time_in_range(start, end, x):
    return start <= x <= end


def int_prompt(text=""):
    print(text);
    int_answer = None;
    while int_answer is None:
        answer = input();
        try:
            int_answer = int(answer)
        except ValueError or TypeError:
            print("Try again. Write a number");
    return int_answer


def input_date(text="", format='%Y-%m-%d %H:%M', formatText='(Format: YYYY-MM-DD hh:mm)'):
    print(f"-------{text} {formatText}-------");
    result = None;
    while result is None:
        answer = input();
        try:
            result = datetime.strptime(answer, format);
        except ValueError:
            print(ValueError(f"Incorrect format, Try again\n-------{text} {formatText}-------"))
    return result


def load_schedule(file_destination):
    busy_dic = {}
    with open(file_destination) as file:
        for line in file:
            line = line.split(";")
            if len(line) == 4:
                try:
                    busy_time = [datetime.strptime(line[1], '%m/%d/%Y %I:%M:%S %p'),
                                datetime.strptime(line[2], '%m/%d/%Y %I:%M:%S %p')]
                except ValueError:
                    print(ValueError(f"Line removed due to incorrect data format: {line[1]} to {line[2]}"));
                if line[0] in busy_dic:
                    busy_dic[line[0]].append(busy_time)
                else:
                    busy_dic[line[0]] = [busy_time]
    return busy_dic
def get_person_nbr_list(busy_dic):
    count = 0;
    person_nbr = input(f'-------Give Work Number (Person {count + 1})(Blank answer to continue)-------\n')
    person_nbr_list = [];
    while person_nbr != "" or count < 1:
        if person_nbr in busy_dic and person_nbr not in person_nbr_list:
            person_nbr_list.append(person_nbr)
            count += 1
        else:
            print("That person has already been added, or is not in the system")
        person_nbr = input(f'-------Give Work Number (Person {count + 1})(Blank answer to continue)-------\n')
    return person_nbr_list

def get_busy_times(busy_dic,person_nbr_list, start_date, end_date):
    busy_times = [];
    for person_nbr in person_nbr_list:
        for busy_time in busy_dic[person_nbr]:
            if time_in_range(start_date, end_date, busy_time[0]) or time_in_range(start_date, end_date, busy_time[1]):
                busy_times.append(busy_time)
    return busy_times

def correct_dates(office_start, office_end, start_date, end_date):
    if start_date.hour < office_start.hour:
        start_date = start_date.replace(hour=office_start.hour, minute=office_start.minute)
    if end_date.hour >= office_end.hour:
        end_date = end_date.replace(hour=office_end.hour, minute=office_end.minute)
    return start_date, end_date

def find_time(busy_times, office_start, office_end, start_date, end_date, duration):
    test_time = start_date;
    found = False;
    while found == False:
        found = True;
        for busy_time in busy_times:
            if time_in_range(busy_time[0], busy_time[1], test_time) or time_in_range(busy_time[0], busy_time[1],
                                                                              test_time + timedelta(minutes=duration)):
                test_time = test_time.replace(hour=busy_time[1].hour, minute=busy_time[1].minute) + timedelta(minutes=30)
                if test_time >= datetime(test_time.year, test_time.month, test_time.day, office_end.hour, office_end.minute):
                    test_time += timedelta(days=1)
                    test_time = test_time.replace(hour=office_start.hour, minute=office_start.minute)
                    found = False
                    break
    if test_time >= end_date:
        return "No Time Found"
    return f"-------Found Time is: {test_time} to {test_time + timedelta(minutes=duration)}-------"

if __name__ == '__main__':
    busy_dic = load_schedule("freebusy.txt")
    office_start = input_date("Office's Opening Hour", '%H:%M', '(Format: hh:mm)')
    office_end = input_date("Office's Closing Hour", '%H:%M', '(Format: hh:mm)')
    start_date = input_date("Earliest Meeting Date")
    end_date = input_date("Latest Meeting Date")
    duration = int_prompt("-------The Meetings Duration in Minutes-------")
    person_nbr_list = get_person_nbr_list(busy_dic)
    busy_times = get_busy_times(busy_dic,person_nbr_list, start_date, end_date)
    start_date, end_date = correct_dates(office_start, office_end, start_date, end_date)
    print(find_time(busy_times, office_start, office_end, start_date, end_date, duration))
