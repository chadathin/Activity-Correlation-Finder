# Activity Correlation Finder

### Uses Pandas module to analyze a "Weekly Summary" .csv file from Garmin Connect
### Attempts to answer the question: What training metric had the greatest impact on running speed
- Takes a .csv file output by Garmin Connect Website.
- Filters data such that remaining columns include
  - Time Period (week)
  - Activities (activities)
  - Average Heart Rate (avg_hr)
  - Total Distance (tot_distance)
  - Total Activity Time (tot_time)
  - Average Speed (avg_speed)
- Finds 1st STDEV and 2nd STDEV from the mean avg_speed
- Finds the most-recent week in which either the avg_speed was >= 1st (or 2nd) STDEV
- Gets the 12 weeks of training leading up to that weeks
- Finds Pearson correlations between each category (speed, mileage, hr, etc)
