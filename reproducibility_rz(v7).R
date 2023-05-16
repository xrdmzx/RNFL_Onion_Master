library(readxl)
library(dplyr)
# make sure to run wscv
# rm(list = ls()) 

# ALL DATA
repro_data=c("results-standard circle, standard clockhours-repro.csv",
             "results-fixed ellipse, standard clockhours-repro.csv",
             "results-aspect ratio adjusted ellipse, standard clockhours-repro.csv",
             "results-standard circle, adjusted clockhours-repro.csv",
             "results-fixed ellipse, adjusted clockhours-repro.csv",
             "results-aspect ratio adjusted ellipse, adjusted clockhours-repro.csv"
)

reproducibility=list()
for (repro in repro_data){

path=paste("/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/9-Reproducibility_in_all_eyes/9-required code and data/", 
           repro, sep = "")
  
data=read.csv(path)

data=data[!duplicated(data), ] #all radii
# data=subset(data, radius_from_center_px==136) #conventional location
# data=subset(data, radius_from_center_mm==1.05) #circle ideal location
data=subset(data, radius_from_center_mm==0.86) #ellipse ideal location

data$id=paste(data$monkey, data$laterality, 
               data$radius_from_center_px, sep = "_")

names(data)[1]="subject_id"

table=data %>%
  group_by(id) %>%
  summarise(n=length(unique(subject_id)))


id_full=table[table$n==2, "id"]

data=subset(data, id %in% id_full$id)

all_monkey=unique(data$monkey)
# parameter=c("avg_rnfl_thickness_um","superior_rnfl_thickness_um",
#             "nasal_rnfl_thickness_um", "inferior_rnfl_thickness_um",
#             "temporal_rnfl_thickness_um", "clockhour.1_rnfl_thickness_um",
#             "clockhour.2_rnfl_thickness_um", "clockhour.3_rnfl_thickness_um",
#             "clockhour.4_rnfl_thickness_um", "clockhour.5_rnfl_thickness_um",
#             "clockhour.6_rnfl_thickness_um", "clockhour.7_rnfl_thickness_um",
#             "clockhour.8_rnfl_thickness_um", "clockhour.9_rnfl_thickness_um",
#             "clockhour.10_rnfl_thickness_um", "clockhour.11_rnfl_thickness_um",
#             "clockhour.12_rnfl_thickness_um")

parameter=c("avg_rnfl_thickness_um","superior_rnfl_thickness_um",
            "nasal_rnfl_thickness_um", "inferior_rnfl_thickness_um",
            "temporal_rnfl_thickness_um")

wscv=data.frame()
for (i in parameter){
  matrix=data.frame()
  for (subject in all_monkey){
    for (eye in c("OD", "OS")){
      subdata=subset(data, monkey==subject & laterality==eye)
      scan=unique(subdata$subject_id)
      scan1=subset(subdata, subject_id==scan[1])
      scan1=data.frame(id=scan1$id, par1=scan1[, i])
      scan2=subset(subdata, subject_id==scan[2])
      scan2=data.frame(id=scan2$id, par2=scan2[, i])
      subdata=merge(scan1, scan2, by="id")
      matrix=rbind(matrix, subdata)
    }
  }
  wscv=rbind(wscv, c(i, unlist(agree.wscv(as.matrix(matrix[, 2:3])))))
}

names(wscv)=c("parameters", "wscv", "lbound", "ubound")

reproducibility=c(reproducibility, list(repro, no_eyes=length(id_full$id), wscv))

}
results_dir = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/9-Reproducibility_in_all_eyes/9-results/"
# capture.output(reproducibility, file = paste(results_dir,"repro_wsvc at 136px.txt"))
# capture.output(reproducibility, file = paste(results_dir,"repro_wsvc at 1.05mm.txt"))
capture.output(reproducibility, file = paste(results_dir,"repro_wsvc at 1.14mm.txt"))

