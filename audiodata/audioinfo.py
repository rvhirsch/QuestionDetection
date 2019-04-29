import os

import speechrec
# import texttyping

import csv
from pydub import AudioSegment

def getcutsentinfo(start, end, filename):
    tofile = "temp.wav"

    realfilename = filename.replace("transcripts", "splitfiles").replace(".csv", ".wav").replace("//", "/")
    print("CURR FILE:",realfilename)

    newAudio = AudioSegment.from_wav(realfilename)
    newAudio = newAudio[float(start)*1000 : float(end)*1000+1]

    newAudio.export(tofile, format="wav") #Exports to a wav file in the current path.
    return tofile

def getdatafromfolder(folderpath):
    path = folderpath.strip().split("/")
    filename = path[len(path)-2] + ".csv"
    # writefile = open("tempaudios.csv", 'w')

    writefile = open("./transcripts/"+filename, 'w')
    csv_writer = csv.writer(writefile, delimiter=",")

    folderpath += "/transcripts/"

    for filename in os.listdir(folderpath):
        f = open(folderpath + filename, 'r')

        csv_reader = csv.reader(f, delimiter=',')

        for row in csv_reader:
            start = row[1]
            end = row[2]
            sent = row[0]
            label = 1 if "?" in sent else 0

            print(filename, ":", start, "-", end, "=", label)

            try:
                getcutsentinfo(start, end, folderpath + filename)

                speech, stats = speechrec.from_file("temp.wav")  # stats = dict

                # if not "could not understand audio" in speech and not "Could not request results" in speech:
                towrite = list(stats.values())
                towrite.append(filename)
                towrite.append(label)
                print(towrite)

                csv_writer.writerow(towrite)
            except Exception as e:
                continue

        f.close()
    writefile.close()

def getalldata():
    writefile = open("audios.csv", 'w')
    csv_writer = csv.writer(writefile, delimiter=",")

    for foldername in os.listdir("../audiofiles/sentdata/"):
        foldername = "../audiofiles/sentdata/" + foldername + "/transcripts/"

        for filename in os.listdir(foldername):
            f = open(foldername + filename, 'r')

            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                start = row[1]
                end = row[2]
                sent = row[0]
                label = 1 if "?" in sent else 0

                print(filename, ":", start, "-", end, "=", label)

                getcutsentinfo(start, end, foldername+filename)

                try:
                    speech, stats = speechrec.from_file("temp.wav") # stats = dict

                    towrite = list(stats.values())
                    towrite.append(label)
                    print(towrite)

                    csv_writer.writerow(towrite)
                except Exception as e:  # if not "could not understand audio" in speech and not "Could not request results" in speech:

                    continue

            f.close()

    writefile.close()

def concatfiles():
    with open("audios.csv", 'w') as f:
        for filename in os.listdir("../audiodata/transcripts/"):
            print(filename)
            filename = "../audiodata/transcripts/"+filename
            audinfo = open(filename, 'r')
            f.write(audinfo.read())
            audinfo.close()
    f.close()

if __name__ == "__main__":
    print("getting audio data")

    # getdatafromfolder("../audiofiles/sentdata/16-1498/")
    # getdatafromfolder("../audiofiles/sentdata/17-204/")
    # getdatafromfolder("../audiofiles/sentdata/17-532/")
    # getdatafromfolder("../audiofiles/sentdata/17-571/")
    # getdatafromfolder("../audiofiles/sentdata/17-647/")
    getdatafromfolder("../audiofiles/sentdata/17-1091/") # TODO
    # getdatafromfolder("../audiofiles/sentdata/17-1094/")
    # getdatafromfolder("../audiofiles/sentdata/17-1174/")
    # getdatafromfolder("../audiofiles/sentdata/17-1184/")
    # getdatafromfolder("../audiofiles/sentdata/17-1201/")
    # getdatafromfolder("../audiofiles/sentdata/17-1299/")
    # getdatafromfolder("../audiofiles/sentdata/17-1307/")
    # getdatafromfolder("../audiofiles/sentdata/17-1471/")
    # getdatafromfolder("../audiofiles/sentdata/17-1484/")
    # getdatafromfolder("../audiofiles/sentdata/17-1594/")
    # getdatafromfolder("../audiofiles/sentdata/17-1606/")
    # getdatafromfolder("../audiofiles/sentdata/18-96/")
    # getdatafromfolder("../audiofiles/sentdata/18-431/")
    # getdatafromfolder("../audiofiles/sentdata/18-459/")

    # getdatafromfolder("../audiofiles/sentdata/17-1107/") # only first utterance
    # getdatafromfolder("../audiofiles/sentdata/17-290/") # breaks at 17-290-part51.wav, first utterance ??
    # getdatafromfolder("../audiofiles/sentdata/17-1625/") # broken for some reason??? - not used in audio data set, but used in text set

    print("concatting files")
    concatfiles()
    print("DONE")


