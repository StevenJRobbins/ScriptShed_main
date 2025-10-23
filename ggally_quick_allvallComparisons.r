setwd("~/Desktop/1-Sandbox")
library(ggplot2)
library(tidyverse)
library(GGally) 

"""
Test ggally functionality with coloring and correlation by group.
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