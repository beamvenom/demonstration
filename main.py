from datetime import datetime, timedelta


def timeInRange(start, end, x):
    return start <= x <= end


def intPrompt(text=""):
    print(text);
    intAnswer = None;
    while intAnswer is None:
        answer = input();
        try:
            intAnswer = int(answer)
        except ValueError or TypeError:
            print("Try again. Write a number");
    return intAnswer


def inputDate(text="", format='%Y-%m-%d %H:%M', formatText='(Format: YYYY-MM-DD hh:mm)'):
    print(f"-------{text} {formatText}-------");
    result = None;
    while result is None:
        answer = input();
        try:
            result = datetime.strptime(answer, format);
        except ValueError:
            print(ValueError(f"Incorrect format, Try again\n-------{text} {formatText}-------"))
    return result


def loadSchedule(fileDestination):
    busyDic = {}
    with open(fileDestination) as file:
        for line in file:
            line = line.split(";")
            if len(line) == 4:
                try:
                    busyTime = [datetime.strptime(line[1], '%m/%d/%Y %I:%M:%S %p'),
                                datetime.strptime(line[2], '%m/%d/%Y %I:%M:%S %p')]
                except ValueError:
                    print(ValueError("Line removed due to incorrect data format: {} to {}".format(line[1], line[2])));
                if line[0] in busyDic:
                    busyDic[line[0]].append(busyTime)
                else:
                    busyDic[line[0]] = [busyTime]
    return busyDic


def getBusyTimes(busyDic, startDate, endDate):
    count = 0;
    personNbr = input(f'-------Ange anställningsnummer (Person {count + 1})(Blankt svar för att fortsätta)-------\n')
    busyTimes = [];
    while personNbr != "" or count < 1:
        if personNbr in busyDic:
            for busyTime in busyDic[personNbr]:
                if timeInRange(startDate, endDate, busyTime[0]) or timeInRange(startDate, endDate, busyTime[1]):
                    busyTimes.append(busyTime)
            del busyDic[personNbr]
            count += 1
        else:
            print("Den personen är redan tilllagd ELLER finns inte på systemet")
        personNbr = ""
        personNbr = input(f'-------Ange anställningsnummer (Person {count + 1})(Blankt svar för att fortsätta)-------\n')
    return busyTimes

def correctDates(officeStart,officeEnd, startDate,endDate):
    if startDate.hour < officeStart.hour:
        startDate = startDate.replace(hour=officeStart.hour, minute=officeStart.minute)
    if endDate.hour >= officeEnd.hour:
        endDate = endDate.replace(hour=officeEnd.hour, minute=officeEnd.minute)
    return startDate, endDate

def findTime(busyTimes, officeStart, officeEnd, startDate, endDate, duration):
    testTime = startDate;
    found = False;
    while found == False:
        found = True;
        for busyTime in busyTimes:
            if timeInRange(busyTime[0], busyTime[1], testTime) or timeInRange(busyTime[0], busyTime[1],
                                                                              testTime + timedelta(minutes=duration)):
                testTime = testTime.replace(hour=busyTime[1].hour, minute=busyTime[1].minute) + timedelta(minutes=30)
                if testTime >= datetime(testTime.year, testTime.month, testTime.day, officeEnd.hour, officeEnd.minute):
                    testTime += timedelta(days=1)
                    testTime = testTime.replace(hour=officeStart.hour, minute=officeStart.minute)
                    found = False
                    break
    if testTime >= endDate:
        return "No Time Found"
    return f"-------Found Time is: {testTime} to {testTime + timedelta(minutes=duration)}-------"

if __name__ == '__main__':
    busyDic = loadSchedule("freebusy.txt")
    officeStart = inputDate("Kontorets Öppningstid", '%H:%M', '(Format: hh:mm)')
    officeEnd = inputDate("Kontorets Stängnigstid", '%H:%M', '(Format: hh:mm)')
    startDate = inputDate("Tidigaste mötesdatum")
    endDate = inputDate("Senaste mötesdatum")
    duration = intPrompt("-------Hur många minuter varar mötet?-------")
    busyTimes = getBusyTimes(busyDic, startDate, endDate)
    startDate, endDate = correctDates(officeStart, officeEnd, startDate, endDate)
    print(findTime(busyTimes, officeStart, officeEnd, startDate, endDate, duration))
