from ast import Lt
import numpy as np 
from numpy import DataSource, interp
from scipy.signal import find_peaks
from scipy.signal import peak_prominences
import serial 
from serial import Serial 
import time
import pandas as pd 

GRAVITY = 9.81

patient_body_weight = 70

#just going to communicate with one board in here and pull a data set for the heel data
#see if i can come up with an algo that can grab the heel on parameter every time

#the working PCB can be reached at COM4

#GOING TO HAVE A TRY CATCH HERE, the catch will be skipped once the sample data set exists for peak finding experimentation

try:
    #if this succeeds then i have already collected this test data set and can just analyze it with the algorithm 
    #if it fails, all the other stuff has to happen in the except statement
    #test_data = pd.read_csv('test_heel_data.csv')
    test_data = pd.read_csv('parameterCALC_testDATA.csv')

    timeData = test_data['TIME']
    
    left_heel_data = test_data['LEFT_FSR_Heel']
    left_toe_data = test_data['LEFT_FSR_mToe']
    
    right_heel_data = test_data['RIGHT_FSR_Heel']
    right_toe_data = test_data['RIGHT_FSR_mToe']

    timeData = np.array(timeData)
    
    left_heel_data = np.array(left_heel_data)
    left_toe_data = np.array(left_toe_data)
    
    right_heel_data = np.array(right_heel_data)
    right_toe_data = np.array(right_toe_data)
    
    #SECTION TO AMPLITUDE SCALE ALL DATA BEFORE PROCESSING
    LH_normalizer = np.amax(left_heel_data)
    LT_normalizer = np.amax(left_toe_data)
    
    RH_normalizer = np.amax(right_heel_data)
    RT_normalizer = np.amax(right_toe_data)
    
    #NOW with normalizer values can amplitude scale data sets between 0 and 1
    LH_normalized_data = left_heel_data/LH_normalizer
    LT_normalized_data = left_toe_data/LT_normalizer
    
    RH_normalized_data = right_heel_data/RH_normalizer
    RT_normalized_data = right_toe_data/RT_normalizer

    #now here i can work on the algorithm
    #do peak finding on the force data set and then match the index's with the time data

    #peaks = peak_prominences(forceData) #problem is it just picks with only one sample lower on either side so not detecting true peak 
    LH_troughs = find_peaks(LH_normalized_data, prominence = 0.5, distance = 50) #ADDING NEGATIVE SIGN FINDS TROUGHS INSTEAD OF PEAKS WHICH IS NEEDED FOR THIS CASE
    LT_troughs = find_peaks(-LT_normalized_data, prominence = 0.5, distance = 50) #I think the prominence value essentially specifies the percentage from the max peak in the data set that will also be considered
    
    RH_troughs = find_peaks(RH_normalized_data, distance = 50) #since 100 points in a second based on sample rate, 50 is half second, should be no peaks within HS of each other
    RT_troughs = find_peaks(RT_normalized_data, distance = 50) #going with 0.95 as prominence value assuming 95% of flatness of trough or something?
    
    #now syphon out zeroth index to actually pull array
    LH_troughs = LH_troughs[0]
    LT_troughs = LT_troughs[0]
    
    RH_troughs = RH_troughs[0]
    RT_troughs = RT_troughs[0]
    
    #print(LH_troughs)
    #print(LT_troughs)
    print(RH_troughs)
    print(RT_troughs)
    
    #NOW WILL DO LE MATH
    #just do for one foot for now as only really need a proof of concept that the method works
    #go with right foot in this case as left foot data is trash
    
    #try instead creating search algorithm for peaks rather than troughs
    r_heel_on_array = []
    
    for RH in RH_troughs:
        RH_starting_point = RH
        
        RH_solved = False
        
        #since looking for heel on, want to back search from the peak
        while RH_solved == False:
            
            if RH_starting_point == -1 or RH_starting_point >= len(RH_normalized_data) - 5: #negative 1 index because this will still allow for the 0th index to be tested
                RH_solved = True #this is basically a defense against the zeroth index (probably just an edge case)
            
            RH_test_sample_0 = RH_normalized_data[RH_starting_point]
            RH_test_sample_1 = RH_normalized_data[RH_starting_point + 1]
            RH_test_sample_2 = RH_normalized_data[RH_starting_point + 2]
            RH_test_sample_3 = RH_normalized_data[RH_starting_point + 3]
            RH_test_sample_4 = RH_normalized_data[RH_starting_point + 4]
            RH_test_sample_5 = RH_normalized_data[RH_starting_point + 5] #needs to be + 5 since we are back searching in this case
            #now maybe try taking absolute value of difference between the two points
            
            if RH_test_sample_0 < RH_normalized_data[RH]*0.8 and RH_test_sample_0 == RH_test_sample_1 and RH_test_sample_0 == RH_test_sample_2 and RH_test_sample_0 == RH_test_sample_3 and RH_test_sample_0 == RH_test_sample_4 and RH_test_sample_0 == RH_test_sample_5: #basically saying if the two point are the same which should only occur at the trough I think
                r_heel_on_array.append(RH_starting_point + 6) #NOTICE THIS IS 1 HIGHER INDEX THAN TEST SAMPLE 1 AS THIS WILL BE FIRST POINT WHERE FORCE RISES UP
                RH_solved = True
            else:
                RH_starting_point = RH_starting_point - 1 #back search for heel on location
                    
    print(r_heel_on_array)
    
    r_toe_off_array = []
    
    for RT in RT_troughs:
        RT_starting_point = RT
        
        RT_solved = False
        
        #since looking for toe off, want to forward search from the peak
        while RT_solved == False:
            
            if RT_starting_point == len(RT_normalized_data) or RT_starting_point <= 4: #since forward searching want to cancel search before max index of data set is exceeded
                RT_solved = True #since back searching by 5 samples, will still work if peak detected at 5th index position, but will skip if peak detected before 5
                
            RT_test_sample_0 = RT_normalized_data[RT_starting_point]
            RT_test_sample_1 = RT_normalized_data[RT_starting_point - 1]
            RT_test_sample_2 = RT_normalized_data[RT_starting_point - 2]
            RT_test_sample_3 = RT_normalized_data[RT_starting_point - 3]
            RT_test_sample_4 = RT_normalized_data[RT_starting_point - 4]
            RT_test_sample_5 = RT_normalized_data[RT_starting_point - 5] #5 points behind starting point since forward searching through data for toe off
            
            if RT_test_sample_0 == RT_test_sample_1 and RT_test_sample_0 == RT_test_sample_2 and RT_test_sample_0 == RT_test_sample_3 and RT_test_sample_0 == RT_test_sample_4 and RT_test_sample_0 == RT_test_sample_5:
                r_toe_off_array.append(RT_starting_point - 6)
                RT_solved = True
            else:
                RT_starting_point = RT_starting_point + 1
    
    print(r_toe_off_array)
    
    #WOOHOO THIS ALGORITHM IS WORKING FUCK YEAH, so now just need to test the indexing for pulling timestamps basically, then parameter calculation should be good to go 
    r_heel_on_array = r_heel_on_array
    r_toe_off_array = r_toe_off_array
    
    timeData = timeData
    
    r_heel_on_TIMESTAMPS = timeData[r_heel_on_array]
    r_toe_off_TIMESTAMPS = timeData[r_toe_off_array]
    
    print("little space here just for shits")
    print(r_heel_on_TIMESTAMPS)
    print(r_toe_off_TIMESTAMPS)
    
except:
    #create serial object 
    s = serial.Serial('COM5', 115200, timeout = 2) #LAPTOP COM PORTS
    s1 = serial.Serial('COM6', 115200, timeout = 2)
    
    #s = serial.Serial('COM3', 115200, timeout = 2) #DESKTOP COM PORTS
    #s1 = serial.Serial('COM5', 115200, timeout = 2)

    s.write(b'105')
    s1.write(b'105')
    time.sleep(2)

    s.write(b'106')
    s1.write(b'107')
    time.sleep(2)

    #now have to get past calibration step 
    s.flushInput()
    s1.flushInput()
    time.sleep(2)

    s.write(b'109')
    s1.write(b'109')
    s.flushInput()
    s1.flushInput()
    time.sleep(2)


    s.flushInput()
    s1.flushInput()
    time.sleep(2)

    s.write(b'108')
    s1.write(b'108')
    s.flushInput()
    s1.flushInput()
    time.sleep(1)

    #now measurement is occuring but data not being sent 
    #have to wait until measurement done comes in through serial port 

    waiting = True
    
    one_done = False
    two_done = False

    print('measurement started')

    while waiting == True:
        sample = s.readline()
        sample1 = s1.readline()
    
        if b"Measurement_Done" in sample:
            one_done = True
            
        if b"Measurement_Done" in sample1:
            two_done = True
            
        if one_done == True and two_done == True:
            waiting = False


    print('measurement done')

    #once breaks out of loop can now send data over serial port 
    #first will experiement with algorithm for heel sensor which is FSR3 

    s.flushInput()
    s1.flushInput()
    time.sleep(2)

    #write command to bring data in
    s.write(b'Confirm')  
    s1.write(b'Confirm')
    time.sleep(1)

    s.flushInput()
    s1.flushInput()
    time.sleep(2)

    data_done = False

    s.write(b'Send_Data')
    s1.write(b'Send_Data')

    RIGHT_FSR_Heel_BITVAL = []
    RIGHT_FSR_medialToe_BITVAL = []
    RIGHT_FSR_lateralToe_BITVAL = []
    RIGHT_X_AXIS_ACCELERATION = []
    RIGHT_Y_AXIS_ACCELERATION = []
    RIGHT_Z_AXIS_ACCELERATION = []
    
    LEFT_FSR_Heel_BITVAL = []
    LEFT_FSR_medialToe_BITVAL = []
    LEFT_FSR_lateralToe_BITVAL = []
    LEFT_X_AXIS_ACCELERATION = []
    LEFT_Y_AXIS_ACCELERATION = []
    LEFT_Z_AXIS_ACCELERATION = []
    
    time_vector = []
    
    print('sending data')

    while data_done == False:
        raw = s.readline()
        raw1 = s1.readline()

        if b';' not in raw and b';' not in raw1:
            data_done = True
            break

        string = str(raw, 'utf-8')
        string1 = str(raw1, 'utf-8')
        
        split = string.split(',')
        split1 = string1.split(',')

        time_value = int(split[0])
        
        right_heel_value = int(split[6]) #the 6th index corresponds to the heel FSR
        right_medialtoe_value = int(split[4])
        right_lateraltoe_value = int(split[5])
        right_x_acceleration = float(split[1])
        right_y_acceleration = float(split[2])
        right_z_acceleration = float(split[3])
        
        left_heel_value = int(split1[6])
        left_medialtoe_value = int(split1[4])
        left_lateraltoe_value = int(split1[5])
        left_x_acceleration = float(split1[1])
        left_y_acceleration = float(split1[2])
        left_z_acceleration = float(split1[3])

        time_vector.append(time_value)
        
        RIGHT_FSR_Heel_BITVAL.append(right_heel_value)
        RIGHT_FSR_medialToe_BITVAL.append(right_medialtoe_value)
        RIGHT_FSR_lateralToe_BITVAL.append(right_lateraltoe_value)
        RIGHT_X_AXIS_ACCELERATION.append(right_x_acceleration)
        RIGHT_Y_AXIS_ACCELERATION.append(right_y_acceleration)
        RIGHT_Z_AXIS_ACCELERATION.append(right_z_acceleration)
        
        LEFT_FSR_Heel_BITVAL.append(left_heel_value)
        LEFT_FSR_medialToe_BITVAL.append(left_medialtoe_value)
        LEFT_FSR_lateralToe_BITVAL.append(left_lateraltoe_value)
        LEFT_X_AXIS_ACCELERATION.append(left_x_acceleration)
        LEFT_Y_AXIS_ACCELERATION.append(left_y_acceleration)
        LEFT_Z_AXIS_ACCELERATION.append(left_z_acceleration)

    print('data sent')
    
    time_vector = np.array(time_vector)
    
    RIGHT_FSR_Heel_BITVAL = np.array(RIGHT_FSR_Heel_BITVAL)
    RIGHT_FSR_medialToe_BITVAL = np.array(RIGHT_FSR_medialToe_BITVAL)
    RIGHT_FSR_lateralToe_BITVAL = np.array(RIGHT_FSR_lateralToe_BITVAL)
    RIGHT_X_AXIS_ACCELERATION = np.array(RIGHT_X_AXIS_ACCELERATION)
    RIGHT_Y_AXIS_ACCELERATION = np.array(RIGHT_Y_AXIS_ACCELERATION)
    RIGHT_Z_AXIS_ACCELERATION = np.array(RIGHT_Z_AXIS_ACCELERATION)
    
    LEFT_FSR_Heel_BITVAL = np.array(LEFT_FSR_Heel_BITVAL)
    LEFT_FSR_medialToe_BITVAL = np.array(LEFT_FSR_medialToe_BITVAL)
    LEFT_FSR_lateralToe_BITVAL = np.array(LEFT_FSR_lateralToe_BITVAL)
    LEFT_X_AXIS_ACCELERATION = np.array(LEFT_X_AXIS_ACCELERATION)
    LEFT_Y_AXIS_ACCELERATION = np.array(LEFT_Y_AXIS_ACCELERATION)
    LEFT_Z_AXIS_ACCELERATION = np.array(LEFT_Z_AXIS_ACCELERATION)

    right_heel_voltage = np.interp(RIGHT_FSR_Heel_BITVAL, [0, 4095], [1, 3300]) #THINKING COULD FIX DIV/0 error by changing to 1-4095 instead of 0
    right_medialtoe_voltage = np.interp(RIGHT_FSR_medialToe_BITVAL, [0, 4095], [1, 3300])
    right_lateraltoe_voltage = np.interp(RIGHT_FSR_lateralToe_BITVAL, [0, 4095], [1, 3300])
    
    left_heel_voltage = np.interp(LEFT_FSR_Heel_BITVAL, [0, 4095], [1, 3300])
    left_medialtoe_voltage = np.interp(LEFT_FSR_medialToe_BITVAL, [0, 4095], [1, 3300])
    left_lateraltoe_voltage = np.interp(LEFT_FSR_lateralToe_BITVAL, [0, 4095], [1, 3300])

    right_heel_resistance = (right_heel_voltage*10000)/(3301 - right_heel_voltage)
    right_medialtoe_resistance = (right_medialtoe_voltage*10000)/(3301 - right_medialtoe_voltage)
    right_lateraltoe_resistance = (right_lateraltoe_voltage*10000)/(3301 - right_lateraltoe_voltage)
    
    left_heel_resistance = (left_heel_voltage*10000)/(3301 - left_heel_voltage)
    left_medialtoe_resistance = (left_medialtoe_voltage*10000)/(3301 - left_medialtoe_voltage)
    left_lateraltoe_resistance = (left_lateraltoe_voltage*10000)/(3301 - left_lateraltoe_voltage)

    right_heel_force = (GRAVITY*60.701)*right_heel_resistance**-0.625 #look at this as division mathematically, that is why getting div/0 error - SOLVED IT
    right_medialtoe_force = (GRAVITY*60.701)*right_medialtoe_resistance**-0.625
    right_lateraltoe_force = (GRAVITY*60.701)*right_lateraltoe_resistance**-0.625
    
    left_heel_force = (GRAVITY*60.701)*left_heel_resistance**-0.625
    left_medialtoe_force = (GRAVITY*60.701)*left_medialtoe_resistance**-0.625
    left_lateraltoe_force = (GRAVITY*60.701)*left_lateraltoe_resistance**-0.625
    
    #CAP ALL THE FORCE VALUES AT 30N 
    right_heel_force = np.clip(right_heel_force, a_min = 0, a_max = 30)
    right_medialtoe_force = np.clip(right_medialtoe_force, a_min = 0, a_max = 30)
    right_lateraltoe_force = np.clip(right_lateraltoe_force, a_min = 0, a_max = 30)
    
    left_heel_force = np.clip(left_heel_force, a_min = 0, a_max = 30)
    left_medialtoe_force = np.clip(left_medialtoe_force, a_min = 0, a_max = 30)
    left_lateraltoe_force = np.clip(left_lateraltoe_force, a_min = 0, a_max = 30)

    #works up until this point 

    TIME = np.interp(time_vector, [0, 2999], [0, 30])

    index = list(range(1000,2501,1))

    #NOW THIS IS THE DATA TO PULL THE PEAKS FROM
    TIME_reduced = TIME[index]
    
    right_heel_FORCE_reduced = right_heel_force[index]
    right_medialtoe_FORCE_reduced = right_medialtoe_force[index]
    right_lateraltoe_FORCE_reduced = right_lateraltoe_force[index]
    RIGHT_X_AXIS_ACCELERATION_reduced = RIGHT_X_AXIS_ACCELERATION[index]
    RIGHT_Y_AXIS_ACCELERATION_reduced = RIGHT_Y_AXIS_ACCELERATION[index]
    RIGHT_Z_AXIS_ACCELERATION_reduced = RIGHT_Z_AXIS_ACCELERATION[index]
    
    left_heel_FORCE_reduced = left_heel_force[index]
    left_medialtoe_FORCE_reduced = left_medialtoe_force[index]
    left_lateraltoe_FORCE_reduced = left_lateraltoe_force[index]
    LEFT_X_AXIS_ACCELERATION_reduced = LEFT_X_AXIS_ACCELERATION[index]
    LEFT_Y_AXIS_ACCELERATION_reduced = LEFT_Y_AXIS_ACCELERATION[index]
    LEFT_Z_AXIS_ACCELERATION_reduced = LEFT_Z_AXIS_ACCELERATION[index]
    
    #FOR DEBUGGING REASONS
    #rightTOEBITVAL = RIGHT_FSR_Toe_BITVAL[index]
    #rightTOEVOLTAGE = right_toe_voltage[index]
    #rightTOERESISTANCE = right_toe_resistance[index]

    #now want to save data file with actual force data and import it 
    gait_data = {'TIME': TIME_reduced, 'LEFT_FSR_Heel': left_heel_FORCE_reduced, 'LEFT_FSR_mToe': left_medialtoe_FORCE_reduced, 'LEFT_FSR_lToe': left_lateraltoe_FORCE_reduced, 'RIGHT_FSR_Heel': right_heel_FORCE_reduced, 'RIGHT_FSR_mToe': right_medialtoe_FORCE_reduced, 'RIGHT_FSR_lToe': right_lateraltoe_FORCE_reduced, 'RIGHT_X_ACCEL': RIGHT_X_AXIS_ACCELERATION_reduced, 'RIGHT_Y_ACCEL': RIGHT_Y_AXIS_ACCELERATION_reduced, 'RIGHT_Z_ACCEL': RIGHT_Z_AXIS_ACCELERATION_reduced, 'LEFT_X_ACCEL': LEFT_X_AXIS_ACCELERATION_reduced, 'LEFT_Y_ACCEL': LEFT_Y_AXIS_ACCELERATION_reduced, 'LEFT_Z_ACCEL': LEFT_Z_AXIS_ACCELERATION_reduced}

    DATA_TABLE = pd.DataFrame(data = gait_data)

    DATA_TABLE.to_csv('parameterCALC_testDATA.csv')
    
    print('data saved')