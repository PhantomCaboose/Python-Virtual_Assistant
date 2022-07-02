import datetime, random, os, playsound, main

###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
path = "././sounds/alarm/"
all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
randomfile = random.choice(all_mp3)
def validate_time(alarm_time):
    if len(alarm_time) != 8:
        return "Invalid time format! Please try again..."
    else:
        if int(alarm_time[0:2]) > 12:
            return "Invalid HOUR format! Please try again..."
        elif int(alarm_time[3:5]) > 59:
            return "Invalid MINUTE format! Please try again..."
        else:
            return "ok"

def alarm(query):
    while True:
        alarm_time = query.split('for ')[1].upper()
        if int(alarm_time[0]) > 1:
            alarm_time = "0" + alarm_time
        elif int(alarm_time[0]) == 1 and alarm_time[1] == ":":
            alarm_time = "0" + alarm_time
        elif int(alarm_time[0]) == 0:
            alarm_time = alarm_time

        validate = validate_time(alarm_time.lower())
        if validate != "ok":
            print(validate)
        else:
            print(f"Setting alarm for {alarm_time}...")
            main.speak(f"Setting alarm for {alarm_time}...")
            break
    alarm_hour = alarm_time[0:2]
    alarm_min = alarm_time[3:5]
    alarm_period = alarm_time[6:].upper()

    while True:
        now = datetime.datetime.now()

        current_hour = now.strftime("%I")
        current_min = now.strftime("%M")
        current_period = now.strftime("%p")

        if alarm_period == current_period:
            if alarm_hour == current_hour:
                if alarm_min == current_min:
                    print("Wake Up!")
                    playsound.playsound(randomfile)
                    playsound.playsound(randomfile)
                    playsound.playsound(randomfile)
                    break
