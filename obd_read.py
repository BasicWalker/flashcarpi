import obd

def get_speed(s):
    global speed
    if not s.is_null():
        speed = int(s.value.magnitude * 0.060934)  # MPH conversion

def get_rpm(r):
	global rpm
	if not r.is_null():
		rpm = int(r.value.magnitude)