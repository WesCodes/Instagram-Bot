import time

def countdown(t, header = None):
    """
    counts down 00:00 format in console

    t - times in seconds
    header - you can give header to timer
             ex: 'Time to Launch: 00:00'
    """
    while t >= 0:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)

        if header:
            timeformat = header + ": " + timeformat
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print()

