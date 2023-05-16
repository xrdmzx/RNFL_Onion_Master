library(lme4)
library(lmerTest)

rm(list = ls())

estimate="/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/5-Eye_specific_VS_estimated_um-px_RNFL_analysis (v7)/5-code and required data/data in mm - estimate 10 um-px"
specific="/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/5-Eye_specific_VS_estimated_um-px_RNFL_analysis (v7)/5-code and required data/data in mm - eye specific um-px"

estimate_data=list()
specific_data=list()
for (i in 1:6){
  path_est=paste(estimate, "/estimate_", i, ".csv", sep = "")
  path_spe=paste(specific, "/estimate_", i, ".csv", sep = "")
  estimate_data[[i]]=read.csv(path_est)
  specific_data[[i]]=read.csv(path_spe)
}

parameter=c("avg_rnfl_thickness_um","superior_rnfl_thickness_um",    
            "nasal_rnfl_thickness_um","inferior_rnfl_thickness_um",    
            "temporal_rnfl_thickness_um","clockhour.1_rnfl_thickness_um", 
            "clockhour.2_rnfl_thickness_um","clockhour.3_rnfl_thickness_um", 
            "clockhour.4_rnfl_thickness_um","clockhour.5_rnfl_thickness_um", 
            "clockhour.6_rnfl_thickness_um","clockhour.7_rnfl_thickness_um", 
            "clockhour.8_rnfl_thickness_um","clockhour.9_rnfl_thickness_um", 
            "clockhour.10_rnfl_thickness_um","clockhour.11_rnfl_thickness_um",
            "clockhour.12_rnfl_thickness_um")

results=list()
for (j in parameter){
  for (i in 1:6){
    # test_radius = 1.1 #prev r
    # test_radius = 1.09 #ellipse r
    # test_radius = 1.06 #circle r
    test_radius = 1.36 #conventional 1.7mm/12.5um/px
    estimate=subset(estimate_data[[i]], radius_from_center_mm==test_radius)
    specific=subset(specific_data[[i]], radius_from_center_mm==test_radius)
    estimate$method="estimate"
    specific$method="specific"
    compare=rbind(estimate, specific)
    formula=paste(j, "~method+(1|monkey)")
    results=c(results, list(i, j, 
                            coef(summary(lmer(formula, data = compare)))))
  }
}
results_dir = "/Users/zambrr02/Documents/NYU/_Lab Projects/Ronald - Preferred OCT Sampling Location in NHP Manuscript/Manuscript revision/_Data/27- FULL DATA RUN (v7)/5-Eye_specific_VS_estimated_um-px_RNFL_analysis (v7)/5-results/"
capture.output(results, file = paste(results_dir, "estimated_vs_specific_um-px--", test_radius, "mm.txt",sep=""))

