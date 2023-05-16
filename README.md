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
