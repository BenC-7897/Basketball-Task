library(readr)
library(dplyr)
library(lubridate)
library(zoo)
library(ggplot2)

# Load data
df <- read_csv("C:/Users/bencr/Downloads/R/CS_2026/yds_cleaned.csv")

# Convert date
df$date_of_game <- as.Date(df$date_of_game)

# Aggregate by month WITH games only
monthly_goals <- df %>%
  mutate(
    year_month = floor_date(date_of_game, "month")
  ) %>%
  group_by(year_month) %>%
  summarise(
    monthly_goals = sum(is_goal, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(year_month) %>%
  mutate(
    MA_3 = rollmean(monthly_goals, 3, fill = NA, align = "right"),
    MA_6 = rollmean(monthly_goals, 6, fill = NA, align = "right")
  )

# Golden Crosses and Death Crosses
crosses <- monthly_goals %>%
  mutate(
    signal = case_when(
      lag(MA_3) < lag(MA_6) & MA_3 >= MA_6 ~ "Golden Cross",
      lag(MA_3) > lag(MA_6) & MA_3 <= MA_6 ~ "Death Cross",
      TRUE ~ NA_character_
    )
  ) %>%
  filter(!is.na(signal))

# Plot
p <- ggplot(monthly_goals, aes(x = year_month)) +
  
  geom_line(
    aes(y = monthly_goals,
        colour = "Monthly Goals"),
    linewidth = 0.8,
    alpha = 0.35
  ) +
  
  geom_line(
    aes(y = MA_3,
        colour = "3-Month MA"),
    linewidth = 1.3
  ) +
  
  geom_line(
    aes(y = MA_6,
        colour = "6-Month MA"),
    linewidth = 1.3
  ) +
  
  geom_smooth(
    aes(y = monthly_goals,
        colour = "Career Trend"),
    method = "loess",
    se = FALSE,
    linewidth = 1.4
  ) +
  
  # Golden Cross
  geom_point(
    data = subset(crosses, signal == "Golden Cross"),
    aes(y = MA_3),
    shape = 24,
    fill = "gold",
    colour = "black",
    size = 3.5
  ) +
  
  # Death Cross
  geom_point(
    data = subset(crosses, signal == "Death Cross"),
    aes(y = MA_3),
    shape = 25,
    fill = "red",
    colour = "black",
    size = 3.5
  ) +
  
  scale_x_date(
    date_breaks = "2 years",
    date_labels = "%Y"
  ) +
  
  coord_cartesian(
    ylim = c(0, 200)
  ) +
  
  scale_colour_manual(
    values = c(
      "Monthly Goals" = "slateblue2",
      "3-Month MA" = "#0072B2",
      "6-Month MA" = "#009E73",
      "Career Trend" = "#7B3294"
    )
  ) +
  
  labs(
    title = "Kobe Bryant Monthly Successful Shots Over Time",
    subtitle = "Monthly Volume, Moving Averages, Career Trend and Cross Signals",
    x = "Season",
    y = "Monthly Scored Shots",
    colour = NULL
  ) +
  
  theme_minimal(base_size = 13) +
  
  theme(
    plot.title = element_text(face = "bold", size = 16),
    plot.subtitle = element_text(size = 11),
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "bottom",
    aspect.ratio = 0.4
  )

print(p)

# Wider export for presentation
ggsave(
  "kobe_monthly_volume_trend.png",
  plot = p,
  width = 14,
  height = 6,
  dpi = 300
)