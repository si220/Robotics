#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009
import brickpi3
import time
import random
import os

BP = brickpi3.BrickPi3()
# BP.SENSOR_TYPE.NXT_ULTRASONIC specifies that the sensor will be an NXT ultrasonic sensor.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_ULTRASONIC)
# restricting speed of motors
BP.set_motor_limits(BP.PORT_D, 50, 200)
BP.set_motor_limits(BP.PORT_C, 50, 200)

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 360):
        self.sig = [0] * no_bins
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print(self.sig[i])

# --------------------- File management class ---------------

class SignatureContainer():
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;
 
    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print("STATUS:  All signature files removed.")
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.

    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();
    
    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close();
        else:
            print("WARNING: Signature does not exist.")
        
        return ls
#______________________________________________________________________________________________________________ 4.1

def fetch_sensor_readings():
    try:
        value = BP.get_sensor(BP.PORT_2)
        return value
    except brickpi3.SensorError as error:
        print(error)
        return None    

def turn(turn_degrees):
    #reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    degrees_to_encoder_ratio = 210/90
    encoder_angle = degrees_to_encoder_ratio * turn_degrees

    # turn angle_a degrees left
    BP.set_motor_position(BP.PORT_C, encoder_angle)
    BP.set_motor_position(BP.PORT_D, - encoder_angle) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
    

    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

    fetch_sensor_readings()

#______________________________________________________________________________________________________________ 4.1

#--------------------------------------------------------------------------------------------------------------

#______________________________________________________________________________________________________________ 4.2
       
# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    #print "TODO:    You should implement the function that captures a signature."
    for i in range(len(ls.sig)):
        ls.sig[i] = turn(1)

# FILL IN: compare two signatures
def compare_signatures(ls1, ls2):
    dist = 0
    #print "TODO:    You should implement the function that compares two signatures."
    for i in range(len(ls1.sig)):
        squared_diff = (ls1[i] - ls2[i])**2
        dist += squared_diff
    return dist

# This function characterizes the current location, and stores the obtained 
# signature into the next available file.
def learn_location():
    ls = LocationSignature()
    characterize_location(ls)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print("\nWARNING:")
        print("No signature file is available. NOTHING NEW will be learned and stored.")
        print("Please remove some loc_%%.dat files.\n")
        return
    
    signatures.save(ls,idx)
    print("STATUS:  Location " + str(idx) + " learned and saved.")

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen

def recognize_location():
    ls_obs = LocationSignature(); #ls_obs where we are right now
    characterize_location(ls_obs);

    lowest_dist = float('inf')

    for i in range(0, 359):
        ls_obs = ls_obs[-i:] + ls_obs[:-i]
        
    # FILL IN: COMPARE ls_read with ls_obs and find the best match
        for idx in range(signatures.size):
            print("STATUS:  Comparing signature " + str(idx) + " with the observed signature.")
            ls_read = signatures.read(idx)

            dist    = compare_signatures(ls_obs, ls_read)
            
            if dist < lowest_dist:
                lowest_dist = dist
                best_sig = ls_read
                best_idx = idx
            #________________________________________________________________________
            # so to terminate the for loop as we are looping if we dont find a better 
            #_________________________________________________________________________
            #best_sig is the array / histogram of the closest signature a
            #best_idx is the index of the closest sig.

            print(f'best index = {best_idx}')

            return best_sig

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files(). 
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

signatures = SignatureContainer(5);
#signatures.delete_loc_files()

learn_location();
recognize_location();

#______________________________________________________________________________________________________________ 4.2

# they he explained it loop the recieved sig by 1 degree and compare with 5 current sigs then use if statements to see if it matches closely
# the 5 sigs are saved in ls

