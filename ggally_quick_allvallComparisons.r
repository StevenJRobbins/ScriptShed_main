setwd("~/Desktop/1-Sandbox")
library(ggplot2)
library(tidyverse)
library(GGally) 

"""
Script uses ggally from R to make quick all vs all plots with correlation and significance testing, this wone with coloring and correlation values by user-defined group, now called "Group."

In the future, should give this an argparser to take input from command line, and should add an output file in addition to keeping the stdout output. 
"""

# Read and reshape data
random_values.df <- read.table(
  "Random_values_table_grouped.tsv",
  header = TRUE,
  sep = "\t"
)

# Remove the first column "VALUE" becaause otherwise ggpairs gives an error about non-numeric data
random_values.df <- random_values.df %>% select(-VALUE)

#ggpairs_plot <- ggpairs(random_values.df %>% select(where(is.numeric)))
ggpairs_plot <- ggpairs(random_values.df, mapping=ggplot2::aes(colour = Group))

print(ggpairs_plot)
