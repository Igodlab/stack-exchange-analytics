# data_utils.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from datetime import datetime, timedelta

import os

def convert_datetime(strdate, now=False):
    if now == True:
        return datetime.now()
    elif ':' in strdate:
        return datetime.strptime(strdate, "%Y-%m-%d %H:%M:%S")
    else:
        return datetime.strptime(strdate+" 00:00:00", "%Y-%m-%d %H:%M:%S")


# create pandas data frame
def to_df(X):
    k = list(X.keys())
    k0 = k[0]
    df = pd.DataFrame(X[k0], index=[0])
    for ni, ki in enumerate(k[1:]):
        df2 = df.append(pd.DataFrame(X[ki], index=[ni+1]))
        df = df2.copy()
    return df

# Find data by UserId
def findByUserId(userId, users_df):
    return users_df[users_df["Id"] == userId]


# answer ratio
def answer_ratio(df_Post):
    r"""
    Returns the answer ratio for the whole Stack Exchange site based on 

    .. math:: r_{ans} = 1 - \frac{q_{noAns}}{q_{total}}

    Requires a Post.csv loaded dataframe as input.

    Differentiation of type of post is found in:
    https://data.stackexchange.com/stackoverflow/query/36599/show-all-types
    
    and also in the Stack Exchange data dump scheema: 
    https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede

    Parameters
    ----------
    df_Post : pd.DataFrame
              Post.csv loaded data frame.

    Returns
    -------
    ans_ratio : float
                Ratio of 
    """

        
    Q_total = df_Post[df_Post["PostTypeId"] == 1].shape[0]
    Q_no_answered = df_Post[df_Post["AnswerCount"] == 0].shape[0]
    ans_ratio = 1 - Q_no_answered / Q_total
    return ans_ratio

# ------------------------------------------------------------------
# CSE Data Dump
# ------------------------------------------------------------------

# convert to datetime 
def to_datetime(X):
    kk = X.keys()
    date_column_in_table = ["Date", "CreationDate", "LastAccessDate", "CreationDate", "CreationDate", np.nan, "CreationDate", "CreationDate"]
    dateCol_list = [i for i in kk if i in date_column_in_table]
    dateCol = dateCol_list[0]
    X[dateCol] = pd.to_datetime(X[dateCol])

    return X


# load xml
def load_xml(fname, fpath=os.path.join("..", "data"), tables=["Badges", "Comments", "PostHistory", "PostLinks", "Posts", "Tags", "Users", "Votes"], convertToDatetime=True):
    r"""
    Loads data from .xml extension. 

    Parameters
    ----------
    fname : str
            Name of the Stack Exchange platform to load. The name 
            of the 7z file is the same (excluding the extensions) 
            as the directory inside the default argument for fpath. 
            This is a convention for accessing data.
    fpath : str, path, optional
            Path of the data directory that contains the all 
            subdirectories for Stack Exchange platforms.
            
    Returns : df
    """
    flocation = os.path.join(fpath, fname)

    data = {}
    print("\n\nLoading *.xml files for '%s' Stack Exchange:\n" % fname)
    for tab in tables:
        fname_i = os.path.join(flocation, tab + ".xml")
        dataRead = pd.read_xml(fname_i)
        if (convertToDatetime == True) & (tab != "Tags"):
            data[tab] = to_datetime(dataRead)
        else:
            data[tab] = dataRead.copy()
        print(tab + ".xml" + " - shape: ", data[tab].shape)

    return data

def load_csv(fname, fpath=os.path.join("..", "data"), tables=["Badges", "Comments", "PostHistory", "PostLinks", "Posts", "Tags", "Users", "Votes"], convertToDatetime=True):
    r"""
    Loads data from .csv extension. 

    Parameters
    ----------
    fname : str
            Name of the Stack Exchange platform to load. The name 
            of the 7z file is the same (excluding the extensions) 
            as the directory inside the default argument for fpath. 
            This is a convention for accessing data.
    fpath : str, path, optional
            Path of the data directory that contains the all 
            subdirectories for Stack Exchange platforms.
            
    Returns : df
    """
    flocation = os.path.join(fpath, fname)

    data = {}
    print("\n\nLoading *.csv files for '%s' Stack Exchange:\n" % fname)
    for tab in tables:
        fname_i = os.path.join(flocation, tab + ".csv")
        dataRead = pd.read_csv(fname_i)
        if (convertToDatetime == True) & (tab != "Tags"):
            data[tab] = to_datetime(dataRead)
        else:
            data[tab] = dataRead.copy()
        print(tab + ".csv" + " - shape: ", data[tab].shape)

    return data

    
# truncate from / to date
def dateRange(X, fromDate=None, toDate=None, dt=timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)):
    kk = X.keys()
    date_column_in_table = ["Date", "CreationDate", "CreationDate", "CreationDate", "CreationDate", np.nan, "LastAccessDate", "CreationDate"]
    dateCol_list = [i for i in kk if i in date_column_in_table]
    assert len(dateCol_list) >= 1, "Table must have a date column."
    dateCol = dateCol_list[0]
    tables = ["Badges", "Comments", "PostHistory", "PostLinks", "Posts", "Tags", "Users", "Votes"]
    #dateRef = dict(zip(tables, date_column_in_table))

    if (fromDate != None) & (toDate != None):
        fromDateDT = pd.to_datetime(fromDate)
        toDateDT = pd.to_datetime(toDate)
        df = X[(X[dateCol] >= fromDateDT + dt) & (X[dateCol] <= toDateDT + dt + timedelta(days=1))]
    elif (fromDate == None) & (toDate != None):
        toDateDT = pd.to_datetime(toDate)
        df = X[X[dateCol] <= toDateDT + timedelta(days=1) + dt]
    elif (fromDate != None) & (toDate == None):
        fromDateDT = pd.to_datetime(fromDate)
        df = X[(X[dateCol] >= fromDateDT) & (X[dateCol] <= fromDateDT + dt + timedelta(days=1))]
    else:
        df = X.copy()

    return df

# Posts.csv

def questionsPerDay(df_Post, fromDate=None, toDate=None, dt=timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)):
    cc = "PostTypeId"
    qq = 1 # questions: "PostTypeId" == 1
    aa = 2 # answers:   "PostTypeId" == 2
    
    Xchop = dateRange(df_Post, fromDate=fromDate, toDate=toDate, dt=dt)
    Xall  = dateRange(df_Post, fromDate=None, toDate=toDate, dt=dt)

    date  = fromDate
    qs    = Xchop[Xchop[cc] == 1]   # questions per `dt`
    ans   = Xchop[(Xchop[cc] == 2)] # answers per `dt`
    accep = Xchop[(Xchop[cc] == 1) & (~Xchop["AcceptedAnswerId"].isnull())]

    allQs    = Xall[Xall[cc] == 1] # questions up to `toDate`
    allAns   = Xall[Xall[cc] == 2] # answers up to `toDate`
    allNoAns = Xall[(Xall["AnswerCount"] == 0) & (Xall[cc] == 1)]

    return [date]+list(map(lambda xi: xi.shape[0], [qs, ans, accep, allQs, allAns, allNoAns])) 
    

def questionsAnalytics(df_Post, freq=timedelta(days=0)):
    date  = []
    qs    = []
    ans   = []
    accep = []

    allQs    = []
    allAns   = []
    allNoAns = []

    t0 = df_Post["CreationDate"][df_Post.index[0]]
    tf = df_Post["CreationDate"][df_Post.index[-1]]

    while t0 <= tf:
        date_i, q_i, a_i, accepted_i, allQs_i, allAns_i, allNoAns_i = questionsPerDay(df_Post, fromDate=t0, toDate=t0+freq)
        
        date.append(date_i)
        qs.append(q_i)
        ans.append(a_i)
        accep.append(accepted_i)

        allQs.append(allQs_i)
        allAns.append(allAns_i)
        allNoAns.append(allNoAns_i)
        t0 = t0 + freq

    df = pd.DataFrame({"Date": date, 
                       "QuestionsDay": qs, 
                       "AnswersDay": ans, 
                       "AcceptedAnsDay": accep, 
                       "AllQuestions": allQs,
                       "AllAnwers": allAns,
                       "AllNoAnwers": allNoAns
                       })
    df["QuestionsDay"]   = (df["QuestionsDay"] / freq.days).astype(int)
    df["AnswersDay"]     = (df["AnswersDay"] / freq.days).astype(int)
    df["AcceptedAnsDay"] = (df["AcceptedAnsDay"] / freq.days).astype(int)

    df["PercQsAns"] = 1 - df["AllNoAnwers"] / df["AllQuestions"]
    return df

def list_tags(df_Post):
    r"""
    Extracts all tags for one row of the `Tags` column in the`Posts.csv` 
    dataset.
    The input data comes as a continuous string with all tags sandwiched 
    between brakets, like this: "<tag1><tag2>...<tagN>".
    
    This function returns a list where all elements are tags.
    
    Parameters
    ----------
    df_Post : str
        tags for a particular Stack Exchange post.
        
    Return type: list
    """
    if type(df_Post) != str:
        return np.nan
    else:
        Xtrim = df_Post[1:-1]
        return Xtrim.split("><")
    
def unique_tags(x, return_counts=True):
    r"""
    Get unique tags and frequency counts for list of list of tags.
    The input of the funciton `list_tags` applied to all rows of 
    the `Tags` column in `Posts.csv` dataset is a list of lists.
    
    Parameters
    ----------
    x             : list
                    List or list of lists containing tags.
    return_counts : Bool
                    {default = True}.
                    
    Return type: tuple
                 (np.array, np.array)
    """
    xConcat = []
    for xi in x:
        if type(xi) != list:
            xConcat.append(xi)
        else:
            aux = []
            for j in range(len(xi)):
                aux.append(xi[j])
            xConcat = xConcat + aux

    if return_counts == True:
        return np.unique(xConcat, return_counts=True)
    else:
        return xConcat

# barplot for tags in `Posts.csv`
def postsTagsBarplot(data, startDate, endDate, col="Posts", nTags=None):
    df = data[col]
    truncateDate = df[(df["CreationDate"] >= startDate) & (df["CreationDate"] < endDate)]

    listTags = truncateDate["Tags"].apply(list_tags)

    # concatenate all tags among all rows
    uniTags = unique_tags(listTags)
    uniTags_noNa = unique_tags(listTags.dropna())

    # create dataframe for uniTags
    postsTags = pd.DataFrame(uniTags).T
    postsTags = postsTags.rename(columns={1: "Count", 0: "Tag"}).sort_values(by="Count", ascending=False)
    
    postsTags_noNa = pd.DataFrame(uniTags_noNa).T
    postsTags_noNa = postsTags_noNa.rename(columns={1: "Count", 0: "Tag"}).sort_values(by="Count", ascending=False)


    # plot tags
    fig1, axes = plt.subplots(figsize=(14,6))
    sns.barplot(y="Tag", x="Count", data=postsTags[postsTags["Count"] >= 0.01*max(postsTags["Count"])])
    #plt.xticks(rotation=60)
    #plt.show()

    # plot tags no Na
    postTagsFiler = postsTags_noNa[postsTags_noNa["Count"] >= 0.1*max(postsTags_noNa["Count"])]
    fig2, axes = plt.subplots(figsize=(14,6))
    if nTags == None:
        sns.barplot(y="Tag", x="Count", data=postTagsFiler)
    else:
        sns.barplot(y="Tag", x="Count", data=postTagsFiler[:nTags])
    #plt.xticks(rotation=60)
    plt.title("Tag ranking")
    #plt.show()

    return (fig1, fig2)

def postsTagsPieplot(data, startDate, endDate, col="Posts", nTags=None):
    df = data[col]
    truncateDate = df[(df["CreationDate"] >= startDate) & (df["CreationDate"] < endDate)]

    listTags = truncateDate["Tags"].apply(list_tags)

    # concatenate all tags among all rows
    uniTags = unique_tags(listTags)
    uniTags_noNa = unique_tags(listTags.dropna())

    # create dataframe for uniTags
    postsTags = pd.DataFrame(uniTags).T
    postsTags = postsTags.rename(columns={1: "Count", 0: "Tag"}).sort_values(by="Count", ascending=False)
    postsTags.reset_index(inplace=True, drop=True)

    postsTags_noNa = pd.DataFrame(uniTags_noNa).T
    postsTags_noNa = postsTags_noNa.rename(columns={1: "Count", 0: "Tag"}).sort_values(by="Count", ascending=False)
    postsTags_noNa.reset_index(inplace=True, drop=True)

    # plot tags no Na
    postTagsFilter = postsTags_noNa.copy()
    if nTags != None:
        postTagsFilter.loc[range(nTags,postTagsFilter.shape[0]), "Tag"] = "other"
    else:
        postTagsFilter.loc[range(postTagsFilter.shape[0]), "Tag"] = "other"

    fig = px.pie(postTagsFilter, values='Count', names='Tag',
                 title='Most discussed tags in CSE')
                # hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'})
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

