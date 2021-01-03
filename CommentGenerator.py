import random
import numpy as np
import pandas as pd

def commentGen(amount, path):
	word = ["puppy", "car", "rabbit", "girl",
			 "monkey", "runs", "hits", "jumps",
			 "drives", "barfs", "crazily.", "dutifully.",
			 "foolishly.", "merrily.", "occasionally.", "oofbruh"]
	rand_phrase = []

	for i in range(amount):
		rand_i = random.randrange(0, len(word) - 1)
		rand_phrase.append(word[rand_i])

	file1 = open(path + "randomComments.txt", "w+")
	file1.write(','.join(rand_phrase))
	file1.close()

account = pd.read_csv("randomAccounts.csv", header=None)

file1 = open("randomComments.txt", "w+")
file1.write(','.join(list(account.iloc[:, 0])))
file1.close()