from datetime import datetime, date
import time
import RPi.GPIO as gpio
import csv
import os

opt_sensor_pin = 17
reed1_pin = 27
reed2_pin = 22
reed3_pin = 18

accepted_low_time = 20 #ile czasu moze byc stan niski zeby nie liczyc postoju

#zmienne do czujnika optycznego
start_optical = None
stop_optical = None
start_time_main = datetime.now()
first_time=True
optical_cycle_time = None
cycle30_optical = []
avr30_optical = None
cycle_1shift_optical = []
avr_1shift_optical = None
cycle_2shift_optical = []
avr_2shift_optical = None
cycle_3shift_optical = []
avr_3shift_optical = None

#zmienne do czujnika reed1
start_reed1 = None
stop_reed1 = None
first_time_reed1=True
reed1_cycle_time = None
cycle30_reed1 = []
avr30_reed1 = None
cycle_1shift_reed1 = []
avr_1shift_reed1 = None
cycle_2shift_reed1 = []
avr_2shift_reed1 = None
cycle_3shift_reed1 = []
avr_3shift_reed1 = None

#zmienne do czujnika reed2
start_reed2 = None
stop_reed2 = None
first_time_reed2=True
reed2_cycle_time = None
cycle30_reed2 = []
avr30_reed2 = None
cycle_1shift_reed2 = []
avr_1shift_reed2 = None
cycle_2shift_reed2 = []
avr_2shift_reed2 = None
cycle_3shift_reed2 = []
avr_3shift_reed2 = None

#zmienne do czujnika reed3
start_reed3 = None
stop_reed3 = None
first_time_reed3=True
reed3_cycle_time = None
cycle30_reed3 = []
avr30_reed3 = None
cycle_1shift_reed3 = []
avr_1shift_reed3 = None
cycle_2shift_reed3 = []
avr_2shift_reed3 = None
cycle_3shift_reed3 = []
avr_3shift_reed3 = None

#zmienne do liczenie czasu postoju
high_start_reed3 = None
delay_reed3 = None
previous_state_reed3 = 0

high_start_reed2 = None
delay_reed2 = None
previous_state_reed2 = 0

high_start_reed1 = None
delay_reed1 = None
previous_state_reed1 = 0

def op_sensor_rising_detect(opt_sensor_pin):
    print("Opt Sensor rising edge detected!")
    global first_time 
    if first_time == True: #to zadziala tylko przy pierwszym wejsciu
        print("first time!")
        global start_optical
        start_optical = datetime.now()
        #global first_time
        first_time = False
    else: #dla kazdego kolejnego zbocza
        global stop_optical
        stop_optical = datetime.now()
        print("stop optical : {}".format(stop_optical))
        #global start_optical
        print("start optical : {}".format(start_optical))
        global optical_cycle_time
        optical_tmp = stop_optical - start_optical
        if optical_tmp.seconds >= 6.5 :
            optical_cycle_time = optical_tmp
            #liczenie sredniej dla 30 pomiarow
            global cycle30_optical
            if len(cycle30_optical) < 30:
                cycle30_optical.append(optical_cycle_time)
            else:
                global avr30_optical
                sum30 = 0
                for cycle in cycle30_optical:
                    sum30 = sum30 + cycle.seconds
                avr30_optical = sum30 / 30
                cycle30_optical = []
                cycle30_optical.append(optical_cycle_time)
            
            #licznie sredniej dla calej zmiany
            actual_hour = stop_optical.hour
            if actual_hour >= 6 and actual_hour <= 14:
                global cycle_1shift_optical
                global avr_1shift_optical
                global cycle_2shift_optical
                global avr_2shift_optical
                global cycle_3shift_optical
                global avr_3shift_optical
                #zerowanie elementow z poprzednich zmian
                cycle_2shift_optical = []
                avr_2shift_optical = 0
                cycle_3shift_optical = []
                avr_3shift_optical = 0
                
                cycle_1shift_optical.append(optical_cycle_time)
                sum1 = 0
                
                for cycle1 in cycle_1shift_optical:
                    sum1 = sum1 + cycle1.seconds
                    
                avr_1shift_optical = sum1 / len(cycle_1shift_optical)
                
            elif actual_hour >14 and actual_hour <=22:
                #global cycle_1shift_optical
                #global avr_1shift_optical
                #global cycle_2shift_optical
                #global avr_2shift_optical
                #global cycle_3shift_optical
                #global avr_3shift_optical
                #zerowanie elementow z poprzednich zmian
                cycle_1shift_optical = []
                avr_1shift_optical = 0
                cycle_3shift_optical = []
                avr_3shift_optical = 0
                
                cycle_2shift_optical.append(optical_cycle_time)
                sum2 = 0
                
                for cycle2 in cycle_2shift_optical:
                    sum2 = sum2 + cycle2.seconds
                    
                avr_2shift_optical = sum2 / len(cycle_2shift_optical)
                
            elif actual_hour >22 and actual_hour <6:
                #global cycle_1shift_optical
                #global avr_1shift_optical
                #global cycle_2shift_optical
                #global avr_2shift_optical
                #global cycle_3shift_optical
                #global avr_3shift_optical
                
                #zerowanie elementow z poprzednich zmian
                cycle_1shift_optical = []
                avr_1shift_optical = 0
                cycle_2shift_optical = []
                avr_2shift_optical = 0
                
                cycle_3shift_optical.append(optical_cycle_time)
                sum3 = 0
                
                for cycle3 in cycle_3shift_optical:
                    sum3 = sum3 + cycle3.seconds
                    
                avr_3shift_optical = sum3 / len(cycle_3shift_optical)
            
            #zapis do pliku csv
            try:
                with open('/media/CYKL/optical.csv', 'a') as csvfile:
                    optical_csv = csv.writer(csvfile, delimiter=';')
                    optical_csv.writerow([stop_optical, optical_cycle_time, avr30_optical, avr_1shift_optical, avr_2shift_optical, avr_1shift_optical])    
            except Exception as err:
                print("Cannot open the file")
                print(str(err))
               
            start_optical = stop_optical
        else:
            print("Not count! To short time")
    
    

def reed1_falling_detect(reed1_pin):
    print("reed1 sensor falling edge detected!")
    global first_time_reed1
    if first_time_reed1 == True: #to zadziala tylko przy pierwszym wejsciu
        print("first time!")
        global start_reed1
        start_reed1 = datetime.now()
        #global first_time_reed1
        first_time_reed1 = False
    else: #dla kazdego kolejnego zbocza
        global stop_reed1
        stop_reed1 = datetime.now()
        
        #liczenie czasu postoju
        global previous_state_reed1
        previous_state_reed1 = not previous_state_reed1
        delay_reed1_tmp = stop_reed1 - high_start_reed1
        if delay_reed1_tmp.seconds > accepted_low_time:
            delay_reed1 = delay_reed1_tmp
            print("reed1 delay is {}".format(delay_reed1))
            actual_date = date.today()
            try:
                with open('/home/pi/Public/delay.csv', 'a') as csvfile:
                    delay_csv = csv.writer(csvfile, delimiter=';')
                    delay_csv.writerow([actual_date, delay_reed1, 0, 0])
            except Exception as err:
                print("Cannot open the file")
                print(str(err))
        
        print("stop reed1 : {}".format(stop_reed1))
        #global start_reed1
        print("start reed1 : {}".format(start_reed1))
        global reed1_cycle_time
        reed1_tmp = stop_reed1 - start_reed1
        
        reed1_cycle_time = reed1_tmp
            #liczenie sredniej dla 30 pomiarow
        global cycle30_reed1
        if len(cycle30_reed1) < 30:
            cycle30_reed1.append(reed1_cycle_time)
        else:
            global avr30_reed1
            sum30 = 0
            for cycle in cycle30_reed1:
                sum30 = sum30 + cycle.seconds
            avr30_reed1 = sum30 / 30
            cycle30_reed1 = []
            cycle30_reed1.append(reed1_cycle_time)
            
        #licznie sredniej dla calej zmiany
        actual_hour = stop_reed1.hour
        if actual_hour >= 6 and actual_hour <= 14:
            global cycle_1shift_reed1
            global avr_1shift_reed1
            global cycle_2shift_reed1
            global avr_2shift_reed1
            global cycle_3shift_reed1
            global avr_3shift_reed1
            #zerowanie elementow z poprzednich zmian
            cycle_2shift_reed1 = []
            avr_2shift_reed1 = 0
            cycle_3shift_reed1 = []
            avr_3shift_reed1 = 0
                
            cycle_1shift_reed1.append(reed1_cycle_time)
            sum1 = 0
                
            for cycle1 in cycle_1shift_reed1:
                sum1 = sum1 + cycle1.seconds
                    
            avr_1shift_reed1 = sum1 / len(cycle_1shift_reed1)
                
        elif actual_hour >14 and actual_hour <=22:
            #global cycle_1shift_reed1
            #global avr_1shift_reed1
            #global cycle_2shift_reed1
            #global avr_2shift_reed1
            #global cycle_3shift_reed1
            #global avr_3shift_reed1
            #zerowanie elementow z poprzednich zmian
            cycle_1shift_reed1 = []
            avr_1shift_reed1= 0
            cycle_3shift_reed1 = []
            avr_3shift_reed1 = 0
                
            cycle_2shift_reed1.append(reed1_cycle_time)
            sum2 = 0
                
            for cycle2 in cycle_2shift_reed1:
                sum2 = sum2 + cycle2.seconds
                    
            avr_2shift_reed1 = sum2 / len(cycle_2shift_reed1)
                
        elif actual_hour >22 and actual_hour <6:
            #global cycle_1shift_reed1
            #global avr_1shift_reed1
            #global cycle_2shift_reed1
            #global avr_2shift_reed1
            #global cycle_3shift_reed1
            #global avr_3shift_reed1
                
            #zerowanie elementow z poprzednich zmian
            cycle_1shift_reed1 = []
            avr_1shift_reed1 = 0
            cycle_2shift_reed1 = []
            avr_2shift_reed1 = 0
                
            cycle_3shift_reed1.append(reed1_cycle_time)
            sum3 = 0
                
            for cycle3 in cycle_3shift_reed1:
                sum3 = sum3 + cycle3.seconds
                    
            avr_3shift_reed1 = sum3 / len(cycle_3shift_reed1)
            
        #zapis do pliku csv
        try:
            with open('/home/pi/Public/reed1.csv', 'a') as csvfile:
                reed1_csv = csv.writer(csvfile, delimiter=';')
                reed1_csv.writerow([stop_reed1, reed1_cycle_time, avr30_reed1, avr_1shift_reed1, avr_2shift_reed1, avr_1shift_reed1])    
        except Exception as err:
             print("Cannot open the file")
             print(str(err))
               
        start_reed1 = stop_reed1
    

def reed2_falling_detect(reed2_pin):
    print("reed2 sensor falling edge detected!")
    global first_time_reed2
    if first_time_reed2 == True: #to zadziala tylko przy pierwszym wejsciu
        print("first time!")
        global start_reed2
        start_reed2 = datetime.now()
        #global first_time_reed2
        first_time_reed2 = False
    else: #dla kazdego kolejnego zbocza
        global stop_reed2
        stop_reed2 = datetime.now()
        
         #liczenie czasu postoju
        global previous_state_reed2
        previous_state_reed2 = not previous_state_reed2
        delay_reed2_tmp = stop_reed2 - high_start_reed2
        if delay_reed2_tmp.seconds > accepted_low_time:
            delay_reed2 = delay_reed2_tmp
            print("reed2 delay is {}".format(delay_reed2))
            actual_date = date.today()
            try:
                with open('/home/pi/Public/delay.csv', 'a') as csvfile:
                    delay_csv = csv.writer(csvfile, delimiter=';')
                    delay_csv.writerow([actual_date, 0, delay_reed2, 0])
            except Exception as err:
                print("Cannot open the file")
                print(str(err))
        
        print("stop reed2 : {}".format(stop_reed2))
        #global start_reed2
        print("start reed2 : {}".format(start_reed2))
        global reed2_cycle_time
        reed2_tmp = stop_reed2 - start_reed2
        
        reed2_cycle_time = reed2_tmp
            #liczenie sredniej dla 30 pomiarow
        global cycle30_reed2
        if len(cycle30_reed2) < 30:
            cycle30_reed2.append(reed2_cycle_time)
        else:
            global avr30_reed2
            sum30 = 0
            for cycle in cycle30_reed2:
                sum30 = sum30 + cycle.seconds
            avr30_reed2 = sum30 / 30
            cycle30_reed2 = []
            cycle30_reed2.append(reed2_cycle_time)
            
        #licznie sredniej dla calej zmiany
        actual_hour = stop_reed2.hour
        if actual_hour >= 6 and actual_hour <= 14:
            global cycle_1shift_reed2
            global avr_1shift_reed2
            global cycle_2shift_reed2
            global avr_2shift_reed2
            global cycle_3shift_reed2
            global avr_3shift_reed2
            #zerowanie elementow z poprzednich zmian
            cycle_2shift_reed2 = []
            avr_2shift_reed2 = 0
            cycle_3shift_reed2 = []
            avr_3shift_reed2 = 0
                
            cycle_1shift_reed2.append(reed2_cycle_time)
            sum1 = 0
                
            for cycle1 in cycle_1shift_reed2:
                sum1 = sum1 + cycle1.seconds
                    
            avr_1shift_reed2 = sum1 / len(cycle_1shift_reed2)
                
        elif actual_hour >14 and actual_hour <=22:
            #global cycle_1shift_reed2
            #global avr_1shift_reed2
            #global cycle_2shift_reed2
            #global avr_2shift_reed2
            #global cycle_3shift_reed2
            #global avr_3shift_reed2
            #zerowanie elementow z poprzednich zmian
            cycle_1shift_reed2 = []
            avr_1shift_reed2= 0
            cycle_3shift_reed2 = []
            avr_3shift_reed2 = 0
                
            cycle_2shift_reed2.append(reed2_cycle_time)
            sum2 = 0
                
            for cycle2 in cycle_2shift_reed2:
                sum2 = sum2 + cycle2.seconds
                    
            avr_2shift_reed2 = sum2 / len(cycle_2shift_reed2)
                
        elif actual_hour >22 and actual_hour <6:
            #global cycle_1shift_reed2
            #global avr_1shift_reed2
            #global cycle_2shift_reed2
            #global avr_2shift_reed2
            #global cycle_3shift_reed2
            #global avr_3shift_reed2
                
            #zerowanie elementow z poprzednich zmian
            cycle_1shift_reed2 = []
            avr_1shift_reed2 = 0
            cycle_2shift_reed2 = []
            avr_2shift_reed2 = 0
                
            cycle_3shift_reed2.append(reed2_cycle_time)
            sum3 = 0
                
            for cycle3 in cycle_3shift_reed2:
                sum3 = sum3 + cycle3.seconds
                    
            avr_3shift_reed2 = sum3 / len(cycle_3shift_reed2)
            
        #zapis do pliku csv
        try:
            with open('/home/pi/Public/reed2.csv', 'a') as csvfile:
                reed2_csv = csv.writer(csvfile, delimiter=';')
                reed2_csv.writerow([stop_reed2, reed2_cycle_time, avr30_reed2, avr_1shift_reed2, avr_2shift_reed2, avr_1shift_reed2])    
        except Exception as err:
             print("Cannot open the file")
             print(str(err))
               
        start_reed2 = stop_reed2
    

def reed3_falling_detect(reed3_pin):
    print("reed3 sensor falling edge detected!")
    global first_time_reed3
    if first_time_reed3 == True: #to zadziala tylko przy pierwszym wejsciu
        print("first time!")
        global start_reed3
        start_reed3 = datetime.now()
        #global first_time_reed3
        first_time_reed3 = False
    else: #dla kazdego kolejnego zbocza
        global stop_reed3
        stop_reed3 = datetime.now()
        
        #liczenie czasu postoju
        global previous_state_reed3
        previous_state_reed3 = not previous_state_reed3
        delay_reed3_tmp = stop_reed3 - high_start_reed3
        if delay_reed3_tmp.seconds > accepted_low_time:
            delay_reed3 = delay_reed3_tmp
            print("reed3 delay is {}".format(delay_reed3))
            actual_date = date.today()
            try:
                with open('/home/pi/Public/delay.csv', 'a') as csvfile:
                    delay_csv = csv.writer(csvfile, delimiter=';')
                    delay_csv.writerow([actual_date, 0, 0, delay_reed3])
            except Exception as err:
                print("Cannot open the file")
                print(str(err))
            
            
        
        print("stop reed3 : {}".format(stop_reed3))
        #global start_reed3
        print("start reed3 : {}".format(start_reed3))
        global reed3_cycle_time
        reed3_tmp = stop_reed3 - start_reed3
        
        reed3_cycle_time = reed3_tmp
            #liczenie sredniej dla 30 pomiarow
        global cycle30_reed3
        if len(cycle30_reed3) < 30:
            cycle30_reed3.append(reed3_cycle_time)
        else:
            global avr30_reed3
            sum30 = 0
            for cycle in cycle30_reed3:
                sum30 = sum30 + cycle.seconds
            avr30_reed3 = sum30 / 30
            cycle30_reed3 = []
            cycle30_reed3.append(reed3_cycle_time)
            
        #licznie sredniej dla calej zmiany
        actual_hour = stop_reed3.hour
        if actual_hour >= 6 and actual_hour <= 14:
            global cycle_1shift_reed3
            global avr_1shift_reed3
            global cycle_2shift_reed3
            global avr_2shift_reed3
            global cycle_3shift_reed3
            global avr_3shift_reed3
            #zerowanie elementow z poprzednich zmian
            cycle_2shift_reed3 = []
            avr_2shift_reed3 = 0
            cycle_3shift_reed3 = []
            avr_3shift_reed3 = 0
                
            cycle_1shift_reed3.append(reed3_cycle_time)
            sum1 = 0
                
            for cycle1 in cycle_1shift_reed3:
                sum1 = sum1 + cycle1.seconds
                    
            avr_1shift_reed3 = sum1 / len(cycle_1shift_reed3)
                
        elif actual_hour >14 and actual_hour <=22:
            #global cycle_1shift_reed3
            #global avr_1shift_reed3
            #global cycle_2shift_reed3
            #global avr_2shift_reed3
            #global cycle_3shift_reed3
            #global avr_3shift_reed3
            #zerowanie elementow z poprzednich zmian
            cycle_1shift_reed3 = []
            avr_1shift_reed3= 0
            cycle_3shift_reed3 = []
            avr_3shift_reed3 = 0
                
            cycle_2shift_reed3.append(reed3_cycle_time)
            sum2 = 0
                
            for cycle2 in cycle_2shift_reed3:
                sum2 = sum2 + cycle2.seconds
                    
            avr_2shift_reed3 = sum2 / len(cycle_2shift_reed3)
                
        elif actual_hour >22 and actual_hour <6:
            #global cycle_1shift_reed3
            #global avr_1shift_reed3
            #global cycle_2shift_reed3
            #global avr_2shift_reed3
            #global cycle_3shift_reed3
            #global avr_3shift_reed3
                
            #zerowanie elementow z poprzednich zmian
            cycle_1shift_reed3 = []
            avr_1shift_reed3 = 0
            cycle_2shift_reed3 = []
            avr_2shift_reed3 = 0
                
            cycle_3shift_reed3.append(reed3_cycle_time)
            sum3 = 0
                
            for cycle3 in cycle_3shift_reed3:
                sum3 = sum3 + cycle3.seconds
                    
            avr_3shift_reed3 = sum3 / len(cycle_3shift_reed3)
            
        #zapis do pliku csv
        try:
            with open('/home/pi/Public/reed3.csv', 'a') as csvfile:
                reed3_csv = csv.writer(csvfile, delimiter=';')
                reed3_csv.writerow([stop_reed3, reed3_cycle_time, avr30_reed3, avr_1shift_reed3, avr_2shift_reed3, avr_1shift_reed3])    
        except Exception as err:
             print("Cannot open the file")
             print(str(err))
               
        start_reed3 = stop_reed3

def set_gpio():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(opt_sensor_pin, gpio.IN) #gpio do sensora optycznego
    gpio.setup(reed1_pin, gpio.IN) #gpio do kontaktron 1
    gpio.setup(reed2_pin, gpio.IN) #gpio do kontaktron 2
    gpio.setup(reed3_pin, gpio.IN) #gpio do kontaktron 3

def main():
    print("Start Script..")
    print("gpio initialization")
    set_gpio()
    
    #utworzenie pliku csv do sensora optycznego
    optical_csv_exist = os.path.exists("/home/pi/Public/optical.csv")
    if optical_csv_exist == False:
        try:
            with open('/home/pi/Public/optical.csv', 'a') as csvfile:
                optical_csv = csv.writer(csvfile, delimiter=';')
                optical_csv.writerow(['date','cycle optical', 'avr30', 'avr 1shift', 'avr 2shift', 'avr 3shift'])
        except Exception as err:
            print("Cannot open the file")
            print(str(err))
            
    #utworzenie pliku csv do sensora reed1
    reed1_csv_exist = os.path.exists("/home/pi/Public/reed1.csv")
    if reed1_csv_exist == False:
        try:
            with open('/home/pi/Public/reed1.csv', 'a') as csvfile:
                reed1_csv = csv.writer(csvfile, delimiter=';')
                reed1_csv.writerow(['date','cycle reed1', 'avr30', 'avr 1shift', 'avr 2shift', 'avr 3shift'])
        except Exception as err:
            print("Cannot open the file")
            print(str(err))
            
    #utworzenie pliku csv do sensora reed2
    reed2_csv_exist = os.path.exists("/home/pi/Public/reed2.csv")
    if reed2_csv_exist == False:
        try:
            with open('/home/pi/Public/reed2.csv', 'a') as csvfile:
                reed2_csv = csv.writer(csvfile, delimiter=';')
                reed2_csv.writerow(['date','cycle reed2', 'avr30', 'avr 1shift', 'avr 2shift', 'avr 3shift'])
        except Exception as err:
            print("Cannot open the file")
            print(str(err))
            
    #utworzenie pliku csv do sensora reed3
    reed3_csv_exist = os.path.exists("/home/pi/Public/reed3.csv")
    if reed3_csv_exist == False:
        try:
            with open('/home/pi/Public/reed3.csv', 'a') as csvfile:
                reed3_csv = csv.writer(csvfile, delimiter=';')
                reed3_csv.writerow(['date','cycle reed3', 'avr30', 'avr 1shift', 'avr 2shift', 'avr 3shift'])
        except Exception as err:
            print("Cannot open the file")
            print(str(err))
            
            
    #utworzenie pliku csv do czasu postojow
    delay_csv_exist = os.path.exists("/home/pi/Public/delay.csv")
    if delay_csv_exist == False:
        try:
            with open('/home/pi/Public/delay.csv', 'a') as csvfile:
                delay_csv = csv.writer(csvfile, delimiter=';')
                delay_csv.writerow(['date','delay reed1', 'delay reed2', 'delay reed3'])
        except:
            print("Cannot open the file")
    
    gpio.add_event_detect(opt_sensor_pin, gpio.RISING, callback=op_sensor_rising_detect, bouncetime=200)
    
    gpio.add_event_detect(reed1_pin, gpio.FALLING, callback=reed1_falling_detect, bouncetime=200)
    gpio.add_event_detect(reed2_pin, gpio.FALLING, callback=reed2_falling_detect, bouncetime=200)
    gpio.add_event_detect(reed3_pin, gpio.FALLING, callback=reed3_falling_detect, bouncetime=200)
    
    
    print("First init time: {}".format(start_time_main))
    
    while True:
  
        
        #delay
        
        input_reed3 = gpio.input(reed3_pin)
        #print(input_reed3)
        global high_start_reed3
        global previous_state_reed3
        if input_reed3 == 1 and previous_state_reed3 == 0: 
            high_start_reed3 = datetime.now()
            previous_state_reed3 = not previous_state_reed3
            print("reed3 delay start counting")
            
            
        input_reed2 = gpio.input(reed2_pin)
        #print(input_reed2)
        global high_start_reed2
        global previous_state_reed2
        if input_reed2 == 1 and previous_state_reed2 == 0: 
            high_start_reed2 = datetime.now()
            previous_state_reed2 = not previous_state_reed2
            print("reed2 delay start counting")
            
            
        input_reed1 = gpio.input(reed1_pin)
        print(input_reed1)
        global high_start_reed1
        global previous_state_reed1
        if input_reed1 == 1 and previous_state_reed1 == 0: 
            high_start_reed1 = datetime.now()
            previous_state_reed1 = not previous_state_reed1
            print("reed1 delay start counting")
        
        time.sleep(1) #do debugu


if __name__=="__main__":
    main()