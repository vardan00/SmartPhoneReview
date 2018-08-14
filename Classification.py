"""
////////////////////////////////////////////////////////////////////////////////////////////
// Classification.py - This file manipulates the tweets data into      					  //
//                     a format suitable to  generate plots.           					  //
////////////////////////////////////////////////////////////////////////////////////////////
"""

import pickle, os, twitterFetchTweets, gapminderplot, re
import pandas as pd
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import scipy as sc
import numpy as np



def generateGapMinderPlotData(tweets, result, featureLevelAnalysis,modelName):
	"""This function converts the input into a format, that is suittable to render gapMinder Plot.
	
	:param tweets: list of tweets.
	:param result: a dummy variable needs to be removed.
	:param featureLevelAnalysis: The dictionary to store some intermediate results.
	:returns: data suitable to render a gapminder plot.
	:rtype: dictionary.
	
	"""
	
	print("")

	emoticons_str = r"""
    	(?:
    	    [:=;] # Eyes
    	    [oO\-]? # Nose (optional)
    	    [D\)\]\(\]/\\OpP] # Mouth
    	)"""
	
	removeRegex = [emoticons_str, r'http\S+']
	tokens_re = re.compile(r'('+'|'.join(removeRegex)+')', re.VERBOSE | re.IGNORECASE)
	splitting = re.compile(r'(?<![@])\b\w+\b')

	stop_words = stopwords.words("english")
	nresult = []
	word_freq={}
	for t in tweets:
		result = re.sub(tokens_re, "", t)
		result = re.sub('^RT ', "", result)
		result = splitting.findall(result)

		for r in result:
			if r not in stop_words and r not in modelName and r!="camera" and r!="battery" and len(r)>3:
				nresult.append(r)
	
	nresult = remove_values_from_list(nresult,modelName)
	featureLevelAnalysis["words"].extend(nresult)
	df = createDataFrameGapMinder(nresult,modelName)
	return df

def remove_values_from_list(the_list,modelName):
   return [value for value in the_list if value not in modelName and value!="camera" and value!="battery" and len(value)>3]

def createDataFrameGapMinder(nresult,modelName):
	"""A helper function to generate data suitable to render the gapminder plot.
	
	:param nresult: a list of words.
	:returns: returns the formatted data.
	:rtype: dictionary.
	
	"""
	linearsvc = pickle.load(open('SmartPhoneReview/data/LinearSVC', 'rb'))
	tfidf = pickle.load(open('SmartPhoneReview/data/tfidf', 'rb'))
	vals = modelName.split()
	nresult = remove_values_from_list(nresult,modelName)
	df = pd.DataFrame()
	result = FreqDist(nresult).most_common(50)
	t=[x[0] for x in result if x[0]!="camera" and x[0]!="battery" and x[0] not in modelName and len(x[0])>3]
	df["word"] = t
	
	df["freq"] = [x[1] for x in result if x[0]!="camera" and x[0]!="battery" and x[0] not in modelName and len(x[0])>3]
	mean = sum(df["freq"])/len(df["freq"])
	df["freq"] = [val if val<mean else mean for val in df["freq"]]
	df["sentiment"] = list ( map( str, list(linearsvc.predict(tfidf.transform(t))) ))
	size = len(df["word"])
	low = 0
	high = 10
	df["xval"] = np.multiply(sc.rand(size), sc.random.random_integers(low, high, size))
	df["yval"] = np.multiply(sc.rand(size), sc.random.random_integers(low, high, size))
	df = df.to_dict('series')
	return df

def fetchPreprocess(term, featureLevelAnalysis, f,modelName):
	"""A helper function to get the tweets and store and generate the data to render the plots.
	
	:param term: the model name.
	:param featureLevelAnalysis: A dictionary to store some results. 
	:param f: A specification like camera, battery etc.
	:returns: Does not return anything
	:rtype: None
	
	"""
	linearsvc = pickle.load(open('SmartPhoneReview/data/LinearSVC', 'rb'))
	tfidf = pickle.load(open('SmartPhoneReview/data/tfidf', 'rb'))
	overallRatings = featureLevelAnalysis["overallRatings"]
	featureLevelAnalysis["words"] = []
	tweets = []
	result = []
	tweets = list(set(twitterFetchTweets.searchSmartPhone(term)))
	result = list(linearsvc.predict(tfidf.transform(tweets)))

	featureLevelAnalysis["gapminderplot"].append(generateGapMinderPlotData(tweets, result, featureLevelAnalysis,modelName))

	featureLevelAnalysis[f] = {}
	featureLevelAnalysis[f]["barPlot"] = {}
	averageRating = 0

	featureLevelAnalysis[f]["tweets"] = tweets
	totalCount = (result.count(5)+result.count(4)+result.count(3)+result.count(1)+result.count(2))
	overallRatings+=totalCount
		
	for i in range(1,6):
		featureLevelAnalysis["overall"]["barPlot"][str(i)] = featureLevelAnalysis["overall"]["barPlot"].get(str(i), 0) + result.count(i) 
		featureLevelAnalysis[f]["barPlot"][str(i)] = round(100.0*result.count(i)/totalCount, 1)

	featureLevelAnalysis[f]["donutPlot"] = {}
	featureLevelAnalysis["overall"]["averageRating"] = featureLevelAnalysis["overall"].get("averageRating", 0) + (result.count(5)*5.0+result.count(4)*4.0+result.count(3) *3+result.count(1)+result.count(2)*2.0)
	featureLevelAnalysis[f]["averageRating"+f] = round((result.count(5)*5.0+result.count(4)*4.0+result.count(3) *3+result.count(1)+result.count(2)*2.0)/totalCount, 1)

	featureLevelAnalysis["overall"]["donutPlot"]["positive"] = featureLevelAnalysis["overall"]["donutPlot"].get("positive", 0) + result.count(5)+result.count(4)
	featureLevelAnalysis["overall"]["donutPlot"]["neutral"] = featureLevelAnalysis["overall"]["donutPlot"].get("neutral", 0) + result.count(3)
	featureLevelAnalysis["overall"]["donutPlot"]["negative"] = featureLevelAnalysis["overall"]["donutPlot"].get("negative", 0) + result.count(1)+result.count(2)
		
	featureLevelAnalysis[f]["donutPlot"]["positive"] = round((100.0*(result.count(5)+result.count(4))/totalCount), 1)
	featureLevelAnalysis[f]["donutPlot"]["neutral"] = round((100.0*(result.count(3))/totalCount), 1)
	featureLevelAnalysis[f]["donutPlot"]["negative"] = round((100.0*(result.count(1)+result.count(2))/totalCount), 1)

	featureLevelAnalysis["overallRatings"] = overallRatings

def classify(modelName):
	"""Fetch tweets and generate the data to render all plots.
	
	:param modelName: input given by the user.
	:returns: Returns the a dictionary of plot data.
	:rtype: Dictionary
	
	"""
	features = ["camera", "battery", "overall"]
	featureLevelAnalysis = {}
	featureLevelAnalysis["gapminderplot"] = []
	featureLevelAnalysis["overall"] = {}
	featureLevelAnalysis["overall"]["barPlot"] = {}
	featureLevelAnalysis["overall"]["donutPlot"] = {}
	featureLevelAnalysis["overallRatings"] = 0
	featureLevelAnalysis["overall"]["tweets"] = []
	tweets=[]
	for f in features[:-1]:
		term = modelName+" "+f
		fetchPreprocess(term, featureLevelAnalysis, f,modelName)
	
	linearsvc = pickle.load(open('SmartPhoneReview/data/LinearSVC', 'rb'))
	tfidf = pickle.load(open('SmartPhoneReview/data/tfidf', 'rb'))
	overallRatings = featureLevelAnalysis["overallRatings"]
	tweets = list(set(twitterFetchTweets.searchSmartPhone(modelName)))
	featureLevelAnalysis["overall"]["tweets"] = tweets
	result = list(linearsvc.predict(tfidf.transform(tweets)))
	overallRatings += (result.count(5)+result.count(4)+result.count(3)+result.count(1)+result.count(2))

	for i in range(1,6):
		featureLevelAnalysis["overall"]["barPlot"][str(i)] = round(100.0*(result.count(i)+featureLevelAnalysis["overall"]["barPlot"].get(str(i), 0))/ overallRatings, 1)

	featureLevelAnalysis["overall"]["averageRating"] = round((featureLevelAnalysis["overall"]["averageRating"]+result.count(5)*5.0+result.count(4)*4.0+result.count(3) *3+result.count(1)+result.count(2)*2.0)/overallRatings, 1)
	featureLevelAnalysis["overall"]["donutPlot"]["positive"] = round(100.0*(featureLevelAnalysis["overall"]["donutPlot"].get("positive", 0) + result.count(5)+result.count(4)) /overallRatings, 1) 
	featureLevelAnalysis["overall"]["donutPlot"]["neutral"] = round(100.0*(featureLevelAnalysis["overall"]["donutPlot"].get("neutral", 0)+ result.count(3))  /overallRatings, 1) 
	featureLevelAnalysis["overall"]["donutPlot"]["negative"] = round(100.0*(featureLevelAnalysis["overall"]["donutPlot"].get("negative", 0) + result.count(1)+result.count(2)) /overallRatings, 1)


	t = generateGapMinderPlotData(tweets, result, featureLevelAnalysis,modelName)
	featureLevelAnalysis["words"] = remove_values_from_list(featureLevelAnalysis["words"],modelName)
	featureLevelAnalysis["gapminderplot"]=[createDataFrameGapMinder(featureLevelAnalysis["words"],modelName)]+featureLevelAnalysis["gapminderplot"]


	return featureLevelAnalysis