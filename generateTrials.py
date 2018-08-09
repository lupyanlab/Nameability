#!/usr/bin/env python
import random
from itertools import permutations, combinations
from useful_functions import circularList
import pandas as pd

separator = ","
																					
def generateTrials(runTimeVars,runTimeVarsOrder):
	testFile = open('trials/trialList_test_'+runTimeVars['subjCode']+ '.csv','w')
	print runTimeVarsOrder
	header = separator.join(runTimeVarsOrder) + separator + separator.join(("ProblemType", "PartID", "Image", "trialNum", "Message"))
	print >>testFile, header
	seed = int(runTimeVars['seed'])
	random.seed(seed)
	whichSet = int(runTimeVars['whichSet'])
	
	if whichSet == 1:
		images = pd.read_csv('filesdoc_set1.csv')
	elif whichSet == 3:
		images = pd.read_csv('filesdoc_set3.csv')
	elif whichSet == 5:
		images = pd.read_csv('filesdoc_set5.csv')
	elif whichSet == 7:
		images = pd.read_csv('filesdoc_set7.csv')
	else:
		images = pd.read_csv('filesdoc_set1.csv')
		
	stim_list = images.Image.tolist()
	trials = []

	for trial_num in range(60):
		trial = runTimeVars.copy()
		trialNum = 1+ trial_num
		selected_category = random.sample(stim_list,1)[0]
		pic1 = selected_category
		subC1 = images.loc[images['Image'] == pic1, 'ProblemType'].iloc[0]	
		PartID1 = images.loc[images['Image'] == pic1, 'PartID'].iloc[0]	
		Message = images.loc[images['Image'] == pic1, 'Message'].iloc[0]	
		trials.append(separator.join((str(subC1), str(PartID1), pic1, str(trialNum), str(Message))))	 
	
		if pic1 in stim_list:
			stim_list.remove(pic1)

	trialList = trials[:60]
	
	for curTrialList in trialList:
		trialData = separator.join([str(runTimeVars[curRuntimeVar]) for curRuntimeVar in runTimeVarsOrder])+separator+curTrialList
		print >>testFile, trialData
		
if __name__ == "__main__":
	trialList = generateTrials({'subjCode':'NBT_set3', 'gender':'f', 'seed':4, 'whichSet':'3'},['subjCode','gender','seed', 'whichSet'])
	trialList = generateTrials({'subjCode':'NBT_set7', 'gender':'f', 'seed':4, 'whichSet':'7'},['subjCode','gender','seed', 'whichSet'])
	trialList = generateTrials({'subjCode':'NBT_set1', 'gender':'f', 'seed':4, 'whichSet':'1'},['subjCode','gender','seed', 'whichSet'])
	trialList = generateTrials({'subjCode':'NBT_set5', 'gender':'f', 'seed':4, 'whichSet':'5'},['subjCode','gender','seed', 'whichSet'])






