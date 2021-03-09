# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import krippendorff


path = './groupdata/'
with open('agreeement.csv', 'w') as agreement_file:
    for filename in os.listdir(path):
        print(filename, end=" ")
        agreement_file.write(filename[filename.find("cwig") + 4:filename.rfind(".")] + ",")
        annotations_list = []
        with open(path + filename, "r") as file:
            for line in file.readlines():
                #print(line)
                annotations_dict = dict()
                line = line.split(",")
                #print(line[0])
                for index in range(1, len(line)-1): #omit the first and the last entries
                    word_date = line[index].split(":")
                    annotations_dict[word_date[0]] = word_date[1]
                    data = [float(val) for val in annotations_dict.values()]
                annotations_list.append(data)
                
            #print("Data: ", annotations_list)
            #TODO: calculate agreement
            agreement_value = krippendorff.alpha(reliability_data=annotations_list)
            print(agreement_value)
            agreement_file.write(str(round(agreement_value,3)) + "\n")