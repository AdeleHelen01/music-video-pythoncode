from pythonosc import udp_client

from evdev import InputDevice,list_devices, categorize, ecodes, KeyEvent
client = udp_client.SimpleUDPClient("10.106.39.28",8001)

gamepad = InputDevice(list_devices()[0])

CENTER_TOLERANCE = 350
STICK_MAX = 65536


axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

for event in gamepad.read_loop():
	
	if event.type == ecodes.EV_KEY:
		keyevent = categorize(event)
		print(keyevent)
		#SEND OSC TO UNREAL
		if keyevent.keystate == KeyEvent.key_down:
			if keyevent.scancode == 288:
					print('RED')
					client.send_message("/red", 5)
			elif keyevent.scancode == 289:
					print('GREEN')
			elif keyevent.scancode == 290:
					print('BLUE')
					client.send_message("/blue", 5)
			elif keyevent.scancode == 291:
					print('YELLOW')
					
			elif keyevent.scancode == 292:
					print('WHITE')	
					client.send_message("/white", 5)			
	 #read stick axis movement
	elif event.type == ecodes.EV_ABS:
		
		if axis[ event.code ] in [ 'ls_x', 'ls_y', 'rs_x', 'rs_y' ]:
			last[ axis[ event.code ] ] = event.value

			value = event.value - center[ axis[ event.code ] ]

			if abs( value ) <= CENTER_TOLERANCE:
				value = 0

			#if axis[ event.code ] == 'rs_x':
				#if value < 0:
					#print('left')
					
				#else:
					#print('right')
				#print( value )
			elif axis[ event.code ] == 'ls_y':
				if value < 0:
					print('foreward')
					client.send_message("/Joystick", 5)
				else:
					print('backward')
				print( value )
				
