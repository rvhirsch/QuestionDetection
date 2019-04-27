import os

# concat all files for single audio

totalfile = open("./sentdata/sents.csv", 'w')

for dirname in os.listdir("./sentdata/"):
    if dirname == "transcripts" or dirname == "splitfiles" or dirname == "sents.csv":
        continue

    transcripts = "../audiofiles/sentdata/"+dirname+"/transcripts/"
    for filename in os.listdir(transcripts):
        # print(filename)
        filename = transcripts + filename

        f = open(filename, 'r')

        for sent in f:
            # if dirname == "17-1606":
            #     print("OLD:",sent)

            newsent = sent.strip()
            if '?' in newsent:
                newsent += ",1"
            else:
                newsent += ",0"
            totalfile.write(newsent + "\n")

            # if dirname == "17-1606":
            #     print("NEW:",newsent)

        f.close()

totalfile.close()