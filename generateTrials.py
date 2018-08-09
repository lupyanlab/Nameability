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
	setnum = int(runTimeVars['setnum'])
	images = pd.read_csv('filesdoc_sets.csv')
	
	if setnum == 1:
		images = images[images.setnum == 1]
	elif setnum == 3:
		images = images[images.setnum == 3]
	elif setnum == 5:
		images = images[images.setnum == 5]	
	elif setnum == 7:
		images = images[images.setnum == 7]
	else:
		images = images[images.setnum == 1]
		
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
    trialList = generateTrials({'workerId':sys.argv[1]},['workerId'], {'setnum':sys.argv[2]},['setnum'])
 #	trialList = generateTrials({'subjCode':'NBT_set3a', 'gender':'f', 'seed':4, 'setnum':'3'},['subjCode','gender','seed', 'setnum'])
 #	trialList = generateTrials({'subjCode':'NBT_set7a', 'gender':'f', 'seed':4, 'setnum':'7'},['subjCode','gender','seed', 'setnum'])
 #	trialList = generateTrials({'subjCode':'NBT_set5a', 'gender':'f', 'seed':4, 'setnum':'5'},['subjCode','gender','seed', 'setnum'])
	





