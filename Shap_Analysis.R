# Shot outcome model (XGBoost) + SHAP explanations
library(readr); library(dplyr); library(xgboost); library(shapviz)
set.seed(42)

# Data
df <- read_csv("C:/Users/bencr/Downloads/R/CS_2026/yds_cleaned.csv") %>%
  filter(!is.na(is_goal)) %>% # unlabelled rows can't be used for training
  mutate(
    time_left = remaining_min * 60 + remaining_sec,
    is_home = as.integer(grepl("vs\\.", `home/away`)), # "vs." = home, "@" = away
    season_start = as.integer(substr(game_season, 1, 4)),
    across(c(area_of_shot, shot_basics, range_of_shot), factor)
  )

cats <- c("area_of_shot", "shot_basics", "range_of_shot")
features <- c("distance_of_shot", "power_of_shot", "location_x", "location_y",
              "time_left", "knockout_match", "is_home", "season_start", cats)

# One-hot encode categories; keep NAs (XGBoost handles them natively)
to_matrix <- function(d) {
  op <- options(na.action = "na.pass"); on.exit(options(op))
  model.matrix(~ . - 1, data = d[, features])
}

# Train / validation split
idx <- sample(nrow(df), 0.8 * nrow(df))
train <- df[idx, ]; valid <- df[-idx, ]
X_tr <- to_matrix(train); X_va <- to_matrix(valid)
dtr <- xgb.DMatrix(X_tr, label = train$is_goal)

params <- list(objective = "binary:logistic", eval_metric = "logloss",
               max_depth = 4, eta = 0.05, subsample = 0.8,
               colsample_bytree = 0.8, min_child_weight = 5)

# Pick the number of rounds by 5-fold CV rather than guessing
cv <- xgb.cv(params, dtr, nrounds = 1000, nfold = 5, early_stopping_rounds = 30, verbose = 0)
n_best <- which.min(cv$evaluation_log$test_logloss_mean)
bst <- xgb.train(params, dtr, nrounds = n_best)

# Validation performance
p <- predict(bst, X_va); y <- valid$is_goal
auc <- (sum(rank(p)[y == 1]) - sum(y) * (sum(y) + 1) / 2) / (sum(y) * sum(1 - y))
ll <- function(q) -mean(y * log(q) + (1 - y) * log(1 - q))
cat(sprintf("Rounds: %d | AUC: %.3f | Log-loss: %.3f (baseline %.3f)\n", n_best, auc, ll(p), ll(rep(mean(train$is_goal), length(y)))))

# SHAP (on validation sample)
rows <- sample(nrow(X_va), min(2000, nrow(X_va)))
collapse <- setNames(lapply(cats, \(f) grep(paste0("^", f), colnames(X_va), value = TRUE)), cats)
shp <- shapviz(bst, X_pred = X_va[rows, ], X = as.data.frame(valid[rows, features]), collapse = collapse)

sv_importance(shp, kind = "bee") # importance and direction of effect
sv_dependence(shp, "distance_of_shot", color_var = "auto")
sv_dependence(shp, "power_of_shot", color_var = "auto")
sv_dependence2D(shp, x = "location_x", y = "location_y") # effect of shot location
sv_waterfall(shp, row_id = which.max(predict(bst, X_va[rows, ]))) # explain the best chance
plogis(c(-0.225, 1.14))