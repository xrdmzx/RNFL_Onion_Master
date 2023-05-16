library(ggplot2)
library(reshape)
# rm(list = ls())
# ANALYSIS PER PIXEL
data_names=c("results-standard circle, standard clockhours-repro.csv",
             "results-fixed ellipse, standard clockhours-repro.csv",
             "results-aspect ratio adjusted ellipse, standard clockhours-repro.csv",
             "results-standard circle, adjusted clockhours-repro.csv",
             "results-fixed ellipse, adjusted clockhours-repro.csv",
             "results-aspect ratio adjusted ellipse, adjusted clockhours-repro.csv"
)
wscv_list=list()
for (k in 1:6){
dir = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/9-Reproducibility_in_all_eyes/9-required code and data/"
path=paste(dir, data_names[k], sep = "")
data=read.csv(path)

data$id=paste(data$monkey, data$laterality, data$radius_from_center_px, sep = "_")

data=subset(data, !id %in% names(which(table(data$id)==1)))
data$id=paste(data$monkey, data$laterality, sep = "_")

wscv=data.frame()
for (i in sort(unique(data$radius_from_center_px))){
  sub_data=subset(data, radius_from_center_px==i)
  avg=matrix(NA, nrow = 0, ncol = 2)
  sup=matrix(NA, nrow = 0, ncol = 2)
  nas=matrix(NA, nrow = 0, ncol = 2)
  inf=matrix(NA, nrow = 0, ncol = 2)
  temp=matrix(NA, nrow = 0, ncol = 2)
  for (j in unique(sub_data$id)){
    sub_data.1=subset(sub_data, id==j)
    avg=rbind(avg, sub_data.1[, "avg_rnfl_thickness_um"])
    sup=rbind(sup, sub_data.1[, "superior_rnfl_thickness_um"])
    nas=rbind(nas, sub_data.1[, "nasal_rnfl_thickness_um"])
    inf=rbind(inf, sub_data.1[, "inferior_rnfl_thickness_um"])
    temp=rbind(temp, sub_data.1[, "temporal_rnfl_thickness_um"])
  }
  if (nrow(avg)>1){
    wscv=rbind(wscv, c(i, agree.wscv(avg)$value, agree.wscv(sup)$value, 
             agree.wscv(nas)$value, agree.wscv(inf)$value,
             agree.wscv(temp)$value))}
}

names(wscv)=c("radius_from_center_px", "Avg_RNFL", "Sup_RNFL", 
              "Nas_RNFL", "Inf_RNFL", "Temp_RNFL")
wscv_list[[k]]=wscv
csv_file = paste("wscv_per_radius_pixel--",data_names[k], sep = "")
write.csv(wscv_list[[k]], paste(dir, csv_file, sep = ""))

}

names(wscv_list)=data_names

for (i in 1:6){
  ggplot(data = melt(wscv_list[[i]], id="radius_from_center_px"), aes(radius_from_center_px, value, group=variable, color=variable))+
    geom_line()+theme(axis.text.x = element_text(angle = 90))+
    labs(x="radius from center px", y="within subject coefficient of variation", 
         title=data_names[i])
  ggsave(path = dir, filename = paste("wscv_pixel--",data_names[i], ".png", sep=""))
}



######################################################################
######################################################################
######################################################################


# ANALYSIS PER MM
data_names=c("results-standard circle, standard clockhours-repro.csv",
             "results-fixed ellipse, standard clockhours-repro.csv",
             "results-aspect ratio adjusted ellipse, standard clockhours-repro.csv",
             "results-standard circle, adjusted clockhours-repro.csv",
             "results-fixed ellipse, adjusted clockhours-repro.csv",
             "results-aspect ratio adjusted ellipse, adjusted clockhours-repro.csv"
)
wscv_list=list()
for (k in 1:6){
  dir = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/9-Reproducibility_in_all_eyes/9-required code and data/"
  path=paste(dir, data_names[k], sep = "")
  data=read.csv(path)
  
  data$id=paste(data$monkey, data$laterality, data$radius_from_center_mm, sep = "_")
  
  data=subset(data, !id %in% names(which(table(data$id)==1)))
  data$id=paste(data$monkey, data$laterality, sep = "_")
  
  wscv=data.frame()
  for (i in sort(unique(data$radius_from_center_mm))){
    sub_data=subset(data, radius_from_center_mm==i)
    avg=matrix(NA, nrow = 0, ncol = 2)
    sup=matrix(NA, nrow = 0, ncol = 2)
    nas=matrix(NA, nrow = 0, ncol = 2)
    inf=matrix(NA, nrow = 0, ncol = 2)
    temp=matrix(NA, nrow = 0, ncol = 2)
    for (j in unique(sub_data$id)){
      sub_data.1=subset(sub_data, id==j)
      avg=rbind(avg, sub_data.1[, "avg_rnfl_thickness_um"])
      sup=rbind(sup, sub_data.1[, "superior_rnfl_thickness_um"])
      nas=rbind(nas, sub_data.1[, "nasal_rnfl_thickness_um"])
      inf=rbind(inf, sub_data.1[, "inferior_rnfl_thickness_um"])
      temp=rbind(temp, sub_data.1[, "temporal_rnfl_thickness_um"])
    }
    if (nrow(avg)>1){
      wscv=rbind(wscv, c(i, agree.wscv(avg)$value, agree.wscv(sup)$value, 
                         agree.wscv(nas)$value, agree.wscv(inf)$value,
                         agree.wscv(temp)$value))}
  }
  
  names(wscv)=c("radius_from_center_px", "Avg_RNFL", "Sup_RNFL", 
                "Nas_RNFL", "Inf_RNFL", "Temp_RNFL")
  wscv_list[[k]]=wscv
  csv_file = paste("wscv_per_radius_mm--",data_names[k], sep = "")
  write.csv(wscv_list[[k]], paste(dir, csv_file, sep = ""))
  
}

names(wscv_list)=data_names

for (i in 1:6){
  ggplot(data = melt(wscv_list[[i]], id="radius_from_center_px"), aes(radius_from_center_px, value, group=variable, color=variable))+
    geom_line()+theme(axis.text.x = element_text(angle = 90))+
    labs(x="radius from center (mm)", y="within subject coefficient of variation", 
         title=data_names[i])
  ggsave(path = dir, filename = paste("wscv_pixel--",data_names[i], ".png", sep=""))
}



