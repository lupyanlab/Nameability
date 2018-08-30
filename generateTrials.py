#!/usr/bin/env python
import sys
import random
from itertools import permutations, combinations
import pandas as pd

separator = ","
																					
def generateTrials(workerId,setnum):
	#setnum = int(setnum)
	testFile = open('trials/'+workerId+ '_trials.csv','w')
	header = separator.join(["workerId", "setnum", "ProblemType", "PartID", "Image", "trialNum", "Message", "Nameability", "Version"])
	print >>testFile, header
	images = pd.read_csv('filesdoc_sets.csv')
	if setnum=='NA':
		setnum = random.choice(images.setnum.unique())
		images = images[images.setnum == setnum]
	elif int(setnum) in images.setnum.unique():
		images = images[images.setnum == int(setnum)]
		print "setnum is", setnum
		print len(images)
	else:
		print "Setnum must be one of ", str(images.setnum.unique())
	print "setnum is", setnum
	stim_list = images.Image.tolist()
	trials = []

	for trial_num,cur_image in enumerate(stim_list):
		subC1 = images.loc[images['Image'] == cur_image, 'ProblemType'].iloc[0]	
		PartID1 = images.loc[images['Image'] == cur_image, 'PartID'].iloc[0]	
		Message = images.loc[images['Image'] == cur_image, 'Message'].iloc[0]	
		Nameability = images.loc[images['Image'] == cur_image, 'Nameability'].iloc[0]	
		Version = images.loc[images['Image'] == cur_image, 'Version'].iloc[0]	
		trials.append(separator.join((str(workerId),str(setnum),str(subC1), str(PartID1), cur_image, str(trial_num+1), str(Message),  str(Nameability),  str(Version))))	 
	
	for cur_trial in trials:
		print >>testFile, cur_trial
		
if __name__ == "__main__":
	trialList = generateTrials(sys.argv[1], sys.argv[2])



