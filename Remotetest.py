import RPi.GPIO as gpio
gpio.cleanup()

gpio.setmode(gpio.BCM)

clock_wise_button=21
anti_clock_wise_button=16
forward_button=4

left_motor_f=17 #IN3
left_motor_r=18 #IN4
right_motor_r=19 #IN2
right_motor_f=20 #IN1


gpio.setup(clock_wise_button, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(anti_clock_wise_button, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(forward_button, gpio.IN, pull_up_down=gpio.PUD_DOWN)

gpio.setup(left_motor_f,gpio.OUT)
gpio.setup(left_motor_r,gpio.OUT)
gpio.setup(right_motor_f,gpio.OUT)
gpio.setup(right_motor_r,gpio.OUT)

gpio.output(left_motor_f,gpio.HIGH)
gpio.output(right_motor_f,gpio.HIGH)
gpio.output(left_motor_r,gpio.HIGH)
gpio.output(right_motor_r,gpio.HIGH)

                                
while True:


    
    if((gpio.input(forward_button) == 1) and (gpio.input(anti_clock_wise_button)==0) and (gpio.input(clock_wise_button)==0)):
        print("moving forward")
        gpio.output(left_motor_f,gpio.LOW)
        gpio.output(right_motor_f,gpio.LOW)

        gpio.output(left_motor_r,gpio.HIGH)
        gpio.output(right_motor_r,gpio.HIGH)
        
    elif((gpio.input(anti_clock_wise_button) == 1) and (gpio.input(forward_button)==0) and (gpio.input(clock_wise_button)==0)) :
        print("moving antickws")
        gpio.output(left_motor_f,gpio.LOW)
        gpio.output(right_motor_r,gpio.LOW)

        gpio.output(left_motor_r,gpio.HIGH)
        gpio.output(right_motor_f,gpio.HIGH)
        
    elif((gpio.input(clock_wise_button) == 1) and (gpio.input(forward_button)==0) and (gpio.input(anti_clock_wise_button)==0)):
        print("moving ckws")
        gpio.output(left_motor_r,gpio.LOW)
        gpio.output(right_motor_f,gpio.LOW)

        gpio.output(left_motor_f,gpio.HIGH)
        gpio.output(right_motor_r,gpio.HIGH)
        
    else:
        gpio.output(left_motor_f,gpio.HIGH)
        gpio.output(right_motor_f,gpio.HIGH)
        gpio.output(left_motor_r,gpio.HIGH)
        gpio.output(right_motor_r,gpio.HIGH)
    

gpio.cleanup()
