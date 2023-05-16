library(dplyr)

rm(list = ls())
wd = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/3-Normalized_RNFL_per_radius_in_ALL_eyes (v7)/3-code and required data"
setwd(wd)
data_file0 = "results-standard circle, standard clockhours.csv"
data_file1 = "results-fixed ellipse, standard clockhours.csv"
data_file2 = "results-aspect ratio adjusted ellipse, standard clockhours.csv"
data_file3 = "results-standard_circle, adjusted clockhours.csv"
data_file4 = "results-fixed ellipse, adjusted clockhours.csv"
data_file5 = "results-aspect ratio adjusted ellipse, adjusted clockhours.csv"

############# radius_from_CENTER_mm analysis #############
data_files = list(data_file0, data_file1, data_file2, data_file3, data_file4, data_file5)
for (data_file in data_files) {
  data=read.csv(data_file)
  
  data=data %>%
    group_by(subject_id) %>%
    summarise(radius_from_center_px=radius_from_center_px, 
              radius_from_center_mm=radius_from_center_mm,
              avg_rnfl_thickness_um=avg_rnfl_thickness_um,
              standardized_rnfl=avg_rnfl_thickness_um/median(avg_rnfl_thickness_um)
              )
  
  radius_center_summary= data %>%
    group_by(radius_from_center_mm) %>%
    summarise(avg_rnfl=mean(standardized_rnfl), sd_rnfl=sd(standardized_rnfl), sample_var=var(standardized_rnfl))

  radius_center_summary=radius_center_summary %>%
    mutate(cv=sd_rnfl/avg_rnfl)
  
  radius_center_summary=radius_center_summary %>%
    mutate(criteria1=avg_rnfl-cv)

  radius_center_summary=radius_center_summary %>%
    mutate(relative_variance=avg_rnfl-sample_var)
  
  print(data_file)
  filename <- paste("Analysis from center mm-", data_file)
  
  write.csv(radius_center_summary, file = filename, 
            row.names = F)
}

############# radius_from_MARGIN_mm analysis #############
data_files = list(data_file0, data_file1, data_file2, data_file3, data_file4, data_file5)
for (data_file in data_files) {
  data=read.csv(data_file)
  
  data=data %>%
    group_by(subject_id) %>%
    summarise(radius_from_margin_px=radius_from_margin_px, 
              radius_from_margin_mm=radius_from_margin_mm,
              avg_rnfl_thickness_um=avg_rnfl_thickness_um,
              standardized_rnfl=avg_rnfl_thickness_um/median(avg_rnfl_thickness_um)
    )
  
  radius_margin_summary= data %>%
    group_by(radius_from_margin_mm) %>%
    summarise(avg_rnfl=mean(standardized_rnfl), sd_rnfl=sd(standardized_rnfl), sample_var=var(standardized_rnfl))
  
  radius_margin_summary=radius_margin_summary %>%
    mutate(cv=sd_rnfl/avg_rnfl)
  
  radius_margin_summary=radius_margin_summary %>%
    mutate(criteria1=avg_rnfl-cv)
  
  radius_margin_summary=radius_margin_summary %>%
    mutate(relative_variance=avg_rnfl-sample_var)
  
  print(data_file)
  filename <- paste("Analysis from margin mm-", data_file)
  
  write.csv(radius_margin_summary, file = filename, 
            row.names = F)
}
