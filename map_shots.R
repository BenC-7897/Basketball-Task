# Install packages (run once)
install.packages(c("leaflet", "readr", "dplyr", "tidyr"))

# Load libraries
library(readr)
library(dplyr)
library(tidyr)
library(leaflet)

# Load data
df <- read_csv("C:/Users/bencr/Downloads/R/CS_2026/yds_cleaned.csv")

# Check coordinate format
print(head(df$`lat/lng`))

# Split coordinates
df <- df %>%
  separate(
    `lat/lng`,
    into = c("lat", "lng"),
    sep = ","
  ) %>%
  mutate(
    lat = as.numeric(trimws(lat)),
    lng = as.numeric(trimws(lng))
  )

# Remove invalid coordinates
df <- df %>%
  filter(!is.na(lat), !is.na(lng))

# Count goals by location
goal_counts <- df %>%
  filter(is_goal == 1) %>%
  group_by(lat, lng) %>%
  summarise(
    goals = n(),
    .groups = "drop"
  )

# Create map
leaflet(goal_counts) %>%
  addTiles() %>%
  addCircleMarkers(
    lng = ~lng,
    lat = ~lat,
    radius = ~sqrt(goals) ,
    color = "green",
    fillColor = "green",
    fillOpacity = 0.7,
    stroke = FALSE,
    popup = ~paste("Goals:", goals)
  )