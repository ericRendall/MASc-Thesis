import numpy as np 
import pandas as pd 
from scipy import signal
from scipy.signal import find_peaks

#THIS SCRIPT IS TO QUICKLY TEST THE PEAKS FOUND FROM COLLECTED FSR DATA
#to see what is causing the errors in the parameter calculations
#maybe find_peaks() input parameters (distance, prominence) can be applied to reduce these errors

#import the collected data set that caused the errors
test_data = pd.read_csv('ER1234_220317-0300_GAITDATA.csv') #this can be replaced with whatever recent file name of choice 

left_FSR_TOE = test_data['LeftFSR_MedialToe']
#clip the data to the right size 
#left_FSR_TOE = left_FSR_TOE[1000:2500]
left_FSR_HEEL = test_data['LeftFSR_Heel']

#import right foot data
right_FSR_TOE = test_data['RightFSR_MedialToe']
right_FSR_HEEL = test_data['RightFSR_Heel']

#extract out the correct index
index = list(range(1000,2501,1))

left_FSR_TOE = left_FSR_TOE[index]
left_FSR_HEEL = left_FSR_HEEL[index]

right_FSR_TOE = right_FSR_TOE[index]
right_FSR_HEEL = right_FSR_HEEL[index]

#amplitude scale all data 
LT_scaler = np.amax(left_FSR_TOE)
LH_scaler = np.amax(left_FSR_HEEL)

RT_scaler = np.amax(right_FSR_TOE)
RH_scaler = np.amax(right_FSR_HEEL)

left_FSR_TOE_ampScaled = left_FSR_TOE/LT_scaler
left_FSR_HEEL_ampScaled = left_FSR_HEEL/LH_scaler

right_FSR_TOE_ampScaled = right_FSR_TOE/RT_scaler
right_FSR_HEEL_ampScaled = right_FSR_HEEL/RH_scaler

#convert back to numpy array?
left_FSR_TOE_ampScaled = np.array(left_FSR_TOE_ampScaled)
left_FSR_HEEL_ampScaled = np.array(left_FSR_HEEL_ampScaled)

right_FSR_TOE_ampScaled = np.array(right_FSR_TOE_ampScaled)
right_FSR_HEEL_ampScaled = np.array(right_FSR_HEEL_ampScaled)

#now find the peaks breh 
peaks_LEFT_mtoe = find_peaks(left_FSR_TOE_ampScaled, distance = 60, prominence = 0.2)
peaks_LEFT_mtoe = peaks_LEFT_mtoe[0]
#print(peaks_LEFT_mtoe)

LEFT_toe_off_array = []

#TEST OUT ALGO
for LT in peaks_LEFT_mtoe: #THE IF STATEMENTS IN THIS ALGORITHM ARE ONE WAY OF DOING IT, but check the other 3 algos for the cleaner way
        
            LT_starting_point = LT

            LT_solved = False
            
            if LT_starting_point == len(left_FSR_TOE_ampScaled) or LT_starting_point <= 4: #since forward searching want to cancel search before max index of data set is exceeded
                LT_solved = True #since back searching by 5 samples, will still work if peak detected at 5th index position, but will skip if peak detected before 5
            
            while LT_solved == False:
                
                LT_test_sample_0 = left_FSR_TOE_ampScaled[LT_starting_point]
                LT_test_sample_1 = left_FSR_TOE_ampScaled[LT_starting_point - 1]
                LT_test_sample_2 = left_FSR_TOE_ampScaled[LT_starting_point - 2]
                LT_test_sample_3 = left_FSR_TOE_ampScaled[LT_starting_point - 3]
                LT_test_sample_4 = left_FSR_TOE_ampScaled[LT_starting_point - 4]
                LT_test_sample_5 = left_FSR_TOE_ampScaled[LT_starting_point - 5] #5 points behind starting point since forward searching through data for toe off
            
                if LT_test_sample_0 < left_FSR_TOE_ampScaled[LT]*0.8 and LT_test_sample_0 == LT_test_sample_1 and LT_test_sample_0 == LT_test_sample_2 and LT_test_sample_0 == LT_test_sample_3 and LT_test_sample_0 == LT_test_sample_4 and LT_test_sample_0 == LT_test_sample_5:
                    LEFT_toe_off_array.append(LT_starting_point - 6)
                    LT_solved = True

                else:
                    LT_starting_point = LT_starting_point + 1
                    
                    if LT_starting_point == len(left_FSR_TOE_ampScaled) or LT_starting_point <= 4: #since forward searching want to cancel search before max index of data set is exceeded
                        LT_solved = True #since back searching by 5 samples, will still work if peak detected at 5th index position, but will skip if peak detected before 5
                        
#print(LEFT_toe_off_array)



peaks_LEFT_heel = find_peaks(left_FSR_HEEL_ampScaled, distance = 60, prominence = 0.2)
peaks_LEFT_heel = peaks_LEFT_heel[0]

LEFT_heel_on_array = []

for LH in peaks_LEFT_heel:

            LH_starting_point = LH

            LH_solved = False
            
            if LH_starting_point == -1 or LH_starting_point >= len(left_FSR_HEEL_ampScaled) - 5: #negative 1 index because this will still allow for the 0th index to be tested
                LH_solved = True #this is basically a defense against the zeroth index (probably just an edge case)

            while LH_solved == False:
            
                LH_test_sample_0 = left_FSR_HEEL_ampScaled[LH_starting_point]
                LH_test_sample_1 = left_FSR_HEEL_ampScaled[LH_starting_point + 1]
                LH_test_sample_2 = left_FSR_HEEL_ampScaled[LH_starting_point + 2]
                LH_test_sample_3 = left_FSR_HEEL_ampScaled[LH_starting_point + 3]
                LH_test_sample_4 = left_FSR_HEEL_ampScaled[LH_starting_point + 4]
                LH_test_sample_5 = left_FSR_HEEL_ampScaled[LH_starting_point + 5] #needs to be + 5 since we are back searching in this case
                #now maybe try taking absolute value of difference between the two points
            
                if LH_test_sample_0 < left_FSR_HEEL_ampScaled[LH]*0.8 and LH_test_sample_0 == LH_test_sample_1 and LH_test_sample_0 == LH_test_sample_2 and LH_test_sample_0 == LH_test_sample_3 and LH_test_sample_0 == LH_test_sample_4 and LH_test_sample_0 == LH_test_sample_5: #basically saying if the two point are the same which should only occur at the trough I think
                    LEFT_heel_on_array.append(LH_starting_point + 6) #NOTICE THIS IS 1 HIGHER INDEX THAN TEST SAMPLE 1 AS THIS WILL BE FIRST POINT WHERE FORCE RISES UP
                    LH_solved = True
                else:
                    LH_starting_point = LH_starting_point - 1 #back search for heel on location
                    
                    if LH_starting_point == -1 or LH_starting_point >= len(left_FSR_HEEL_ampScaled) - 5: #negative 1 index because this will still allow for the 0th index to be tested
                        LH_solved = True #this is basically a defense against the zeroth index (probably just an edge case)
                        
#print(LEFT_heel_on_array)

#can see here without prominence some false peaks are fooling the system - adding a well thought out prominence value should fix the error 

#in the code we duplicate delete before using what was found as HS and TO values for calculations
#after duplicate deletion, should give better idea of where the errors are occuring

#DO RIGHT LEG
peaks_RIGHT_mtoe = find_peaks(right_FSR_TOE_ampScaled, distance = 60, prominence = 0.2)
peaks_RIGHT_mtoe = peaks_RIGHT_mtoe[0]

RIGHT_toe_off_array = []

for RT in peaks_RIGHT_mtoe:
            RT_starting_point = RT
        
            RT_solved = False
            
            if RT_starting_point == len(right_FSR_TOE_ampScaled) or RT_starting_point <= 4: #since forward searching want to cancel search before max index of data set is exceeded
                RT_solved = True #since back searching by 5 samples, will still work if peak detected at 5th index position, but will skip if peak detected before 5
        
            #since looking for toe off, want to forward search from the peak
            while RT_solved == False:
                
                RT_test_sample_0 = right_FSR_TOE_ampScaled[RT_starting_point]
                RT_test_sample_1 = right_FSR_TOE_ampScaled[RT_starting_point - 1]
                RT_test_sample_2 = right_FSR_TOE_ampScaled[RT_starting_point - 2]
                RT_test_sample_3 = right_FSR_TOE_ampScaled[RT_starting_point - 3]
                RT_test_sample_4 = right_FSR_TOE_ampScaled[RT_starting_point - 4]
                RT_test_sample_5 = right_FSR_TOE_ampScaled[RT_starting_point - 5] #5 points behind starting point since forward searching through data for toe off
            
                if RT_test_sample_0 < right_FSR_TOE_ampScaled[RT]*0.8 and RT_test_sample_0 == RT_test_sample_1 and RT_test_sample_0 == RT_test_sample_2 and RT_test_sample_0 == RT_test_sample_3 and RT_test_sample_0 == RT_test_sample_4 and RT_test_sample_0 == RT_test_sample_5:
                    RIGHT_toe_off_array.append(RT_starting_point - 6)
                    RT_solved = True
                else:
                    RT_starting_point = RT_starting_point + 1
                    
                    if RT_starting_point == len(right_FSR_TOE_ampScaled) or RT_starting_point <= 4: #since forward searching want to cancel search before max index of data set is exceeded
                        RT_solved = True #since back searching by 5 samples, will still work if peak detected at 5th index position, but will skip if peak detected before 5


peaks_RIGHT_heel = find_peaks(right_FSR_HEEL_ampScaled, distance = 60, prominence = 0.2)
peaks_RIGHT_heel = peaks_RIGHT_heel[0]

RIGHT_heel_on_array = []

for RH in peaks_RIGHT_heel:
            RH_starting_point = RH
        
            RH_solved = False
            
            if RH_starting_point == -1 or RH_starting_point >= len(right_FSR_HEEL_ampScaled) - 5: #negative 1 index because this will still allow for the 0th index to be tested
                RH_solved = True #this is basically a defense against the zeroth index (probably just an edge case)
        
            #since looking for heel on, want to back search from the peak
            while RH_solved == False:
            
                RH_test_sample_0 = right_FSR_HEEL_ampScaled[RH_starting_point]
                RH_test_sample_1 = right_FSR_HEEL_ampScaled[RH_starting_point + 1]
                RH_test_sample_2 = right_FSR_HEEL_ampScaled[RH_starting_point + 2]
                RH_test_sample_3 = right_FSR_HEEL_ampScaled[RH_starting_point + 3]
                RH_test_sample_4 = right_FSR_HEEL_ampScaled[RH_starting_point + 4]
                RH_test_sample_5 = right_FSR_HEEL_ampScaled[RH_starting_point + 5] #needs to be + 5 since we are back searching in this case
                #now maybe try taking absolute value of difference between the two points
            
                if RH_test_sample_0 < right_FSR_HEEL_ampScaled[RH]*0.8 and RH_test_sample_0 == RH_test_sample_1 and RH_test_sample_0 == RH_test_sample_2 and RH_test_sample_0 == RH_test_sample_3 and RH_test_sample_0 == RH_test_sample_4 and RH_test_sample_0 == RH_test_sample_5: #basically saying if the two point are the same which should only occur at the trough I think
                    RIGHT_heel_on_array.append(RH_starting_point + 6) #NOTICE THIS IS 1 HIGHER INDEX THAN TEST SAMPLE 1 AS THIS WILL BE FIRST POINT WHERE FORCE RISES UP
                    RH_solved = True
                else:
                    RH_starting_point = RH_starting_point - 1 #back search for heel on location
                    
                    if RH_starting_point == -1 or RH_starting_point >= len(right_FSR_HEEL_ampScaled) - 5: #negative 1 index because this will still allow for the 0th index to be tested
                        RH_solved = True #this is basically a defense against the zeroth index (probably just an edge case)
                        
                        
#now have all of them
LEFT_heel_on_array = LEFT_heel_on_array #ARRAY CONTAINS ALL INDEX POSITIONS OF HEEL ON FOR LEFT FOOT
LEFT_toe_off_array = LEFT_toe_off_array #AND THIS IS THE GOLDEN ARRAY FULL OF INDEX's OF TOE OFF POINTS FOR THE LEFT FOOT
#RIGHT FOOT
RIGHT_heel_on_array = RIGHT_heel_on_array #AND THIS ARRAY CONTAINS ALL INDEX POSITIONS FOR HEEL ON EVENTS FOR THE RIGHT FOOT 
RIGHT_toe_off_array = RIGHT_toe_off_array

#finally duplicate deletion, then done
LEFT_heel_on_array = list(dict.fromkeys(LEFT_heel_on_array))
LEFT_toe_off_array = list(dict.fromkeys(LEFT_toe_off_array))
        
RIGHT_heel_on_array = list(dict.fromkeys(RIGHT_heel_on_array))
RIGHT_toe_off_array = list(dict.fromkeys(RIGHT_toe_off_array)) #NOW ALL DUPLICATES SHOULD BE DELETED

#these are still index positions 
print(LEFT_heel_on_array)
print(LEFT_toe_off_array)

print(RIGHT_heel_on_array)
print(RIGHT_toe_off_array)

#now try resizing
LH_length = len(LEFT_heel_on_array)
LT_length = len(LEFT_toe_off_array)

RH_length = len(RIGHT_heel_on_array)
RT_length = len(RIGHT_toe_off_array)

FSR_array_lengths = [LH_length, LT_length, RH_length, RT_length]
FSR_array_lengths_MINIMUM = min(FSR_array_lengths)

#now do the resize
LEFT_heel_on_array = LEFT_heel_on_array[0:FSR_array_lengths_MINIMUM]
LEFT_toe_off_array = LEFT_toe_off_array[0:FSR_array_lengths_MINIMUM]
RIGHT_heel_on_array = RIGHT_heel_on_array[0:FSR_array_lengths_MINIMUM]
RIGHT_toe_off_array = RIGHT_toe_off_array[0:FSR_array_lengths_MINIMUM]

#print resized arrays
print(LEFT_heel_on_array)
print(LEFT_toe_off_array)

print(RIGHT_heel_on_array)
print(RIGHT_toe_off_array)
