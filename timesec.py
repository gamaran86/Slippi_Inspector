
# Change time from sentisecs min, sec, centisecs
# init time is 8 min 3 sec

def convert_to_frame(hour,min,sec,cs):
    f_hour = hour*60*60*60
    f_min = min*60*60
    f_sec = sec*60
    f_cs = cs /100 * 60
    return f_hour + f_min + f_sec + f_cs

def convert_f_to_time(f):
    hour = f // (60*60*60)
    f_min = f % (60*60*60)

    min = f_min // (60*60)
    f_sec = f_min % (60*60)

    tsec = f_sec / 60

    sec = int(str(tsec).split('.')[0])

    cs = int(round(float('0.'+str(tsec).split('.')[1]),2)*100)

    return (hour,min,sec,cs)

def format_time(hour,min,sec,cs):
    formatted_time_str = str()
    if hour == 0:
        hour = '00'
    elif 0<hour<=9:
        hour = '0'+ str(int(hour))
    else:
        hour=str(hour)

    if min == 0:
        min = '00'
    elif 0<min<=9:
        min = '0'+ str(int(min))
    else:
        min=str(int(min))

    if sec == 0:
        sec = '00'
    elif 0<sec<=9:
        sec = '0'+ str(int(round(sec)))
    else:
        sec=str(int(round(sec)))

    if cs == 0:
        cs = '00'
    elif 0<cs<=9:
        cs = '0'+ str(int(round(cs,0)))
    else:
        cs=str(int(round(cs,0)))

    return hour + ':' + min + ':' + sec + ' ' + cs
"""
endtime = convert_to_cs(0,5,10,86)
print(endtime)

timepause = endtime - 116 * 100 / 60
print(timepause)

timeinit = 48300
timeinitend = convert_to_cs(0,5,11,80)
print(timeinitend)

delta = timeinitend - timepause
print(delta)
start = timeinit - delta
print(start)
print(format_time(*convert_cs_to_time(start)))
"""
