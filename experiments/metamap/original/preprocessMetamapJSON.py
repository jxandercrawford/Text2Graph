import os
import sys
import json
import csv


#directory = "/Users/jess/Desktop/SeniorDesign/JSONfiles"

directory = "/home/xc383@drexel.edu/text2graph/experiments/metamap/sample"

### FOR EACH FILE

outputAnns = []
#semTypeStats = {}
cuiStats = {}
semTypes = {}


f_csv = open("/home/xc383@drexel.edu/text2graph/experiments/metamap/train_jsonPreprocess.csv", "w")
f_csv.write("filename, cui, dnStats, semType \n")

for filename in os.listdir(directory):
    dnStats = {}
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):

        ### Open file
        fp = open(f, 'r')
        lines = fp.readlines()

        try:
            texas = json.loads(lines[1])
        except:
            texas = None

        if texas:
            if "AllDocuments" in texas:

                for doc in texas["AllDocuments"]:
                    if "Document" in doc and "Utterances" in doc["Document"]:
                        utterances = doc["Document"]["Utterances"]
                        if utterances:
                            for utt in utterances:
                                ann = {}
                                ann["FileName"] = filename
                                if "Phrases" in utt:
                                    for phrase in utt["Phrases"]:
                                        if "Mappings" in phrase:  # if "Mappings" in phrase and len(phrase["Mappings"]) > 0:
                                            for mapping in phrase["Mappings"]:
                                                for mappingCandidate in mapping["MappingCandidates"]:
                                                    if not mappingCandidate["CandidateCUI"] in dnStats:
                                                        dnStats[ mappingCandidate["CandidateCUI"] ] = 1
                                                    else:
                                                        dnStats[ mappingCandidate["CandidateCUI"] ] += 1
                                                    if not mappingCandidate["CandidateCUI"] in semTypes:
                                                        semTypes[mappingCandidate["CandidateCUI"]] = mappingCandidate["SemTypes"]

                                                    ann["CandidateCUI"] = mappingCandidate["CandidateCUI"]
                                                    #ann["SemTypes"] = "|" + "|".join(mappingCandidate["SemTypes"]) + "|"
                                                    cui = ann["CandidateCUI"]
                                                    outputAnns.append(ann.copy()) #not sure but useful for writing csv


                        else:
                            print("checking anns failed")

                    else:
                        print("utterances failed")

    fp.close()


    for eachCUI in dnStats:
        f_csv.write(filename + "," + eachCUI + "," + str(dnStats[eachCUI]) + "," + '"' + str(semTypes[eachCUI]) + '"' + "\n")

            # wrhite filename, eachCUI, dnStats[eachCUI]

f_csv.close()
