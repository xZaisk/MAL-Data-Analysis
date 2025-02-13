# Load necessary libraries
library(dplyr)
library(readr)
library(stringr)  


# Load dataset (update the path)
df <- read_csv("C:/Users/khaos/Documents/UM/DSC project/mal_anime_list.csv")

# View the first few rows
head(df)

# Check dataset dimensions
cat("Dataset contains", nrow(df), "rows and", ncol(df), "columns.\n")

# View column names
colnames(df)

# Count missing values in each column
colSums(is.na(df))


# Drop rows where critical values are missing
df <- df %>% 
  filter(!is.na(rank) & !is.na(mean) & !is.na(popularity) & !is.na(num_episodes) & !is.na(media_type))

# Fill Missing Categorical Values
#df <- df %>%
#  mutate(
#    studios = ifelse(is.na(studios), "Unknown", studios),
#    genres = ifelse(is.na(genres), "Unknown", genres),
#    status = ifelse(is.na(status), "Unknown", status),
#    source = ifelse(is.na(source), "Unknown", source),
#    synopsis = ifelse(is.na(synopsis), "Unknown", synopsis)
#  )

# Replace NA, Empty Strings (""), and Whitespace (" ")
df <- df %>%
  mutate(
    studios = ifelse(is.na(studios) | studios == "" | str_trim(studios) == "", "Unknown", studios),
    genres = ifelse(is.na(genres) | genres == "" | str_trim(genres) == "", "Unknown", genres),
    status = ifelse(is.na(status) | status == "" | str_trim(status) == "", "Unknown", status),
    source = ifelse(is.na(source) | source == "" | str_trim(source) == "", "Unknown", source),
    synopsis = ifelse(is.na(synopsis) | synopsis == "" | str_trim(synopsis) == "", "Unknown", synopsis)
  )



# converting start date end date data types
df <- df %>%
  mutate(start_date = as.Date(start_date, format = "%m/%d/%Y"))

# handling Missing end_date for Ongoing Anime
df <- df %>%
  mutate(
    end_date = as.Date(ifelse(end_date == "N/A", NA, end_date), format = "%m/%d/%Y")
  )

# turn certain categorical columns into factor ()
df <- df %>%
  mutate(
    status = as.factor(status),
    rating = as.factor(rating),
    media_type = as.factor(media_type),
    source = as.factor(source)
  )


#checks
table(df$end_date)  # Ensure "Ongoing" is present


