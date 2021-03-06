import pandas as pd
import re
from datetime import datetime
from nltk.corpus import stopwords
from wordcloud import WordCloud
import seaborn as sns
from matplotlib import pyplot as plt

#read data
news = pd.read_csv('news.csv')
news.head()
news.describe()


#filter rows between 2011 and 2019 inclusive
news[['Year']] = news[['Year']].loc[news['Year'].apply(lambda x: (x >= 2011) & (x <= 2019))]
news.shape
list(news.columns.values)

#create 'Date' column
news['Date'] = news['Year'].astype(str) + ' ' + news['Month'] + ' ' + news['Day'].astype(str)
news['Date'] = news['Date'].apply(lambda x: datetime.strptime(x, '%Y %b %d').date())

# introduce dummy variable columns, based on the certain words in an observation 
def check_any(pattern, string):
    string= string.lower()
    if re.search(pattern, string) != None:
        return 1
    else: 
        return 0
def check_any(pattern1, pattern2, string):
    string= string.lower()
    if re.search(pattern1, string) !=None and re.search(pattern2, string) != None:
        return 1
    else: 
        return 0

df['Article_bank_purdue'] = df['Article'].apply(lambda x: check_any('purdue', 'bankruptcy', x))
print(df['Article_bank_purdue'].sum())

for i in ['Header', 'Article']:
    for y in ['opioid', 'purdue', 'bankruptcy']:
        news[i + '_' + y] = news[i].apply(lambda x: check_any(y, x))
        print(news[i + '_' + y].sum())

# use pandas time series 
df['Date'] = pd.to_datetime(df['Date'])
df.Date.dtype
df = df.set_index('Date')
df = df['9/26/2011':'9/14/2019']
df.shape

df = df.drop(['Unnamed: 0'], axis = 1)

# number of articles with certain words for each year
df_grouped = df.groupby(df.index.year).agg({'Article_opioid': ['sum'],'Article_purdue': ['sum'],'Article_bank_purdue': ['sum']})
df_grouped
# correaltion matrix for the number of articles with certain words for each year
df_c= df.groupby(df.index.year).agg({'Article_opioid': ['sum'],'Article_purdue': ['sum'],'Article_bankruptcy': ['sum']})
df_corr = df_corr.corr(method = "pearson")
df_corr


# line chart for the number of articles with certain words for each year
sns.set(rc={'figure.figsize':(11, 4)})
ax = df.\
    groupby(df.index.year).\
    agg({'Article_opioid': ['sum'],'Article_purdue': ['sum'],
         'Article_bank_purdue':['sum']}).\
    plot(marker = 'o', linestyle = '-')
ax.set_ylabel('Number of Articles')
ax.set_title('Number of Articles per Year Containing Certain Words')
ax.legend(labels = ['# of articles with "opioid"', '# of articles with "purdue"',\
                    '# of articles with "bankruptcy"&"purdue"'])
plt.savefig('Trend_words.png', bbox_inches='tight')

# word cloud for articles about opioid crisis
stop = stopwords.words('english')
stop.extend(['one', 'told cnn', 'trump', 'president', 'say', 'said', 'may', 'new', 'according', 'many', 'two', \
            'make', 'made', 'including', 'work', 'need', 'know', 'year', 'still', 'want', 'take', 'going',\
             'state', 'monday', 'first', 'week', 'pr', 'michael', 'jackson', 'donald'])
stop

mask = np.array(Image.open("usa_map.jpg"))
wc = WordCloud(background_color="black", max_words=2000, width=800, height=400, mask = mask)
for_cloud = str(df.loc[df.Article_opioid == 1]['Article'].\
apply(lambda text: " ".join(word for word in text.lower().split() if word not in stop)))
#wc.generate(' '.join(df['Article'].loc[df['Article_opioid'] == 1]))
wc.generate(for_cloud)

#save data
wc.to_file("clou_opioid.png")
df.to_csv('news_final.csv')




