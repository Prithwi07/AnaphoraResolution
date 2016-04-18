#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import codecs
import re
accepted_annaphora_list=[]
# with open('acceptedAnaphoraList.txt','r') as f:
#     accepted_annaphora_list.append(f.readline())
    
accepted_annaphora_list = ['मैं','हम','आप' ,'तुम' ,'तू' ,'यह' ,'वह' ,'ये' ,'वे' ,'मुझे' ,'मुझको' ,'हमें' ,'हमको' ,'तुझे' ,'तुझको' ,'तुम्हें' ,'तुमको' ,'आपको' ,'इसे' ,'इसको' ,'इन्हें' ,'इनको' ,'उसे' ,'उसको' ,'उन्हें' ,'उनको' ,'मैंने' ,'हमने' ,'तुने' ,'तुमने' ,'आपने' ,'इसने' ,'इन्होंने' ,'उसने' ,'उन्होंने' ,'मुझसे' ,'हमसे' ,'तुझसे' ,'तुमसे' ,'आपसे' ,'इससे' ,'इनसे' ,'उससे' ,'उनसे' ,'मेरा' ,'मेरी' ,'मेरे' ,'तेरा' ,'तेरी' ,'तेरे' ,'हमारा' ,'हमारी' ,'हमारे' ,'आपका' ,'तुम्हारा' ,'इसका' ,'उसका' ,'इनका' ,'उनका' ,'उनकी' ,'उनके' ,'तुम्हारा' ,'तुम्हारी' ,'तुम्हारे' ,'आपकी' ,'आपके' ,'इसकी' ,'उसकी' ,'इसके' ,'उसके' ,'इनकी' ,'इनके' ,'मुझमे' ,'हममें' ,'तुझमें' ,'आपमें' ,'उसमें' ,'उनमें' ,'इसमें' ,'इनमें' ,'जो' ,'जिसने' ,'जिसे' ,'जिससे' ,'जिसको' ,'जिसका' ,'जिसकी' ,'जिसके' ,'जिसमें' ,'जिन्होनें' ,'जिन्हे' ,'जिनसे' ,'जिनको' ,'जिनका' ,'जिनकी' ,'जिनके' ,'जिनमें' ,'अपना' ,'अपने' ,'अपनी' ,'अपनों' ,'अपनेआप' ,'स्वयं' ,'खुद' ,'कोई' ,'कुछ' ,'सभी' ,'यहां' ,'यहाँ' ,'वहां' ,'वहाँ' ,'जहां' ,'जहाँ' ]
def createDict(filename):
    rootDir = dict()
    newSentenceDict = dict()
    sentenceCntr = 0
    begin=False
    ann_num=-1
    can_num=-1
    with codecs.open(filename,"r",encoding="utf-8") as infile:
        for line in infile:
            isAnn=False
            isCan=False
            #print(line.encode("utf-8"))
            lineTuples = line.encode('utf-8').split('\t')
            #print(lineTuples)
            if (lineTuples[0][0] == '#'):
                continue
            elif ((lineTuples[0] == '\r\n' or lineTuples[0] == '\n')):
                rootDir[sentenceCntr] = newSentenceDict
                sentenceCntr += 1
                newSentenceDict = dict() 
                continue
            else:
                wordAttribList = list()
                m1 = re.search(r"([0-9])+", lineTuples[7])
                #wordAttribList = lineTuples[3:8]
                if(lineTuples[5]=='B-NP' and lineTuples[4]=='PRP' and lineTuples[7]!='-' and (lineTuples[3] in accepted_annaphora_list)):
                    m = re.search(r"\(([0-9])+\)", lineTuples[7])
                    if(m != None ):
                        isAnn=True
                        ann_num=m.group(1)
                    else:
                        isAnn=False
                else:
                    isAnn=False
                if(lineTuples[7]!='-'):
                    if (lineTuples[4]=='NN' or lineTuples[4]=='NNP'): 
                        isCan=True
                        can_num = m1.group(0)
                        begin=False
                    elif (lineTuples[7].count('(') > lineTuples[7].count(')')): 
                        can_num = lineTuples[7].strip()[-1:]
                        begin=True
                    else:
                        begin=False    
                elif (begin):
                    if (lineTuples[4]=='NN' or lineTuples[4]=='NNP'): 
                        isCan=True
                        begin=False
                else:
                    isCan=False                    
                wordAttribList = lineTuples[3:8]      
                wordAttribList.append(isAnn)
                wordAttribList.append(isCan)
                ####### Morph string manipulation starts here #####
                if len(lineTuples) > 7:
                    morphString = lineTuples[8]
                    morphTupples = morphString.split('|')
                    morphResults = len(morphTupples)
                    if morphResults > 1:
                        str = morphTupples[1].strip()
                        
                        str = str.split("\'",1)[1]
                        str = str[:-2]
                        
                        morphKnowledge = str.split(',')     #this has tupples from first morph output
                        #print(morphKnowledge)
                        
                        wordAttribList.append(morphKnowledge[2])
                        wordAttribList.append(morphKnowledge[3])
                
                ##### End of Morph String #####
                wordAttribList.append(ann_num)
                wordAttribList.append(can_num)
                newSentenceDict[lineTuples[2]] = wordAttribList # Added word attributes
#                 print(newSentenceDict)
        
        rootDir[sentenceCntr] = newSentenceDict     #once last sentence addition      
    return rootDir
    


if __name__ == "__main__":
    createDict()
##################### Notes ########################
# These are the fields in rootDir #
# [0] -> Word #
# [1] -> POS #
# [2] -> Chunk Tag #
# [3] -> NER #
# [5] -> Gender#
# [6] -> singular/plural #
# Usage: rootDir[sentence number][word number][0-6]#
 