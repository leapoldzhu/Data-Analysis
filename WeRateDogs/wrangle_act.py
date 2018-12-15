#!/usr/bin/env python
# coding: utf-8

# # Wrangle Project

# In[1]:


# Import packages needed
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import tweepy
import json

get_ipython().run_line_magic('matplotlib', 'inline')


# ## Collect data
# ### Object
# #### 1. given twitter data
# 
#   upload
# 
# #### 2. prediction image data
#   
#   download with `requests` from url `https://raw.githubusercontent.com/udacity/new-dand-advanced-china/master/%E6%95%B0%E6%8D%AE%E6%B8%85%E6%B4%97/WeRateDogs%E9%A1%B9%E7%9B%AE/image-predictions.tsv`
#   
# #### 3. additional data from json file
# 
#   since it's difficult to get access to twitter, we use provided txt file.

# ### Log
# #### 1. given twitter data
# 
#   Upload `twitter-archive-enhanced.csv`
# 
# #### 2. prediction image data
# 
#   Use requests to download data from given url

# In[2]:


# use requests to download
url = 'https://raw.githubusercontent.com/udacity/new-dand-advanced-china/master/%E6%95%B0%E6%8D%AE%E6%B8%85%E6%B4%97/WeRateDogs%E9%A1%B9%E7%9B%AE/image-predictions.tsv'
r = requests.get(url)
# save text to Prediction-image-data.csv
file_name = 'image_predictions.tsv'
with open(file_name, 'w') as file:
    file.write(r.text)


# #### 3. additional data from json file
#   Upload `tweet_json.txt`
#   
# ### Read file
# 
# - [Read multi json objects](https://www.jianshu.com/p/b6a02b49845c)

# In[3]:


tweet_info = pd.read_csv('twitter-archive-enhanced.csv')
image_info = pd.read_csv('image_predictions.tsv', sep='\t')
# json.load can't deal with multiple json objects, use dump first
tweet_json_info = []
with open('tweet_json.txt', 'r') as file:
    for line in file.readlines():
        tweet_json_info.append(json.loads(line))


# ### Conclude
# 
# Data stored in `tweet_info`, `image_info`, `tweet_json_info`

# ## Assess
# 
# Dataset: `tweet_info`, `image_info`, `tweet_json_info`
# 
# - Missing data
# - Format
# - Accuracy
# - Consistency
# 
# [Tweet data reference](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html)
# 
# ### 1. tweet_info

# In[4]:


tweet_info.sample(5)


# In[5]:


tweet_info.info()


# In[6]:


tweet_info.source[1]


# In[7]:


# if there are duplicated tweet
tweet_info.tweet_id.duplicated().sum()


# In[8]:


tweet_info.name.value_counts()


# In[9]:


tweet_info[tweet_info.name=='a'].text[2153]


# In[10]:


tweet_info[(tweet_info.pupper!='None') & (tweet_info.doggo!='None')]


# In[11]:


tweet_info[(tweet_info.floofer!='None') & (tweet_info.doggo!='None')]


# In[12]:


tweet_info[(tweet_info.puppo!='None') & (tweet_info.doggo!='None')]


# ### 2. image_info

# In[13]:


image_info.head()


# In[14]:


image_info.info()


# ### 3. tweet_json

# In[15]:


len(tweet_json_info)


# In[16]:


tweet_json_info[4]


# ### Quality
# #### tweet_info
# 
# 1. missing data(need `retweet_count` and `favorite_count`)
# 
# 2. there are some retweeted tweets
# 
# 3. Types
#     
#     - tweet_id is type int64 
# 
#     - in_reply_to_status_id is type float64 
# 
#     - in_reply_to_user_id is type float64 
# 
#     - retweeted_status_id is type float64 
# 
#     - retweeted_status_user_id is type float64 
# 
#     - timestamp is object type
#     
#     - retweeted_status_timestamp is type object 
# 
# 4. timestamp has +0000 at end
# 
# 5. source has tag a, and href link
#     
# 6. dogs has no name displayed as None, which isn't np.nan in pandas
# 
# 7. dogs have name begin with [a-z], like 'a', 'an', 'the', and others, obviously not a dog name.
# 
# 8. breeds of dogs displayed as None
# 
# 9. 12 records have `doggo` and `pupper`, 1 record has `doggo` and `puppo`, and 1 record has `doggo` and `floofer`.
# 
# 10. `retweeted_status_id`, `retweeted_status_user_id` and `retweeted_status_timestamp` (don't need them)
# 
# #### image_info
# 
# 1. tweet_id is type int64
# 
# 2. too many prediction results
# 
# #### tweet_json_info
# 
# 1. many redundant data
#     
# ### Tidy
# 
# #### tweet_info
# 
# 1. last four columns, `doggo` `floofer` `pupper` `puppo` can be integrate into one column `Stage`
# 2. columns `numerator` and `denomitor` can be one column `score`
# 
# #### image_info
# 
# 1. image_info should be a part of tweet_info

# ## Clean

# In[17]:


tweet_info_clean = tweet_info.copy()
image_info_clean = image_info.copy()
tweet_json_info_clean = tweet_json_info.copy()


# ### Retweeted tweets
# 
# ***Define***
# 
# There are some tweets are retweeted, we don't need that parts of data. Find them and delete them.
# 
# ***Code***

# In[18]:


# we could say all retweeted tweets are those retweeted_status_id isn't null
(tweet_info_clean[~tweet_info_clean.text.str.extract(r'(RT @)').isnull()].index != tweet_info_clean[~tweet_info_clean.retweeted_status_id.isnull()].index).sum()


# In[19]:


tweet_info_clean = tweet_info_clean[tweet_info_clean.retweeted_status_id.isnull()]
tweet_info_clean.reset_index(drop=True, inplace=True)
tweet_info_clean


# ***Test***

# In[20]:


tweet_info_clean.tail()


# In[21]:


tweet_info_clean.info()


# ### Redundant columns
# 
# ***Define***
# 
# Delete `retweeted_status_id`, `retweeted_status_user_id` and `retweeted_status_timestamp`
# 
# ***Code***

# In[22]:


tweet_info_clean.drop(['retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp', 'in_reply_to_status_id', 'in_reply_to_user_id'], axis=1, inplace=True)


# ***Test***

# In[23]:


tweet_info_clean.head()


# In[24]:


tweet_info_clean.columns


# ### Missing data
# 
# ***Define***
# 
# extract `followers_count`, `retweet_count` and `favorite_count` data with `tweet_id` in `tweet_json_info`, then join with `tweet_info`
# 
# **Note**:
# 
# Maybe this problem can be seen as two problems: 1. Establish a dataframe with three columns from json file; 2. Merge it with tweet_info_clean dataframe, but I'll record it as one problem here.
# 
# ***Code***

# In[25]:


# extract `retweet_count` , `favorite_count` and `tweet_id`
attribute = ['id', 'retweet_count', 'favorite_count', 'followers_count']
# construct a list to store json dictionary
data_dict = []
for info in tweet_json_info:
    data_dict.append({})
    for attr in attribute:
        if attr=='followers_count':
            data_dict[-1][attr] = info['user'][attr]
        else:
            data_dict[-1][attr] = info[attr]
    
# join two dataframes together
pdData = pd.DataFrame.from_dict(data_dict)
pdData.rename(columns={'id':'tweet_id'}, inplace=True)
tweet_info_clean = tweet_info_clean.merge(pdData, on='tweet_id', how='left')
# if we fill NaN with 0, it would probably affects our further analysis
# but it also have some 0 in these records, so we decide to fill them with 0.
tweet_info_clean.favorite_count.fillna(0, inplace=True)
tweet_info_clean.retweet_count.fillna(0, inplace=True)
# this part is drop NaN rows
#tweet_info_clean = tweet_info_clean[~((tweet_info_clean.favorite_count.isnull()) | (tweet_info_clean.retweet_count.isnull()))]
#tweet_info_clean.reset_index(drop=True, inplace=True)


# ***Test***

# In[26]:


tweet_info_clean.favorite_count.value_counts()


# In[27]:


tweet_info_clean.info()


# In[28]:


tweet_info_clean.tail()


# ### More than one stage
# 
# ***Define***
# 
# For merge operation can be done exactly, solve this problem first
# 
# Check text content, determine exact stage of dogs.
# 
# - If there are two dogs, copy other information and make a new record.
# 
# ***Code***

# In[29]:


pupper_doggo_list = []
for index, row in tweet_info_clean[(tweet_info_clean.pupper!='None') & (tweet_info_clean.doggo!='None')].iterrows():
    print(row.text)
    pupper_doggo_list.append(index)
    
print('\n', tweet_info_clean[(tweet_info_clean.floofer!='None') & (tweet_info_clean.doggo!='None')].text[172])

print('\n', tweet_info_clean[(tweet_info_clean.puppo!='None') & (tweet_info_clean.doggo!='None')].text[165])


# In[30]:


# -8 name; -7 doggo; -6 floofer; -5 pupper; -4 puppo
# set one doggo record and one pupper record
def doggo_and_pupper(Data, index, name = None):
    '''
    If one record have doggo and pupper stage at same time, split it into two records.
    
    Input:
        Data - Data needed to be operated
        index - index of record
        name - If two dogs have name, put them in a list, doggo's name in first place. Default: None
        
    Output:
        Data - Data after operated
    '''
    Data.iloc[index, -5] = 'None'
    if name:
        Data.iloc[index, -8] = name[0]
    Data = Data.append(Data.iloc[index].copy())
    if name:
        Data.iloc[index, -8] = name[1]
    Data.iloc[index, -5] = 'pupper'
    Data.iloc[index, -7] = 'None'
    
    return Data

# change records
# This is Dido. She's playing the lead role in "Pupper Stops to Catch Snow Before Resuming Shadow Box with Dried Apple." 13/10 (IG: didodoggo) https://t.co/m7isZrOBX7
# this is a pupper
tweet_info_clean.iloc[pupper_doggo_list[0], -7] = 'None'
# Here we have Burke (pupper) and Dexter (doggo). Pupper wants to be exactly like doggo. Both 12/10 would pet at same time https://t.co/ANBpEYHaho
# two dogs
tweet_info_clean = doggo_and_pupper(tweet_info_clean, pupper_doggo_list[1], name = ['Dexter', 'Burke'])
# Like doggo, like pupper version 2. Both 11/10 https://t.co/9IxWAXFqze
# two dogs
tweet_info_clean = doggo_and_pupper(tweet_info_clean, pupper_doggo_list[2])
# This is Bones. He's being haunted by another doggo of roughly the same size. 12/10 deep breaths pupper everything's fine https://t.co/55Dqe0SJNj
# this is a pupper
tweet_info_clean.iloc[pupper_doggo_list[3], -7] = 'None'
# This is Pinot. He's a sophisticated doggo. You can tell by the hat. Also pointier than your average pupper. Still 10/10 would pet cautiously https://t.co/f2wmLZTPHd
# this is a doggo
tweet_info_clean.iloc[pupper_doggo_list[4], -5] = 'None'
# Pupper butt 1, Doggo 0. Both 12/10 https://t.co/WQvcPEpH2u
# two dogs
tweet_info_clean = doggo_and_pupper(tweet_info_clean, pupper_doggo_list[5])
# Meet Maggie &amp; Lila. Maggie is the doggo, Lila is the pupper. They are sisters. Both 12/10 would pet at the same time https://t.co/MYwR4DQKll
# two dogs
tweet_info_clean = doggo_and_pupper(tweet_info_clean, pupper_doggo_list[6], name = ['Maggie', 'Lila'])
# Please stop sending it pictures that don't even have a doggo or pupper in them. Churlish af. 5/10 neat couch tho https://t.co/u2c9c7qSg8
# this is a doggo
tweet_info_clean.iloc[pupper_doggo_list[7], -5] = 'None'
# This is just downright precious af. 12/10 for both pupper and doggo https://t.co/o5J479bZUC
# two dogs
tweet_info_clean = doggo_and_pupper(tweet_info_clean, pupper_doggo_list[8])
# Like father (doggo), like son (pupper). Both 12/10 https://t.co/pG2inLaOda
# two dogs
tweet_info_clean = doggo_and_pupper(tweet_info_clean, pupper_doggo_list[9])

# At first I thought this was a shy doggo, but it's actually a Rare Canadian Floofer Owl. Amateurs would confuse the two. 11/10 only send dogs https://t.co/TXdT3tmuYk
# this is a doggo
tweet_info_clean.iloc[172, -6] = 'None'

# Here's a puppo participating in the #ScienceMarch. Cleverly disguising her own doggo agenda. 13/10 would keep the planet habitable for https://t.co/cMhq16isel
# this is a puppo
tweet_info_clean.iloc[165, -7] = 'None'
tweet_info_clean = tweet_info_clean.reset_index(drop=True)


# ***Test***

# In[31]:


tweet_info_clean[(tweet_info_clean.pupper!='None') & (tweet_info_clean.doggo!='None')]


# In[32]:


tweet_info_clean[(tweet_info_clean.floofer!='None') & (tweet_info_clean.doggo!='None')]


# In[33]:


tweet_info_clean[(tweet_info_clean.puppo!='None') & (tweet_info_clean.doggo!='None')]


# ### Image_info prediction
# 
# ***Define***
# 
# There are too many results, choose the most confident one(check p1_conf, p2_conf and p3_conf, find max one) as final result
# 
# ***Code***

# In[34]:


image_info_clean.tail()


# In[35]:


# find the most confident answer and corresponding data
image_info_clean.p1_conf.values
conf_list = np.concatenate(([image_info_clean.p1_conf.values], [image_info_clean.p2_conf.values], [image_info_clean.p3_conf.values]), axis=0)
(conf_list.argmax(axis=0)==0).sum
image_info_clean = image_info_clean[['tweet_id', 'jpg_url', 'img_num', 'p1', 'p1_conf', 'p1_dog']]


# ***Test***

# In[36]:


image_info_clean.tail()


# ### Tidiness
# 
# **Note**
# 
# When needed, I'll split the data after all quality issues are solved.
# 
# #### Unit columns
# 
# ***Define***
# 
# Unite columns `doggo`, `floofer`, `pupper` and `puppo` into one column `Stage`
# 
# ***Code***

# In[37]:


tweet_info_clean.columns


# In[38]:


# one loop of original index
loop_len = tweet_info_clean.index.max() + 1

# melt four columns into one colun, `Stage`
#df_merge = tweet_info_clean.melt(id_vars=['index', 'tweet_id', 'in_reply_to_status_id', 'in_reply_to_user_id',
#       'timestamp', 'source', 'text', 'expanded_urls', 'rating_numerator',
#       'rating_denominator', 'name', 'favorite_count', 'retweet_count'], value_name='Stage')
df_merge = tweet_info_clean.melt(id_vars=['tweet_id', 'timestamp', 'source', 'text', 'expanded_urls',
       'rating_numerator', 'rating_denominator', 'name', 'favorite_count', 'followers_count',
       'retweet_count'], value_name='Stage')

# clean df_merge, delete redundant records
index_list=[]
for ind in range(loop_len):
    # check which value is not null, `doggo`, `floofer`, `pupper` or `puppo`
    if df_merge.Stage[ind]!='None':
        index_list.append(ind)
    elif df_merge.Stage[ind+loop_len]!='None':
        index_list.append(ind+loop_len)
    elif df_merge.Stage[ind+loop_len*2]!='None':
        index_list.append(ind+loop_len*2)
    elif df_merge.Stage[ind+loop_len*3]!='None':
        index_list.append(ind+loop_len*3)
    else:
        index_list.append(ind)
        
tweet_info_clean = df_merge.iloc[index_list].drop('variable', axis=1)
# set None in Stage to np.nan
tweet_info_clean.Stage = tweet_info_clean.Stage.replace('None', np.nan)


# ***Test***

# In[39]:


tweet_info_clean.info()


# In[40]:


tweet_info_clean.Stage.value_counts()


# In[41]:


df_merge.Stage.value_counts()


# #### Calculate numerator/denominator
# 
# ***Define***
# 
# Calculate result of numerator/deominator, store it in the new column `score`, then drop columns `rating_numerator` and `rating_denominator`
# 
# ***Code***

# In[42]:


tweet_info_clean['score'] = tweet_info_clean.rating_numerator/tweet_info_clean.rating_denominator
tweet_info_clean = tweet_info_clean.drop(['rating_numerator', 'rating_denominator'], axis=1)
# since they all under same underline, 10 points, which means we could also use rating_numerator directly


# ***Test***

# In[43]:


tweet_info_clean.tail()


# #### image_info integrate
# 
# ***Define***
# 
# Integrate image_info into tweet_info
# 
# ***Code***

# In[44]:


tweet_info_clean = tweet_info_clean.merge(image_info_clean, how='left')


# ***Test***

# In[45]:


tweet_info_clean.info()


# ### Timestamp format
# 
# ***Define***
# 
# Extract year, month, day in orginal string, prepare for transform in next step
# 
# ***Code***

# In[46]:


tweet_info_clean.timestamp = tweet_info_clean.timestamp.str.extract(r'(.*)[\s]\+\d{4}', expand=True)


# ***Test***

# In[47]:


tweet_info_clean.timestamp


# ### Wrong types
# 
# ***Define***
# 
# - change tweet_id type to string
# 
# - change in_reply_to_status_id to type string (skip this step, since we have dropped this column)
# 
# - change in_reply_to_user_id to type string (skip this step, since we have dropped this column)
# 
# - change retweeted_status_id to type string (skip this step, since we have dropped this column)
# 
# - change retweeted_status_user_id to type string (skip this step, since we have dropped this column)
# 
# - change timestamp to object datetime
# 
# - change retweeted_status_timestamp to type datetime (skip this step, since we have dropped this column)
# 
# - chnge img_num to type string
# 
# ***Code***

# In[48]:


# change 5 columns from int64 to string
tweet_info_clean.tweet_id = tweet_info_clean['tweet_id'].apply(str)
tweet_info_clean.img_num = tweet_info_clean.img_num.apply(str)
# change two columns from string to datetime
tweet_info_clean.timestamp = pd.to_datetime(tweet_info_clean.timestamp, format='%Y-%m-%d %H:%M:%S')


# ***Test***

# In[49]:


tweet_info_clean.info()


# ### Source link tag < a >
# ***Define***
# 
# Use extract to find text between tag < a >
# 
# ***Code***

# In[50]:


tweet_info_clean.source = tweet_info_clean.source.str.extract(r'<a.*>(.*)</a>', expand=True)


# ***Test***

# In[51]:


tweet_info_clean.source.str.contains('</a>').sum()


# In[52]:


tweet_info_clean.source.str.contains('<a').sum()


# In[53]:


tweet_info_clean.source.sample(5)


# ### Name column
# 
# ***Define***
# 
# - Change None in name column to NaN
# 
# - Change a, an and the to NaN
# 
# - Also set other columns where NaN to np.NaN
# 
# ***Code***

# In[54]:


# set all words start with [a-z] as NaN
tweet_info_clean.name = tweet_info_clean.name.replace(tweet_info_clean.name.str.extract(r'(^[a-z]+$)'), np.nan)
# set None to NaN
tweet_info_clean.name = tweet_info_clean.name.replace('None', np.nan)
# other columns


# ***Test***

# In[55]:


tweet_info_clean.info()


# In[56]:


tweet_info_clean.name.value_counts()


# ### Split the dataframe
# 
# ***Define***
# 
# Use this operation if analysis need those data splited.
# 
# ***Code***
# 
# Blank
# 
# ***Test***
# 
# Blank

# ## Store
# 
# For now, we have one dataframe `tweet_info_clean` maybe used, so we store it into `twitter_archive_master.csv`

# In[57]:


tweet_info_clean.to_csv('twitter_archive_master.csv', index=False)


# ## Analysis
# 
# 1. Which stage of dogs is most tweeted?
# 
# 2. Is there any relation between retweet_count and favorite_count?
# 
# 3. Is there any relation between time and favorite_counts?
# 
# 4. How many source of tweets? What platform is most popular?
# 
# 5. Which stage get most highest score?
# 
# 6. Will follower become more as time past?
# 
# ### Read data

# In[58]:


df = pd.read_csv('twitter_archive_master.csv')


# ### Q1. Which stage of dogs is most tweeted?

# In[59]:


df.Stage.value_counts()


# ***Conclude***
# 
# They tweeted pupper 232 times, which is most often.

# ### Q2. Is there any relation betweet retweet_count and favorite_count?

# In[60]:


# sort favorite_count and corresponding retweet_count ascending
favorite_counts = df.favorite_count.sort_values()
retweet_counts = df.loc[favorite_counts.index].retweet_count
X = favorite_counts.values
Y = retweet_counts.values

plt.scatter(X, Y)
plt.title('Favorite_counts and retweet_counts')
plt.xlabel('favorite_count')
plt.ylabel('retweet_count')


# ***Conclude***
# 
# From plot above, we can see favorite_count have a positive correlation with retweet_count. 
# 
# Also, retweet_count largely smaller than favorite_count, since it's more bothering to make a retweet than press like button. With this point, we could use retweet_count as a more rigid source to evaluate how people like these tweets.

# ### Q3. Is there any relation between time and favorite_counts

# In[61]:


# sort favorite_count and corresponding retweet_count ascending
time_ = df.timestamp.sort_values()
favorite_counts = df.loc[time_.index].favorite_count
X = time_.values
Y = favorite_counts.values

plt.scatter(X, Y)
plt.title('time and favorite_counts')
plt.xlabel('time')
plt.ylabel('favorite_count')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False)


# We also curious will time the tweet posted affect favorite count. Next, we'll split time into four periods:
# 
# - 23:00:00 - 8:00:00
# 
# - 8:00:00 - 12:00:00
# 
# - 12:00:00 - 18:00:00
# 
# - 18:00:00 - 23:00:00

# In[62]:


df_time_favorite = df[['favorite_count']].set_index(pd.DatetimeIndex(df['timestamp']))
# split time into four periods
df_night = df_time_favorite.between_time('23:00:00', '6:00:00')
df_morning = df_time_favorite.between_time('6:00:00', '13:00:00')
df_afternoon = df_time_favorite.between_time('13:00:00', '18:00:00')
df_evening = df_time_favorite.between_time('18:00:00', '23:00:00')
# plot
Y = [df_night.mean(), df_morning.mean(), df_afternoon.mean(), df_evening.mean()]
plt.plot(Y)
plt.title('time and favourite_counts')
plt.ylabel('favourite_count')
plt.xticks(np.arange(4), ('23:00:00 - 6:00:00', '6:00:00 - 13:00:00', '13:00:00 - 18:00:00', '18:00:00 - 23:00:00'), rotation=20)
plt.xlabel('time')


# ***Conclude***
# 
# Basically, there's a positive correlation betweet these two variables, which is not very rigid. 
# 
# We could also observe there's some points where much more favorite_count than expected, and at any time, there are tweets not very popular.
# 
# In next plot, we could observe that tweets posted in day get more favorite than those tweeted in night.

# ### Q4. How many source of tweets?

# In[63]:


df.source.value_counts()


# ***Conclude***
# 
# Of course, we could do this by observation.
# 
# iPhone is most used platform, which is not surprised, then we have three other platforms, both are far less used than iPhone.

# ### Q5. Which stage of dogs get most highest score?

# In[64]:


df.groupby('Stage').score.describe()


# ***Conclude***
# 
# From table above, puppo is a little popular than other three stage of dogs. It has largest mean and little std, from it's qartile, we can further confirm the conclusion.
# 
# **Note**
# 
# I wonder if we could extract some example from doggo and pupper, then use hypothetical test to confirm it statistically.

# ### Q6. Will follower become more as time past?

# In[65]:


# sort favorite_count and corresponding retweet_count ascending
time_ = df.timestamp.sort_values()
followers_counts = df.loc[time_.index].followers_count
X = time_.values
Y = followers_counts.values

plt.plot(X, Y)
plt.title('time and favorite_counts')
plt.xlabel('time')
plt.ylabel('followers_count')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False)


# ***Conclude***
# 
# So, we could tell from the plot that we don't always have more followers with time past, there are some peaks from time to time.
# 
# At the same time, the follower number fluctuate around 3,768,950.

# In[ ]:




