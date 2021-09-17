import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


df=pd.read_csv("C:/Users/j.elachkar/Desktop/airline_Tweets.csv")
print(df.head())

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.subheader("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.markdown("this application is a streamlit dashboard to analyse the sentiment of Tweets")
st.sidebar.markdown("Show random tweet")

# 1st visualization
random_tweet = st.sidebar.radio("Sentiment",["neutral","positive","negative"])
st.sidebar.markdown(df.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

# 2nd visualization

st.sidebar.markdown("Number of Tweets by sentiment")
select = st.sidebar.selectbox("Visualization type",["Histogram","Pie chart"])
count = df['airline_sentiment'].value_counts()
data_frame = pd.DataFrame({'sentiment':count.index,'values':count.values})
print(count)
print(data_frame)
if st.sidebar.checkbox("check to see"):
    st.markdown("Number of tweets by sentiment")
    if select =="Histogram":
        fig=px.bar(data_frame,x='sentiment',y='values',color='sentiment')
        st.plotly_chart(fig)
    else:
        select=="Pie chart"
        fig1=px.pie(data_frame,names='sentiment',values='values')
        st.plotly_chart(fig1)


# 3rd visualization
st.sidebar.markdown("When and where are users tweeting from?")
hour = st.sidebar.slider("hour",min_value=0,max_value=24)
df['tweet_created']=pd.to_datetime(df['tweet_created'])
modified_data = df[df['tweet_created'].dt.hour==hour]
if st.sidebar.checkbox("Press"):
    st.markdown("Tweets Location based on the time of the day")
    st.markdown("%i tweets between %i:00 and %i:00"% (len(modified_data),hour,(hour+3)%24))
    st.map(modified_data)
    st.write(modified_data)


# 4th visualization
st.sidebar.subheader("Breakdown airline tweets by sentiment")
multi = st.sidebar.multiselect("pick airlines",df['airline'].unique())

if len(multi)>0:
    data=df[df['airline'].isin(multi)]
    fig2=px.histogram(data,x='airline',y='airline_sentiment',histfunc='count',facet_col='airline_sentiment',
                      color='airline_sentiment',labels={'airline_sentiment':'tweets'})
    st.plotly_chart(fig2)

# 5th visualization
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud",['positive','negative','neutral'])

if not st.sidebar.checkbox("close",True,key='3'):
    st.subheader('word cloud for %s sentiment'% (word_sentiment))
    df1= df[df['airline_sentiment']==word_sentiment]
    words= ' '.join(df1['text'])


    processed_words=' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word !='RT'])

    wordcloud=WordCloud(stopwords=STOPWORDS,background_color='white',height=604,width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([]) # to remove x axis data, we don't need it in a word cloud
    plt.yticks([]) # to remove y axis data, we don't need it in a word cloud
    st.pyplot()