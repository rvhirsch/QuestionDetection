import os
import sys

# concat all files for single audio

totalfile = open("sents.csv", 'w')

for foldername in os.listdir("../audiofiles/sentdata/"):
    if foldername == "sents.csv":
        continue
    print("dir:", foldername)
    for filename in os.listdir("../audiofiles/sentdata/"+foldername+"/transcripts/"):
        filename = "../audiofiles/sentdata/"+foldername+"/transcripts/" + filename
        f = open(filename, 'r')

        for sent in f:
            newsent = sent.strip()
            if '?' in newsent.split(',')[0]:
                newsent += ",1"
            else:
                newsent += ",0"
            totalfile.write(newsent + "\n")
        f.close()

totalfile.close()

# add sents to end of full data
totalfile = open("sents.csv", 'r')

fullfile = open("../audiofiles/sentdata/sents.csv", 'a')
fullfile.writelines(totalfile.readlines())

totalfile.close()
fullfile.close()

# f = open("sents.csv", 'r')
# f2 = open("sents2.csv", 'w')
#
# for line in f:
#     # print(line)
#     splitted = line.split(",")
#     num = splitted[-2]
#     # print(num)
#     # num = "," + str(i) + ","
#     # print(num)
#     newnum = "17-1594-part" + str(num)
#     # print(newnum)
#     splitted[-2] = newnum
#     # newline = newline.replace(num, newnum)
#     newline = ",".join(splitted)
#     print(newline)
#     f2.write(newline)
#
# f.close()
# f2.close()
