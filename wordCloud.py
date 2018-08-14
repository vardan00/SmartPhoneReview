"""
	wordCloud.py - Get twitter data using api

"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def wordCloud(term, tweets):
	"""Generates a world cloud image in the shape of term.
     
	:param term: The term given by the user.
	:param tweets: The list of tweets.
	:returns: nothing
	:rtype: None
	
	"""
	
	# get an image                                                                                                                                        
	base = Image.new("RGBA", (2000, 400), (255,255,255,0))
	
	# make a blank image for the text, initialized to transparent text color                                                                              
	txt = Image.new('RGBA', base.size, (255,255,255,0))
	
	f=open("SmartPhoneReview/static/fonts/BlackHanSans-Regular.ttf", 'rb')
	# get a font                                                                                                                                          
	fnt = ImageFont.truetype(f, 300)
	d = ImageDraw.Draw(txt)
	if len(term) > 10:
		term = term.split()[0]
	d.text((10,60), term, font=fnt, fill=(0,0,0,255))
	out = Image.alpha_composite(base, txt)
	text = " ".join(tweets)
	alice_mask = np.array(out)	
	stopwords = set(STOPWORDS)
	stopwords.add("said")

	wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
	               stopwords=stopwords)
	
	# generate word cloud
	words = text.split()
	unwanted_chars = ".,-_ (and so on)"
	wordfreq = {}
	for raw_word in words:
	    word = raw_word.strip(unwanted_chars)
	    if word not in wordfreq:
	        wordfreq[word] = 0 
	    wordfreq[word] += 1
	wc.generate_from_frequencies(wordfreq)
	
	# store to file
	wc.to_file("SmartPhoneReview/static/images/"+"".join(term)+".png")
