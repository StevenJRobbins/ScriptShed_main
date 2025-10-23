setwd("~/Desktop/1-Sandbox")
library(ggplot2)
library(tidyverse)
library(ggh4x)

# Read and reshape data
random_values.df <- read.table(
  "Random_values_table.tsv",
  header = TRUE,
  sep = "\t"
)

#convert table into long format, where each row is a single observation repeating the column names into a new "Sample" column and the values into a "Value" column. 
longdata <- random_values.df %>%
  pivot_longer(
    cols = starts_with("Sample"),
    names_to = "Sample",
    values_to = "Value"
  )

# Define facet colors for label strips
facet_colors <- c(
  "Sample_1" = "seagreen",
  "Sample_2" = "skyblue",
  "Sample_3" = "orange",
  "Sample_4" = "purple",
  "Sample_5" = "pink",
  "Sample_6" = "gold",
  "Sample_7" = "turquoise",
  "Sample_8" = "brown"
)

# --- Faceted Plot with wider boxes and points ---
P <- ggplot(longdata, aes(x = 1, y = Value)) + #setting x=1 to center boxplots, if x = Sample then they were misaligned.
  geom_boxplot(
    width = 0.7,  # wider boxes, but I resized the whole plot later to compensate
    outlier.shape = 21, #set shape of outlier points to match normal data points. NOTE: outliers are automatically drawn by geom_boxplot unless outlier.shape = NA
    outlier.size = 2,
    outlier.alpha = 0.8, #NOTE: THIS REMOVES OUTLIERS TO PREVENT OVERLAP WITH JITTERED POINTS. This is what "fixed" the jumping points bug in previous version, but would hide some data points that are outliers.
    color = "black", #sets the color of the box
    fill = "#96bddd" #sets the fill of the box
  ) +
  geom_jitter(
    width = 0.3,           # slightly more jitter
    shape = 21,
    size = 2,
    color = "black", #sets the color of the data points
    fill = "#96bddd", #sets the fill of the data points
    alpha = 0.8
  ) +
  ggh4x::facet_wrap2( #facet wrapping with colored strips
    ~ Sample,
    nrow = 2,              # 2 rows of facets
    scales = "free_y",  #gives own independent y-axis scales, could have also been "fixed" to have same y-axis across facets or "free" to allow both x and y to vary.
    strip = ggh4x::strip_themed( #customize the strip appearance
      background_x = ggh4x::elem_list_rect(fill = facet_colors) #apply the custom colors defined earlier
    )
  ) +
  scale_x_continuous(labels = NULL) + #remove x-axis labels
  labs(x = NULL, y = "Value") + #hardcode y-axis label as "Value"
  theme_bw() + #use a black and white theme
  theme( #customize theme elements
    axis.text.x = element_blank(), #remove x-axis text
    axis.ticks.x = element_blank(), #remove ticks at bottom on x-axis
    strip.text = element_text(face = "bold", size = 12), #bold facet strip text
    panel.spacing = unit(0.1, "lines"), #increase space between facets
    panel.grid = element_blank() #remove grid lines for cleaner look
  )

# --- Make the whole plot wider on screen ---
ggsave("wide_facets_plot.png", P, width = 10, height = 6, dpi = 300) #saved file as wider image file to make boxes look less skinny
print(P) #show the plot in RStudio live viewer
