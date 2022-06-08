import pandas as pd
from scipy.stats import kendalltau, spearmanr

filename = "Week_copy.csv"
lthr = 180

class ActivityStats:
  def __init__(self,data_frame):
    self.means = {
    'hr':data_frame['avg_hr'].mean().astype(int),
    'dist':round(data_frame['tot_distance'].mean(),2),
    'time':round(data_frame['tot_time'].mean(),2),
    'activities': data_frame['activities'].mean().astype(int),
    'speed': round(data_frame['avg_speed'].mean(),2)
    }
    self.stdevs = {
      'hr':data_frame['avg_hr'].std().astype(int),
      'dist':round(data_frame['tot_distance'].std(),2),
      'time':round(data_frame['tot_time'].std(),2),
      'activities': data_frame['activities'].std().astype(int),
      'speed': round(data_frame['avg_speed'].std(),3)
    }
    self.correls = {
      'Pearson':data_frame.corr(method='pearson'),
      'Kendall':data_frame.corr(method='kendall'),
      'Spearman':data_frame.corr(method='spearman')
    }
  def print_means(self,other):
    this = self.means['speed']
    that = other.means['speed']
    print("Per cent diff = {}%".format((this-that)/this)*100)

def time_to_minutes(time_string):
    minutes = 0
    time_list = time_string.split(":")
    time_list = [int(e) for e in time_list]
    if len(time_list)==3:
        minutes += time_list[0]*60
        minutes += time_list[1]
        minutes += time_list[2]/60
    elif len(time_list) == 2:
        minutes += time_list[0]
        minutes += time_list[1]/60
    return round(minutes,2)

#making a list of missing values to eliminate incomplete rows later
missing_values = ["--"]

#Names we are going to have to change columns to, for easier access later
renames = {"Activities":"activities", "Time Period": "week","Average Heart Rate":"avg_hr","Total Distance":"tot_distance","Total Activity Time":"tot_time","Average Speed":"avg_speed"}

#Read CSV into DataFrame
df = pd.read_csv(filename, delimiter=',',na_values=missing_values)

#Only keep columns we care about
df = df.filter(["Time Period",  "Total Activity Time", "Activities", "Total Distance", "Average Speed","Average Heart Rate"],axis=1)

#Rename columns to make them easier to deal with later
df.rename(columns=renames,inplace=True)

########################################################################
############################### CLEANING ###############################
########################################################################

#Drop last row since that is 'sums' and 'totals'
df.drop(df.tail(1).index,inplace=True)

#get rid of incomplete rows (any row with a column value of "--" defined in missing_values above)
df.dropna(axis=0, how='any',inplace=True)

#Reset index values after dropping rows
df.reset_index(drop=True)

#Change 'activities' to ints
df.activities = df.activities.astype(int)

#Get rid of ' h:mss', change 'tot_time' to minutes (floats, 2 decimal places)
df.tot_time = df.tot_time.str.replace(" h:m:s","")
#--This is a bit clunky, had to make the series a list and apply my homemade function to each element
time_list = df.tot_time.tolist()
for i in range(len(time_list)):
    time_list[i] = time_to_minutes(time_list[i])

#--Then I had to drop the current 'tot_time' and make a new one with the 'time_list' I had just made
df.drop('tot_time', axis=1,inplace=True)
df['tot_time'] = time_list

#Get rid of ' mi' and change tot_distance to floats
df.tot_distance = df.tot_distance.str.replace(" mi","").astype(float)

#Get rid of ' bpm' and change avg_hr to ints
df.avg_hr = df.avg_hr.str.replace(" bpm","").astype(int)

#Get rid of ' mph' and change avg_speed to floats
df.avg_speed = df.avg_speed.str.replace(" mph","").astype(float)

#Create a 'volume' column
#df['volume']=df['avg_hr']*df['tot_time']
df['rel_volume']=(df['tot_time'])/(df['activities'])*(df['avg_hr'])

#===Check it is read in correctly===#
print(df.head(5))
print(df.tail(5))

#create a new object holding OVERALL stats from large dataframe (df)
overall_activity_stats = ActivityStats(df)

##########################################################################################
################################### FILTERING BY STDEV ###################################
##########################################################################################

#1 STDEV above mean
speed_1_sd = round(overall_activity_stats.means['speed'] + (overall_activity_stats.stdevs['speed']*1),2)

#2 STDEV above mean
speed_2_sd = round(overall_activity_stats.means['speed'] + (overall_activity_stats.stdevs['speed']*2),2)

#Make new DataFrame with all rows with speed >= 1 STDEV above mean
filtered_df = df[df['avg_speed']>=speed_1_sd]

#get the index of the most recent row
most_recent_row = filtered_df.index[0]

#Make new DataFrame with the 12 weeks leading up to most recent 'fast' week
review = pd.DataFrame(df.loc[most_recent_row-11:most_recent_row])


#######################################################################################
################################### OBJECT CREATION ###################################
#######################################################################################

#create a new object holding FILTERED stats from filtered_df
filtered_activity_stats = ActivityStats(filtered_df)

#create a new object holding MOST RECENT FAST stats from review
review_activity_stats = ActivityStats(review)

# Show correlations between data points
# Ex. How strong of a correlation is there between average speed and volume? Distance?
print(overall_activity_stats.correls['Pearson'])
print(filtered_activity_stats.correls['Pearson'])
print(review_activity_stats.correls['Pearson'])

