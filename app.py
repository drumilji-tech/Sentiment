import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns



consumerKey = 'f8d1RpUU2itJ4wVtluGcwd8DN'
consumerSecret = '8r0DyL6g5b4Wx9FZbVMgnkJ14OXSMHBaTgD4shkAb0ePWFLLTz'
accessToken = '1287055837416919041-lQj0GPr3ezO3gUBIUa5ERZEdqxX5jz'
accessTokenSecret = 'IBybnzO8ESkApzYAQAU34dNfWOHlC4Il1ysY0Q3YZCCzv'


#Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)















#plt.style.use('fivethirtyeight')










def app():


	st.title("Sentiment Tweet Analyzer 🔥🔥🔥🔥")


	activities=["Sentiment Tweet Analyzer","Contact Me"]

	choice = st.sidebar.selectbox("Select Your Activity",activities)

	

	if choice=="Sentiment Tweet Analyzer":

		st.subheader("Analyze the tweets of any twitter user")

		st.subheader("The Project is used for :")

		
		st.write("1. Generates a Word Cloud")
		st.write("2. Performing Sentiment Analysis and displays it in the form of a Bar Graph")


		raw_text = st.text_area("Enter the exact twitter handle of the Personality (without @)")


		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])


		if st.button("Analyze"):

			
			if Analyzer_choice == "Show Recent Tweets":

				st.success("Searching Tweets")

				
				def Show_Recent_Tweets(raw_text):

					# Extract 100 tweets from the twitter user
					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					
					def get_tweets():

						l=[]
						i=1
						for tweet in posts[:5]:
							l.append(tweet.full_text)
							i= i+1
						return l

					recent_tweets=get_tweets()		
					return recent_tweets

				recent_tweets= Show_Recent_Tweets(raw_text)

				st.write(recent_tweets)



			elif Analyzer_choice=="Generate WordCloud":

				st.success("Generating  Cloud")

				def gen_wordcloud():

					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")


					# Create a dataframe with a column called Tweets
					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
					# word cloud visualization
					allWords = ' '.join([twts for twts in df['Tweets']])
					wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
					plt.imshow(wordCloud, interpolation="bilinear")
					plt.axis('off')
					plt.savefig('WC.jpg')
					img= Image.open("WC.jpg") 
					return img

				img=gen_wordcloud()

				st.image(img)



			else:



				
				def Plot_Analysis():

					st.success("Generating Visuals for Sentiment Analysis")

					


					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


					
					# Create a function to clean the tweets
					def cleanTxt(text):
					 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
					 text = re.sub('#', '', text) # Removing '#' hash tag
					 text = re.sub('RT[\s]+', '', text) # Removing RT
					 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
					 
					 return text


					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
					   return TextBlob(text).sentiment.subjectivity

					# Create a function to get the polarity
					def getPolarity(text):
					   return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)


					def getAnalysis(score):
					  if score < 0:
					    return 'Negative'
					  elif score == 0:
					    return 'Neutral'
					  else:
					    return 'Positive'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))


				st.pyplot(use_container_width=True)

				

	

	else:

		st.subheader("This project was done by Drumil Joshi(https://www.linkedin.com/in/drumil-joshi-00636716a/)")



	st.subheader(' ------------------------A project by : Drumil T Joshi ----------------------')



if __name__ == "__main__":
	app()
