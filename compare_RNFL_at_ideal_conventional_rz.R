library(dplyr)
library(lme4)
library(lmerTest)

rm(list=ls())

#all eyes analysis
dir = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/4-Comparing RNFL values at Ideal vs Conventional Location (v7)/4-code and required data/"
ideal=read.csv(paste(dir, "Ideal_location_ONLY_RNFL_measurements.csv", sep=""))
conventional=read.csv(paste(dir, "Conventional_Location_ONLY_RNFL_measurements.csv", sep=""))

names(ideal)[1]="method"
names(conventional)[1]="method"

ideal$compare="ideal"
conventional$compare="conventional"

parameter=c("avg_rnfl_thickness_um", "superior_rnfl_thickness_um",
            "nasal_rnfl_thickness_um", "inferior_rnfl_thickness_um",
            "temporal_rnfl_thickness_um", "clockhour.1_rnfl_thickness_um", 
            "clockhour.2_rnfl_thickness_um", "clockhour.3_rnfl_thickness_um",
            "clockhour.4_rnfl_thickness_um", "clockhour.5_rnfl_thickness_um",
            "clockhour.6_rnfl_thickness_um", "clockhour.7_rnfl_thickness_um",
            "clockhour.8_rnfl_thickness_um", "clockhour.9_rnfl_thickness_um",
            "clockhour.10_rnfl_thickness_um", "clockhour.11_rnfl_thickness_um",
            "clockhour.12_rnfl_thickness_um")

method=unique(ideal$method)

results=list()
for (i in method){
  sub_ideal=subset(ideal, method==i)
  sub_conventional=subset(conventional, method==i)
  sub_data=rbind(sub_ideal, sub_conventional)
  for (j in parameter){
    formula=paste(j, "~compare+(1|monkey)")
    results=c(results, list(i, j, coef(summary(lmer(formula, data=sub_data)))))
  }
}

results_dir = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/4-Comparing RNFL values at Ideal vs Conventional Location (v7)/4-results/"
capture.output(results, file = paste(results_dir, "summary-all_eyes--IDEAL_vs_CONVENTIONAL.txt"))
