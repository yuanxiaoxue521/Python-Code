#This file combines scores, e.g. from P_P and KH, into one file. 
#The new scores are "fusion of verifiers", can be directly given to the EER code.
#author: Guochen

import os
import re
import csv
import sys

def isCurrentBigger(F1, F2): #compares two current lines of two feature sets
    return ((F1.measurement > F2.measurement and F1.templateId == F2.templateId and F1.testId == F2.testId) or \
					(F1.templateId == F2.templateId and F1.testId > F2.testId) or \
					F1.templateId > F2.templateId)

def areTheyEqual(F1, F2):
	return F1.measurement == F2.measurement and F1.templateId == F2.templateId  and F1.testId == F2.testId 

def errorWrite(errorFile, message):
	#TODO finish this, put it into code 
	errorFile.write('%s \n' %(message))
	errorFile.write('KH: %s \n' %(lineKH))
	errorFile.write('Digraph %s \n' %(lineDigraph))
	errorFile.write('P_P: %s \n' %(lineP_P))
	errorFile.write('Combined revision bursts %s \n' %(lineCombinedRevisionBursts))
	errorFile.write('-------\n')


class currentFeatureInfo: #currently only for holding info about current row
	measurement = 0
	templateId = 0
	testId = 0
	def __init__(self, name):
		self.name = name

#iterate through weights: first is KH, second P_P, third digraph, fourth combined revision burst
#DONE:#####
#weightArray = [[0.2, 0, 0.8, 0], [0.9, 0, 0.1, 0], [0.1, 0, 0.9, 0], #KH + digraph
#	[0.7, 0.3, 0, 0], [0.6, 0.4, 0, 0], #KH + P_P
#	[0.4, 0.2, 0.4, 0], 
#weightArray = [[0.3, 0.2, 0.5, 0], [0.5, 0.2, 0.3, 0], #KH + digraph + P_P
#	[0.4, 0.1, 0.4, 0.1], [0.3, 0.1, 0.5, 0.1], 
	#TODo:
#weightArray = [[0.5, 0.1, 0.3, 0.1]] #KH + digraph + P_P + combined revision burst
weightArray = [[0.2, 0, 0.8, 0], [0.7, 0.3, 0, 0]]
for currentWeights in weightArray:
	#weight should sum to one
	WEIGHT_KH = currentWeights[0]
	WEIGHT_P_P = currentWeights[1]
	WEIGHT_DIGRAPH = currentWeights[2]
	WEIGHT_COMBINED_REVISION_BURSTS = currentWeights[3]

	print 'KH:', WEIGHT_KH, ' P_P:', WEIGHT_P_P, ' Digraph:', WEIGHT_DIGRAPH, ' Combined revision:', WEIGHT_COMBINED_REVISION_BURSTS

	if abs((WEIGHT_KH + WEIGHT_P_P + WEIGHT_DIGRAPH + WEIGHT_COMBINED_REVISION_BURSTS) - 1) > 0.000001:
		currentSum = WEIGHT_KH + WEIGHT_P_P + WEIGHT_DIGRAPH + WEIGHT_COMBINED_REVISION_BURSTS
		sys.stdout.write('WARNING: weights should sum to one, otherwise fusion of verifiers does not make sense! \n')
		print 'current sum is ', currentSum
		sys.exit() #finish the script
	verifierArray = ['SM'] #Se
	sliceArray =  [30, 60, 90, 120, 150, 180, 210] #30, 60
	for verifier in verifierArray:
		sys.stdout.write('%s \n' %(verifier))
		for sliceSize in sliceArray:
			sys.stdout.write('%d \n' %(sliceSize))

			

			folderKH = ('/Users/zdenka/Documents/ml-tools/PP_Burst_code/scores_for_fusion/KH/metric_' + verifier + 
				'pause2000_best_features98_interval_' + str(sliceSize) +'_collection1_KH_150_added')
			folderP_P = ('/Users/zdenka/Documents/ml-tools/PP_Burst_code/scores_for_fusion/P_P/metric_' + verifier + 
				'_interval_' + str(sliceSize) + '_pause1000collection1features_72P_Pwith150_col')
			folderDigraph = ('/Users/zdenka/Documents/ml-tools/PP_Burst_code/scores_for_fusion/Digraph/metric_' + verifier + 
				'_interval_' + str(sliceSize) + '_collection1_featuresSelected_676_Digraph_with150')
			folderCombinedRevisionBursts = ('/Users/zdenka/Documents/ml-tools/PP_Burst_code/scores_for_fusion/CombinedRevisionBursts/metric_' +
				verifier + 'pause1000_best_features67_interval_' + str(sliceSize) +'_collection1_KH_150_added')
			newFolder = ('/Users/zdenka/Documents/ml-tools/PP_Burst_code/scores_for_fusion/CombinationOfVerifiers/metric_' + verifier + 
				'_interval_' + str(sliceSize) + '_pause1000collection1features_72P_P_weight' + 
				str(WEIGHT_P_P) + '98KH_weight' + str(WEIGHT_KH) + '_Digraph676_weight' + str(WEIGHT_DIGRAPH) + 
				'_CombinedRevisionBursts_weight' + str(WEIGHT_COMBINED_REVISION_BURSTS) + '_Combined')
			if not os.path.exists(newFolder):
				os.makedirs(newFolder)
			fileNameArray = ['GenuineScores', 'ImpostorScores']
			for fileName in fileNameArray:
				#info about current row: 
				P_P = currentFeatureInfo('P_P')
				KH = currentFeatureInfo('KH')
				Digraph = currentFeatureInfo('Digraph')
				CombinedRevisionBursts = currentFeatureInfo('CombinedRevisionBursts')

				fileKH = open(folderKH + '/' + fileName + 'Testing.txt', 'rU')
				lineArrayKH = fileKH.readlines()

				if WEIGHT_P_P != 0:
					fileP_P = open(folderP_P + '/' + fileName + 'Testing.txt', 'rU')
					lineArrayP_P = fileP_P.readlines()
				else:
					lineArrayP_P = ['0 measurements: 0 template: 0 test: 0']

				if WEIGHT_DIGRAPH != 0:
					fileDigraph = open(folderDigraph + '/' + fileName + 'Testing.txt', 'rU')
					lineArrayDigraph = fileDigraph.readlines()
				else:
					lineArrayDigraph = ['0 measurements: 0 template: 0 test: 0']

				if WEIGHT_COMBINED_REVISION_BURSTS != 0:
					fileCombinedRevisionBursts = open(folderCombinedRevisionBursts + '/' + fileName + 'Testing.txt', 'rU')
					lineArrayCombinedRevisionBursts = fileCombinedRevisionBursts.readlines()
				else:
					lineArrayCombinedRevisionBursts = ['0 measurements: 0 template: 0 test: 0']

				newFileWithDetails = open(newFolder + '/' + fileName + 'Testing.txt', 'w')
				newFile = open(newFolder + '/' + fileName + '.txt', 'w')
				errorFile = open(newFolder + '/ERROR' + fileName + '.txt', 'w')
				
				P_PCounter = 0
				KHCounter = 0
				DigraphCounter = 0
				CombinedRevisionBurstsCounter = 0
				while KHCounter != len(lineArrayKH):
					#sys.stdout.write('line KH: %s' %(lineKH))
					lineKH = lineArrayKH[KHCounter].rstrip()

					#Counter of P_P lines:
					if P_PCounter < len(lineArrayP_P): 
						lineP_P = lineArrayP_P[P_PCounter].rstrip()
					else: #when there are no more lines for P_P
						lineP_P = '0 measurements: 0 template: 0 test: 0'

					#Counter of Digraph lines: 
					if DigraphCounter < len(lineArrayDigraph): 
						lineDigraph = lineArrayDigraph[DigraphCounter].rstrip()
					else: #when there are no more lines for digraph
						lineDigraph = '0 measurements: 0 template: 0 test: 0'

					#Counter of Combined revision burst lines:
					if CombinedRevisionBurstsCounter < len(lineArrayCombinedRevisionBursts): 
						lineCombinedRevisionBursts = lineArrayCombinedRevisionBursts[CombinedRevisionBurstsCounter].rstrip()
					else: #when there are no more lines for combined revision bursts
						lineCombinedRevisionBursts = '0 measurements: 0 template: 0 test: 0'
					#sys.stdout.write('line P_P : %s \n' %(lineP_P))
					lineKHSplit = lineKH.split(' ')
					lineP_PSplit = lineP_P.split(' ')
					lineDigraphSplit = lineDigraph.split(' ')
					lineCombinedRevisionBurstsSplit = lineCombinedRevisionBursts.split(' ')

					#0 is score, 2 number of measurement, 4 templateID, 6 testID
					KH.measurement = int(lineKHSplit[2])
					P_P.measurement = int(lineP_PSplit[2])
					Digraph.measurement = int(lineDigraphSplit[2])
					CombinedRevisionBursts.measurement = int(lineCombinedRevisionBurstsSplit[2])

					KH.templateId = int(lineKHSplit[4])
					P_P.templateId = int(lineP_PSplit[4])
					Digraph.templateId = int(lineDigraphSplit[4])
					CombinedRevisionBursts.templateId = int(lineCombinedRevisionBurstsSplit[4])

					KH.testId = int(lineKHSplit[6])
					P_P.testId = int(lineP_PSplit[6])
					Digraph.testId = int(lineDigraphSplit[6])
					CombinedRevisionBursts.testId = int(lineCombinedRevisionBurstsSplit[6])

					if (areTheyEqual(KH, P_P) or WEIGHT_P_P == 0) and \
						(areTheyEqual(KH, Digraph) or  WEIGHT_DIGRAPH == 0) and \
						(areTheyEqual(KH, CombinedRevisionBursts) or WEIGHT_COMBINED_REVISION_BURSTS == 0):
						#best situations, measurements are present in all the features. all the lines are matching! 
						#weight the scores and increase the counter for all the features
						scoreKH = float(lineKHSplit[0]) #TODO currentWeightScore
						scoreP_P = float(lineP_PSplit[0])
						scoreDigraph = float(lineDigraphSplit[0])
						scoreCombinedRevisionBursts = float(lineCombinedRevisionBurstsSplit[0])
						newScore = WEIGHT_KH*scoreKH + WEIGHT_P_P*scoreP_P + WEIGHT_DIGRAPH*scoreDigraph + WEIGHT_COMBINED_REVISION_BURSTS*scoreCombinedRevisionBursts
						P_PCounter = P_PCounter + 1
						KHCounter = KHCounter + 1
						DigraphCounter = DigraphCounter + 1
						CombinedRevisionBurstsCounter = CombinedRevisionBurstsCounter + 1
					
					elif (isCurrentBigger(KH, P_P) and P_P.measurement != 0) or \
						(isCurrentBigger(KH, Digraph) and Digraph.measurement != 0) or \
						(isCurrentBigger(KH, CombinedRevisionBursts) and CombinedRevisionBursts.measurement != 0): 
						#TODO add for not present weights
						#some measurement, which is not in KH: this happens rarely
						if areTheyEqual(P_P, Digraph) and areTheyEqual(P_P, CombinedRevisionBursts):# restriction 0 not needed, it's already at one level higher
							#all except KH are present. 
							newScore = ((WEIGHT_DIGRAPH + WEIGHT_KH)*float(lineDigraphSplit[0]) + WEIGHT_P_P*float(lineP_PSplit[0]) 
								+ WEIGHT_COMBINED_REVISION_BURSTS*float(lineCombinedRevisionBurstsSplit[0]))

							P_PCounter = P_PCounter + 1
							DigraphCounter = DigraphCounter + 1
							CombinedRevisionBurstsCounter = CombinedRevisionBurstsCounter + 1

							errorWrite(errorFile, 'all three without KH')
						elif Digraph.measurement != 0 and (isCurrentBigger(P_P, Digraph) or P_P.measurement ==0) and \
						(isCurrentBigger(CombinedRevisionBursts, Digraph) or CombinedRevisionBursts.measurement == 0):
							#current is only digraph
							newScore = float(lineDigraphSplit[0])
							DigraphCounter = DigraphCounter + 1
							errorWrite(errorFile, 'only digraph without KH')
						elif P_P.measurement != 0 and (isCurrentBigger(Digraph, P_P) or Digraph.measurement == 0) and\
						(isCurrentBigger(CombinedRevisionBursts, P_P) or CombinedRevisionBursts.measurement == 0):
							#current is only P_P
							newScore = float(lineP_PSplit[0])
							P_PCounter = P_PCounter + 1
							errorWrite(errorFile, 'only P_P without KH')
						elif CombinedRevisionBursts.measurement != 0 and (isCurrentBigger(P_P, CombinedRevisionBursts) or P_P.measurement == 0) and \
						(isCurrentBigger(Digraph, CombinedRevisionBursts) or Digraph.measurement == 0):
							#current is only combined revision bursts
							newScore = float(lineCombinedRevisionBurstsSplit[0])
							CombinedRevisionBurstsCounter = CombinedRevisionBurstsCounter + 1
							errorWrite(errorFile, 'only combined revision burst without kh')
						elif areTheyEqual(P_P, Digraph) and P_P.measurement != 0 and Digraph.measurement != 0:
							#only P_P + Digraph
							newScore = ((WEIGHT_KH + WEIGHT_DIGRAPH)*float(lineDigraphSplit[0]) + 
								(WEIGHT_P_P + WEIGHT_COMBINED_REVISION_BURSTS)*float(lineP_PSplit[0]))

							P_PCounter = P_PCounter + 1
							DigraphCounter = DigraphCounter + 1
							
							errorWrite(errorFile, 'P_P + digraph without kh')
						elif areTheyEqual(P_P, CombinedRevisionBursts) and P_P.measurement != 0 and CombinedRevisionBursts.measurement != 0:
							newScore = ((WEIGHT_P_P/(WEIGHT_P_P + WEIGHT_COMBINED_REVISION_BURSTS))*float(lineP_PSplit[0]) + 
							(WEIGHT_COMBINED_REVISION_BURSTS/(WEIGHT_P_P + WEIGHT_COMBINED_REVISION_BURSTS))*float(lineCombinedRevisionBurstsSplit[0]))	

							P_PCounter = P_PCounter + 1
							CombinedRevisionBurstsCounter = CombinedRevisionBurstsCounter + 1

							errorWrite(errorFile, 'P_P + combined revision burst without kh')
						elif areTheyEqual(Digraph, CombinedRevisionBursts) and Digraph.measurement != 0 and CombinedRevisionBursts.measurement != 0:
							newScore = ((WEIGHT_KH + WEIGHT_DIGRAPH) * float(lineDigraphSplit[0]) + 
								(WEIGHT_P_P + WEIGHT_COMBINED_REVISION_BURSTS)*float(lineCombinedRevisionBurstsSplit[0]) )

							DigraphCounter = DigraphCounter + 1
							CombinedRevisionBurstsCounter = CombinedRevisionBurstsCounter + 1

							errorWrite(errorFile, 'digraph + combined revision burst without kh')
						else:
							sys.stdout.write('something wrong in my conditions non KH\n')
							sys.stdout.write('KH: %s \n' %(lineKH))
							sys.stdout.write('Digraph %s \n' %(lineDigraph))
							sys.stdout.write('P_P: %s \n' %(lineP_P))
							sys.stdout.write('Combined revision bursts %s \n' %(lineCombinedRevisionBursts))
							
							#NO KH COUNTER +1 there!!!
					else:
						#this measurement does not exist in all featues, but it exists in KH
						KHCounter = KHCounter + 1
						isCurrentDigraph = False
						isCurrentP_P = False
						isCurrentCombinedRevisionBurst = False
						#P_P was not available for this measurement, KH has weight 100 % 
						if areTheyEqual(KH, Digraph) and Digraph.measurement != 0: 
							DigraphCounter = DigraphCounter + 1
							isCurrentDigraph = True
						if areTheyEqual(KH, P_P) and P_P.measurement != 0: 
							P_PCounter = P_PCounter + 1
							isCurrentP_P = True
						if areTheyEqual(KH, CombinedRevisionBursts) and CombinedRevisionBursts.measurement != 0: 
							CombinedRevisionBurstsCounter = CombinedRevisionBurstsCounter + 1
							isCurrentCombinedRevisionBurst = True
						#compute scores:
						#only KH and digraph:
						if isCurrentDigraph and not isCurrentP_P and not isCurrentCombinedRevisionBurst:
							newScore = WEIGHT_KH*float(lineKHSplit[0]) + (1-WEIGHT_KH)*float(lineDigraphSplit[0])
						elif not isCurrentDigraph and not isCurrentP_P and not isCurrentCombinedRevisionBurst:
							newScore = float(lineKHSplit[0])
						elif not isCurrentDigraph and isCurrentP_P and isCurrentCombinedRevisionBurst: 
							newScore = ((WEIGHT_DIGRAPH + WEIGHT_KH)*float(lineKHSplit[0]) + WEIGHT_P_P*float(lineP_PSplit[0]) + 
							WEIGHT_COMBINED_REVISION_BURSTS*float(lineCombinedRevisionBurstsSplit[0]))
						else: 
							currentBurstWeight = WEIGHT_COMBINED_REVISION_BURSTS + WEIGHT_P_P
							currentBurstScore = 0
							if isCurrentCombinedRevisionBurst and not isCurrentP_P:
								currentBurstScore = float(lineCombinedRevisionBurstsSplit[0])
							elif not isCurrentCombinedRevisionBurst and isCurrentP_P:
								currentBurstScore = float(lineP_PSplit[0])
							else:
								sys.stdout.write('something wrong in my conditions with KH \n')

							if isCurrentDigraph:
								newScore = (WEIGHT_KH*float(lineKHSplit[0]) + WEIGHT_DIGRAPH*float(lineDigraphSplit[0]) + 
								currentBurstWeight*currentBurstScore)
							else:
								newScore = (WEIGHT_KH + WEIGHT_DIGRAPH)*float(lineKHSplit[0]) + currentBurstWeight*currentBurstScore


							
					#example of line:'1.1904096337 measurements: 1 template: 1 test: 4'
					newFileWithDetails.write(str(newScore) + ' measurements: ' + str(KH.measurement) + ' template: ' + str(KH.templateId) + 
						' test: ' + str(KH.testId) + '\n')
					newFileWithDetails.write('P_PCounter %d' %(P_PCounter))
					newFileWithDetails.write('next line: %s \n' %(lineP_P))
					newFile.write(str(newScore) + '\n')


				fileKH.close()

				if WEIGHT_P_P != 0:
					fileP_P.close()
				if WEIGHT_DIGRAPH != 0:
					fileDigraph.close()
				if WEIGHT_COMBINED_REVISION_BURSTS != 0: 
					fileCombinedRevisionBursts.close()
				newFile.close()
				newFileWithDetails.close()
				errorFile.close()

