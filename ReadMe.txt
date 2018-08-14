SMARTPHONE REVIEW: A SECOND OPINION FROM TWEETS

When dealing with products of which the quality is difficult to ascertain
prior to purchase, one may expect a greater reliance on secondary cues
that help consumers in their selection process. This application uses 
the raw and genuine data from tweets to estimate and review the quality 
of the smartphone, using sentiment analysis and provides different 
visualizations based on the ratings.


ANALYTICAL FEATURES AVAILABLE AS OUTPUT
=======================================

1. You will be able to visualize the world cloud .
2. Word Frequencies based on ratings. On hovering on the circles, you can see the correspoding
   words.
3. It also contains a play button, to get an animation of word frequencies base on 
   features. You can click on pause button to pause the animation at any time.
4. There is also slider to manually observe the word frequencies based on features. 
5. A Bar Graph depicting the percentage distribution of categorical tweets. You can hove on
   the bars to view the ratings.
6. A Donut Animation plot which shows the average rating in the center and sentiment analysis 
   distribution in the annular ring (As positive, negative, neutral).


INSTALLATION
============

The easiest way to install Bokeh is using the Anaconda Python distribution 
and its included Conda package management system. To install Bokeh and its 
required dependencies, enter the following command at a Bash or Windows command prompt:

conda install bokeh

To install using pip, enter the following command at a Bash or Windows command prompt:

pip install bokeh

Once Bokeh is installed, install the following libraries to help the application run 
by entering the below commands one by one:

pip install pandas
pip install numpy
pip install scipy
pip install nltk
pip install sklearn
pip install python-twitter
pip install pillow
pip install matplotlib
pip install wordcloud

Once all the libraries are installed, open the file keys.py and add your keys from twitter 
at respective positions.

self.consumer_key='YOUR CONSUMER KEY'
self.consumer_secret='YOUR CONSUMER SECRET KEY'
self.access_token_key='YOUR ACCESS TOKEN KEY'
self.access_token_secret='YOUR ACCESS TOKEN SECRET KEY'



RUNNING THE APPLICATION
=======================

From command prompt change the directory to the extracted project directory and enter 
the following command

bokeh serve --show SmartPhoneReview

After executing the above command, the browser opens a new tab with the link 
http://localhost:5006/SmartPhoneReview



INTERACTING WITH APPLICATION
============================

In the browser, enter a smartphone model name in the text box provided and hit Enter.
The application fetches tweets from twitter and uses the model to rate the tweets into 
the categories of Ratings of 1, 2, 3, 4, 5. and displays multiple graph visualizations.

You can choose different features of the smartphone using the dropdown menu and see 
the respective changes in the graph visualizations.

You can also do the same for another smartphone model just by entering a new name in 
the smartphone model name text box.




