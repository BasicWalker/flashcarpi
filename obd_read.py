import obd

def get_speed(s):
    global speed
    if not s.is_null():
        sspeed = int(s.value.to("mph").magnitude)  # MPH conversion

def get_rpm(r):
    global rpm1
    if not r.is_null():
        rpm1 = int(r.value.magnitude)
