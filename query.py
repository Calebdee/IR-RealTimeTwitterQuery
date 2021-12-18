import pickle 
import PySimpleGUI as sg
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import nltk


def main():
	ii = 2
	tw = 2
	mu = 1

	
	if len(sys.argv) != 2:
		print("Invalid query call, consider the example query")
		print("python query.py \"QUERY TYPE HERE\"")
		return

	query = sys.argv[1].split(" ")

	with open('invert_index.pickle', 'rb') as handle:
		ii = pickle.load(handle)
	with open('tweet_corpus.pickle', 'rb') as handle:
		tw = pickle.load(handle)

	lemma = nltk.wordnet.WordNetLemmatizer()

	matches = []
	for keyword in query:
		kerword = lemma.lemmatize(keyword).lower()
		if keyword in ii:
			for num in ii[keyword]:
				if num not in matches:
					matches.append(num)
	
	df = pd.DataFrame(index=range(len(matches)),columns=range(4))
	row = 0
	print("Tweets that matched a keyword:" + str(len(matches)))

	for match in matches:
		ql = 0
		for keyword in query:
			d = tw[match].text.split()
			d_count = 0
			for w in d:
				if w.lower() == keyword:
					d_count += 1
			if keyword  in ii:
				ql += math.log((len(d)/(len(d)+mu))*(d_count/len(d)) + (mu/(mu+len(d)))*(len(ii[keyword])/len(ii)))
		df[0][row] = tw[match].text
		df[1][row] = ql
		df[2][row] = tw[match].pic
		df[3][row] = tw[match].time
		row += 1
	df = df.sort_values(by=[1], ascending=False)

	print("Median query log likelihood: " + str(df[1].median()))
	print("Model's Best Match: " + df[0][0])
	print("See the full output in out.csv")
	df.to_csv("out.csv")
	

class Tweet():
	def __init__(self, user, text, time, profile_pic):
		self.user = user
		self.text = text
		self.time =  time
		self.pic = profile_pic

if __name__ == "__main__":
	main()