## 3/4/23 - RNFL ONION MASTER v5
## ************************************************************************
## **************************** README ************************************
## ************************************************************************
##
## ________________________GENERAL PURPOSE__________________________________
## code for printing out the average, sectoral, clockhour rnfl at each pixel radius 
## USING DIFFERENT SAMPLING PATTERNS
## from disc center to scan window edge, using .txt files from
## hiroshi's spectral oct point by point export software.
## these data can be used to create an aggregate thickness profile
## in pixel by plotting the average rnfl thickness of all eyes at
## each radius. the results will print the oct file name, radius from
## disc center, radius from disc margin and average rnfl thickness at that
## distance. 
## [subject_eye, radius_from_center, radius_from_margin, avg_rnfl_thickness_um]
##
## ________________________INPUT / OUTPUT _________________________________
## Multiple files can be processed by creating a input.csv file with 
## the columns file_name, angle_correction, disc_margin	, disc_ratio.
## These were obtained by manually from enface screenshots of hiroshi's sw
## and angle and margins manually taken using FIJI. 
##
## ______________________PIXEL TO METRIC CONVERSION________________________
## hiroshi's point by point export gives data in pixel,
## so it must be converted to um by appropriate conversion factor in x,y,z
## z_px_to_um is 1.6 according to original (2019) bioptigen setting. 
## xy_px_to_um in a perfect 5x5mm field should be 12.5,
## but due to handheld nature of bioptigen probe should be corrected
## for magnification using eye specific eye biometry (we used ex vivo ONH).
## 
## ___________________________CALCULUS_____________________________________
## Parametric formula for ELLIPSES was used  to calculate coordinates
## x = h + a cos t    
##    where x = x-coordinate, h = center x coordinate, a = radius along x axis, 
##    t = the parameter, which ranges from 0 to 2π radians (0-360 deg)
## y = k + b sin t    
##    where y = y-coordinate, k = center y coordinate, b = radius along y axis, 
##    t = the parameter, which ranges from 0 to 2π radians (0-360 deg)
## For rotation of ellipse
## x1 = (a cos t * cos c) - (b sin t * sin c) + h   where c is rotational angle
## y1 = (a cos t * sin c) + (b sin t * cos c) + k
## monkey disc elipse shape is on average 1.33 vertical to 1 horizontal
## important to note: 12 o clock is -90 deg in python, 3 o clock is 0 deg

## _________________________EXTRA NOTES ___________________________________
## the OCT is actually flipped vertically so we want to report the results by 
## flipping through the horizontal axis ie. ch12=6, ch1=5, ch2=4, ch3=3, 
## ch7=11, ch8=10, ch9=9

## update v3: now adding columns for standard deviation, coefficient of variance,
## and ideal location criteria (average - cv) per radius. the hope is we can do
## per eye ideal location. removed image creation since already done in v2

## fixed issue in v5 where ellipse vertial radius was being written in csv 
## should be the horizontal radius since that is what is being used
## *************************************************************************

## dependancies
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv
import datetime
from PIL import Image
import os

# global variables
z_px_to_um = 1.6

## ************************** USER CHOOSES ANALYSIS ***************************  

while True:
    print('\n***********************************************************\nWelcome to the RNFL Onion Master! \n\n Please select the type of analysis you would like to perform:')
    print(' 1 - standard circle, standard clockhours')
    print(' 2 - fixed ellipse, standard clockhours')
    print(' 3 - aspect ratio adjusted ellipse, standard clockhours')
    print(' 4 - standard_circle, adjusted clockhours')
    print(' 5 - fixed ellipse, adjusted clockhours')
    print(' 6 - aspect ratio adjusted ellipse, adjusted clockhours')
    # print(' 0 - RUN ALL ANALYSES')
    try:
        user_input = int(input("\nEnter the analysis number of your choice: "))
    except ValueError:
        print("\nINVALID INPUT. Try again!\n")
        continue
    if user_input < 0 or user_input > 6:
        print("\nINVALID NUMBER. Try again!\n")
        continue
    else:
        break
    
if user_input == 1:
    script_name = 'standard circle, standard clockhours' 
if user_input == 2:
    script_name = 'fixed ellipse, standard clockhours' 
if user_input == 3:
    script_name = 'aspect ratio adjusted ellipse, standard clockhours'
if user_input == 4:
    script_name = 'standard_circle, adjusted clockhours' 
if user_input == 5:
    script_name = 'fixed ellipse, adjusted clockhours'
if user_input == 6:
    script_name = 'aspect ratio adjusted ellipse, adjusted clockhours' 

# # if user input is 0 then we loop through all of the analyses
# if user_input == 0:
#     script_name = 'ALL ANALYSES' 
   
print('\n***********************************************************\n\n' + script_name +' analysis selected\ncalculating RNFL averages (~60secs/file)....\n\n')

## *********************** CREATE AND GET FILES ***************************      
# create csv file with full export file_name, angle_correction, and disc_margin
with open('input.csv') as input_csvfile:
    input_csvfile_df = pd.read_csv(input_csvfile)
    
f_time = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
# create results csv with headers
with open('results-' + script_name + '-' + f_time + '.csv', 'w', newline='') as results_csvfile:
    rnfl_results_writer = csv.writer(results_csvfile, delimiter=',')
    rnfl_results_writer.writerow(['subject_eye', 'monkey', 'laterality', 'um/px', 'radius_from_center_px', 'radius_from_center_mm', 'radius_from_margin_px', 'radius_from_margin_mm', 'avg_rnfl_thickness_um', 'superior_rnfl_thickness_um', 'nasal_rnfl_thickness_um', 'inferior_rnfl_thickness_um', 'temporal_rnfl_thickness_um', 'clockhour-1_rnfl_thickness_um', 'clockhour-2_rnfl_thickness_um', 'clockhour-3_rnfl_thickness_um', 'clockhour-4_rnfl_thickness_um', 'clockhour-5_rnfl_thickness_um', 'clockhour-6_rnfl_thickness_um', 'clockhour-7_rnfl_thickness_um', 'clockhour-8_rnfl_thickness_um', 'clockhour-9_rnfl_thickness_um', 'clockhour-10_rnfl_thickness_um', 'clockhour-11_rnfl_thickness_um', 'clockhour-12_rnfl_thickness_um', 'sd', 'cv', 'criteria'])
    results_csvfile.close()

# create directory for Figures
cwd = os.getcwd()
path = cwd + '/Figures-' + script_name
isExist = os.path.exists(path)
if isExist == False:
    os.mkdir(path, 0o777)
 

## ************************** FUNCTIONS **********************************      
    
# degree to radians function
def to_rad(r):
    radians = r * ((math.pi)/180)
    return radians

# get array of x coordinates of ELLIPSE based on x = radius 
def get_coordinates(r, center_x, center_y, angle_corr, disc_ratio):
    circle_x_coordinates = []
    circle_y_coordinates = []
    
    # ***** THESE COORDINATE FORMULAS DEFINE THE  DIFFERENT SAMPLING TYPES ******
    for degrees in range(361):
        if user_input == 1:   # standard circle, standard clockhours
            x_coordinate = round(math.cos(to_rad(degrees)) * r + center_x) 
            y_coordinate = round(math.sin(to_rad(degrees)) * r + center_y)
        if user_input == 2: # fixed ellipse, standard clockhours
            x_coordinate = round(math.cos(to_rad(degrees)) * r + center_x) 
            y_coordinate = round(math.sin(to_rad(degrees)) * round(1.33 * r) + center_y)
        if user_input == 3: # aspect ratio adjusted ellipse, standard clockhours
            x_coordinate = round((r * (math.cos(to_rad(degrees)) * math.cos(to_rad(angle_corr+90)))) - (round(1.333 * r) * (math.sin(to_rad(degrees))) * (math.sin(to_rad(angle_corr+90)))) + center_x)
            y_coordinate = round((r * (math.cos(to_rad(degrees)) * math.sin(to_rad(angle_corr+90)))) + (round(1.333 * r) * (math.sin(to_rad(degrees))) * (math.cos(to_rad(angle_corr+90))))+ center_y)
        if user_input == 4:   # sstandard_circle, adjusted clockhours
            x_coordinate = round(math.cos(to_rad(degrees+angle_corr+90)) * r + center_x) 
            y_coordinate = round(math.sin(to_rad(degrees+angle_corr+90)) * r + center_y)  
        if user_input == 5:
            x_coordinate = round(math.cos(to_rad(degrees)) * r + center_x) 
            y_coordinate = round(math.sin(to_rad(degrees)) * round(disc_ratio * r) + center_y)
        if user_input == 6: 
            x_coordinate = round((r * (math.cos(to_rad(degrees)) * math.cos(to_rad(angle_corr+90)))) - (round(disc_ratio * r) * (math.sin(to_rad(degrees))) * (math.sin(to_rad(angle_corr+90)))) + center_x)
            y_coordinate = round((r * (math.cos(to_rad(degrees)) * math.sin(to_rad(angle_corr+90)))) + (round(disc_ratio * r) * (math.sin(to_rad(degrees))) * (math.cos(to_rad(angle_corr+90))))+ center_y)

        # breaks loop if reaches edge of grid
        if x_coordinate in range(1, 399) and y_coordinate in range(1, 399):
            circle_x_coordinates.append(x_coordinate)
            circle_y_coordinates.append(y_coordinate)
        else:
            circle_x_coordinates.clear()
            circle_y_coordinates.clear()
            print('reached edge at:', x_coordinate, ',', y_coordinate)
            return(circle_x_coordinates, circle_y_coordinates)
    return(circle_x_coordinates, circle_y_coordinates)

# get thickness of pixel at specific coordinates
def get_thickness(x,y,df):
    pixel_thickness = df.iloc[y][x]
    return pixel_thickness
    
# get average thickness of specified range
def get_average_thickness(oct_df, x_coordinates, y_coordinates, specified_range_a, specified_range_b, specified_array):
    temp_array = []    
    for i in specified_range_a:
        x = x_coordinates[i]
        y = y_coordinates[i]  
        if get_thickness(x, y, oct_df) != 933:
            temp_array.append(get_thickness(x, y, oct_df))
    for i in specified_range_b:
        x = x_coordinates[i]
        y = y_coordinates[i]  
        if get_thickness(x, y, oct_df) != 933:
            temp_array.append(get_thickness(x, y, oct_df))
    thickness_avg = (sum(temp_array)/ len(temp_array)) * z_px_to_um
    specified_array.append(thickness_avg)
        
def ch_angle_correction(prev_ch_range, prev_ch_var, ch_range_corr):
    # because some clockhours degrees are interrupted by the 0-360 border, we need to make two buckets (ch#a and ch#b) to include all degrees of one clock hours
    # get previous clock hour info
    prev_range_min = min(prev_ch_range)
    prev_range_max = max(prev_ch_range) + 1
    prev_range_var_name = prev_ch_var[-1]
    # if previous was ch#a bucket and it was complete then ch#b bucket is the same and avg of both will be the ch avg
    if (prev_range_max - prev_range_min) == 30 and prev_range_var_name == 'a':
        return range(prev_range_min, prev_range_max)
    else:
        ch_range_min = prev_range_max
        ch_range_max = ch_range_min + 30  
        
        if prev_range_max == 360: # have to start ch_min at 0 , ch_max is deg needed to make ch a full 30 deg
            ch_range_min = 0
            if (360 - prev_range_min) == 30: # in case previous ch already has 30 deg
                ch_range_max = 30
            else:
                ch_range_max = 30 - (360 - prev_range_min)
            return range(ch_range_min, ch_range_max)       
        if ch_range_max > 360: # cant go over 360 degrees
            ch_range_max = 360
            return range(ch_range_min, ch_range_max)
        if ch_range_min >= 0 and ch_range_max <= 360: # degrees must be 0-360
            return range(ch_range_min, ch_range_max)
        
        
def px_to_mm(um_per_px, radius_in_px):
    radius_in_mm = round((um_per_px * radius_in_px)/1000,2)
    return radius_in_mm
            
# main function  
def main(df, user_input):

    for index, row in df.iterrows():        
        # get variables from csv columns per row
        file_name = row['file_name']
        print(file_name)
        file_path = 'RNFL_full_export_files/' + row['file_name']
        angle_corr = row['angle_correction']
        disc_margin = row['disc_margin']
        disc_ratio = row['disc_ratio']
        laterality = row['laterality']
        um_per_px = row['um/px']
        monkey = row['monkey']
        
        # for calculating elapsed time
        start_time = datetime.datetime.now()
        
        # turn file_csv to dataframe
        oct_df = pd.read_csv(file_path, header=None)
    
        # get center values from txt file name
        center_x =int(file_name[-13:-10])
        center_y =int(file_name[-8:-5])
        
        # according to Pal fundus photo discovery, the OCT is actually flipped vertically so we want to report the results by flipping through the horizontal axis ie. ch12=6, ch1=5, ch2=4, ch3=3, ch7=11, ch8=10, ch9=9
        
        # range for clockhours
        range_ch7a = range(285,315)
        range_ch7b = range(285,315)
        range_ch8a = range(315, 345)
        range_ch8b = range(315, 345)
        range_ch9a = range(345,360)
        range_ch9b = range(0,15)
        range_ch10a = range(15, 45)
        range_ch10b = range(15, 45)
        range_ch11a = range(45,75)
        range_ch11b = range(45,75)
        range_ch12a = range(75,105)
        range_ch12b = range(75,105)
        range_ch1a = range(105,135)
        range_ch1b = range(105,135)
        range_ch2a = range(135,165)
        range_ch2b = range(135,165)
        range_ch3a = range(165, 195)
        range_ch3b = range(165, 195)
        range_ch4a = range(195, 225)
        range_ch4b = range(195, 225)
        range_ch5a = range(225,255)
        range_ch5b = range(225,255)
        range_ch6a = range(255,285)
        range_ch6b = range(255,285)
        # flip clock hours if OS (except ch6 and ch12)
        if laterality == 'OS':
            temp = range_ch1a
            range_ch1a = range_ch11a
            range_ch11a = temp
            temp = range_ch1b
            range_ch1b = range_ch11b
            range_ch11b = temp
            temp = range_ch2a
            range_ch2a = range_ch10a
            range_ch10a = temp
            temp = range_ch2b
            range_ch2b = range_ch10b
            range_ch10b = temp
            temp = range_ch3a
            range_ch3a = range_ch9a
            range_ch9a = temp
            temp = range_ch3b
            range_ch3b = range_ch9b
            range_ch9b = temp
            temp = range_ch4a
            range_ch4a = range_ch8a
            range_ch8a = temp
            temp = range_ch4b
            range_ch4b = range_ch8b
            range_ch8b = temp
            temp = range_ch5a
            range_ch5a = range_ch7a
            range_ch7a = temp
            temp = range_ch5b
            range_ch5b = range_ch7b
            range_ch7b = temp

        # arrays for rnfl averages per radius 
        avg_array = []
        ch1_array = []
        ch2_array = []
        ch3_array = []
        ch4_array = []
        ch5_array = []
        ch6_array = []
        ch7_array = []
        ch8_array = []
        ch9_array = []
        ch10_array = []
        ch11_array = []
        ch12_array = []
    
        # plot sampling circles on 400 x 400 grid
        fig, ax = plt.subplots(figsize=(7,7),constrained_layout=True)
        plt.title(file_name)
        ax.set_xlim(0,400)
        ax.set_ylim(400,0)
        plt.yscale('linear')
    
        # set values for circle
        if user_input == 1 or user_input == 4: 
            starting_circle_radius = disc_margin # currently at 118 as hiroshi's software is now ... future plan will be to get all circle values
        else:
            starting_circle_radius = disc_margin * (1/disc_ratio)
            
        max_r = 0 # for saving maximum radius
        try:
            for r in range(200): #200 is if center is 200,200, will be less otherwise depending on center the loop will break when reaching the edge of the frame
                x_coordinates, y_coordinates = [],[]
                r = round(r + starting_circle_radius)
                x_coordinates, y_coordinates  = get_coordinates(r, center_x, center_y, angle_corr, disc_ratio)
                
                # check if you reached the edge of the window
                if len(x_coordinates)== 0 or len(y_coordinates)== 0: # in get_coordinates an empty coordinates array means its already beyond the 1,399 pixel bounds 
                    max_r = r
                    # avg_array.clear()
                    break
    
                if len(x_coordinates)>359 and len(y_coordinates)>359:
                    ax.plot(center_x, center_y, marker="+", markersize=20)
                    ax.plot(x_coordinates, y_coordinates)
                    
                    # get global avg 
                    avg_temp_array = []
                    
                    for i in range(360):
                        x = x_coordinates[i]
                        y = y_coordinates[i]  
                        if get_thickness(x, y, oct_df) != 933: # for some reason the very first row of values in the point by point export are all equal to 933 and should be omitted from analysis
                            avg_temp_array.append(get_thickness(x, y, oct_df))
                    thickness_avg = (sum(avg_temp_array)/ len(avg_temp_array)) * z_px_to_um
                    # print(r, thickness_avg, len(avg_array))
                    avg_array.append(thickness_avg)   
                    
                    # get average thickness of clockhours
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch1a, range_ch1b, ch1_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch2a, range_ch2b, ch2_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch3a, range_ch3b, ch3_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch4a, range_ch4b, ch4_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch5a, range_ch5b, ch5_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch6a, range_ch6b, ch6_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch7a, range_ch7b, ch7_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch8a, range_ch8b, ch8_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch9a, range_ch9b, ch9_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch10a, range_ch10b, ch10_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch11a, range_ch11b, ch11_array)
                    get_average_thickness(oct_df, x_coordinates, y_coordinates, range_ch12a, range_ch12b, ch12_array)
   
        except IndexError:
             print('* max radius from disc center: ', r)
             pass                                                      
        
        # write average of all circles within each radius donut to csv
        radius_count = int(starting_circle_radius - 1)
        sampling_circle_count = max_r - radius_count - 1 #number of sampling circles from margin to scan window edge
        # print('max_ radius:', max_r)
        # print('disc_margin:', disc_margin)
        # print('center x, y:', center_x, center_y)
        # print('num of sampling circles:', sampling_circle_count)
        # print('avg_array_len (should match sampling_circles): ', len(avg_array))
 # the OCT is actually flipped vertically so we want to report the results by flipping through the horizontal axis ie. ch12=6, ch1=5, ch2=4, ch3=3, ch7=11, ch8=10, ch9=9
        for j in range(len(avg_array)):
            radius_count = radius_count + 1
            radius_from_center_mm = px_to_mm(um_per_px, radius_count)
            radius_from_margin_mm = px_to_mm(um_per_px, j)
            sup_values = (ch11_array[j] + ch12_array[j] + ch1_array[j])/3
            inf_values = (ch5_array[j] + ch6_array[j] + ch7_array[j])/3
            nas_values = (ch8_array[j] + ch9_array[j] + ch10_array[j])/3
            tem_values = (ch2_array[j] + ch3_array[j] + ch4_array[j])/3
            avg_values = (sup_values + nas_values + inf_values + tem_values)/4
            # write data per row to csv
            with open('results-' + script_name + '-' + f_time + '.csv', 'a', newline='') as results_csvfile:
                rnfl_results_writer = csv.writer(results_csvfile, delimiter=',')
                rnfl_results_writer.writerow([file_name] + [monkey] + [laterality] + [um_per_px] + [radius_count] + [radius_from_center_mm] + [j] + [radius_from_margin_mm] + [avg_values] + [sup_values] + [nas_values] + [inf_values] + [tem_values] + [ch1_array[j]] + [ch2_array[j]] + [ch3_array[j]] + [ch4_array[j]] + [ch5_array[j]] + [ch6_array[j]] + [ch7_array[j]] + [ch8_array[j]] + [ch9_array[j]] + [ch10_array[j]] + [ch11_array[j]] + [ch12_array[j]])
        results_csvfile.close()
    
        # add 800 x 800 enface OCT enface screenshot to plot grid *** note device en face image and OCT data is actually flipped vertically
        img = Image.open('Enface_Screenshots/' + file_name[:-4] + '.png')
        img = img.resize((400, 400), Image.ANTIALIAS)
        plt.imshow(img)

        # save plots to file
        plt.savefig('Figures-' + script_name +'/' + file_name +'.png')

        # print to console that file is done
        end_time = datetime.datetime.now()
        print('                    '+ str((end_time - start_time)) + ' s') 
    
# ******************************* EXECUTE ************************************
        
overall_start_time = datetime.datetime.now()      
main(input_csvfile_df, user_input)
overall_end_time = datetime.datetime.now()
print(script_name +' analysis completed in....' + str((overall_end_time - overall_start_time)) + 'mins.')

