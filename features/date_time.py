###########################################################
#------------------------ IMPORTS ------------------------#
###########################################################
import datetime

###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
def get_time():
    current_hour = datetime.datetime.now().hour
    AM_PM = "A.M."
    if 12 <= current_hour <= 23:
        current_hour = current_hour - 12
        AM_PM = "P.M."
    elif current_hour == 24:
        current_hour = current_hour - 12
    elif current_hour == 0:
        current_hour = current_hour + 12
        AM_PM = "A.M."
    current_minute = datetime.datetime.now().minute
    if 9 >= current_minute >= 1:
        current_minute = "O" + str(current_minute)
    current_time = f"{current_hour} {current_minute} {AM_PM}"
    return current_time

def get_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    weekday = datetime.datetime.now().weekday() + 1
    day = datetime.datetime.now().day

    Day_dict = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
                6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'nineth', 10: 'tenth',
                11: 'eleventh', 12:'twelveth', 13: 'thirteenth', 14: 'fourteenth', 15: 'fifteenth',
                16: 'sixteenth', 17: 'seventeenth', 18: 'eighteenth', 19: 'nineteenth', 20: 'twentieth',
                21: 'twenty-first', 22: 'twenty-second', 23: 'twenty-third', 24: 'twenty-fourth',
                25: 'twenty-fifth', 26: 'twenty-sixth', 27: 'twenty-seventh', 28: 'twenty-eighth',
                29: 'twenty-nineth', 30: 'thirtieth', 31: 'thirty-first'}

    Weekday_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    Month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                  5: 'May', 6: 'June', 7: 'July', 8: 'August',
                  9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    if weekday in Weekday_dict.keys():
        weekday_of_the_month = Weekday_dict[weekday]
    if month in Month_dict.keys():
        month_of_the_year = Month_dict[month]
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]

    return f"{weekday_of_the_month}, {month_of_the_year} {day_of_the_week}, {year}"