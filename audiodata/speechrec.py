#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import statistics as stats
import parselmouth
import joblib

import sys
sys.path.insert(0, '../textdata/')
import texttyping

def getspeech(r):
    with sr.Microphone() as source:
        # print("Say something!")
        print ("Listening for speech: ")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)
        # print("You said: " + speech)

        return audio, speech
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def getwavspeech(filename, r):
    openfile = sr.AudioFile(filename)
    with openfile as source:
        audio = r.record(source)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)

        return audio, speech
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def highgreaterthanlow(pitches):
    length = len(pitches)

    first = pitches[:length//2]
    second = pitches[length//2:]

    if sum(first) < sum(second):
        return 1
    return 0

def raisingsumcount(pitches):
    sum = 0
    count = 0
    for i in range(len(pitches)-1):
        if pitches[i+1] > pitches[i]:
            sum += (pitches[i+1] - pitches[i])
            count += 1
    return sum, count

def fallingsumcount(pitches):
    sum = 0
    count = 0
    for i in range(len(pitches)-1):
        if pitches[i+1] < pitches[i]:
            sum += (pitches[i+1] - pitches[i])
            count += 1
    return sum, count

def containsQword(text):
    words = text.split(" ")[:3]
    questions = ["who", "whose", "who's", "who'd", "what", "what's", "what're", "when", "when's", "where", "where's", "why", "why's", "how", "how's", "can", "is", "isn't", "do", "does"]

    return any(x in words for x in questions)

def printparams(list):
    for l in list:
        print (l, "\t:\t", list[l])

def getstats(sound):
    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']

    pitches = [x for x in pitch_values if x != [0]]

    maxval = max(pitches)
    minval = min(pitches)

    pitches = [ (x - minval)/(maxval-minval) for x in pitches] # normalize data

    raisesum, raisecount = raisingsumcount(pitches)
    fallsum, fallcount = fallingsumcount(pitches)

    # print ("\nF0 PARAMETERS:")
    list = {}
    list["min"] = minval
    list["max"] = maxval
    list["range"] = maxval-minval
    list["mean"] = stats.mean(pitches)
    list["median"] = stats.median(pitches)
    list["upsum"] = raisesum
    list["dnsum"] = fallsum
    list["upct"] = raisecount
    list["dnct"] = fallcount
    list["HgtL"] = highgreaterthanlow(pitches)
    list["raise"] = 1 if raisesum > fallsum else 0
    list["num"] = len(pitches)
    # list["hasQ"] = containsQword(text)

    # print (list.values())
    # printparams(list)

    return list

def from_mic(r):
    filename = "audiofiles/mic-results.wav"
    audio, speech = getspeech(r)

    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
        f.close()

    sound = parselmouth.Sound(filename)
    # getstats(sound)

    return sound, speech

def from_mic_loop():
    # obtain audio from the microphone
    r = sr.Recognizer()
    filename = "audiofiles/mic-results.wav"

    more = 'y'

    while (more == 'y'):
        audio, speech = getspeech(r)

        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
            f.close()

        sound = parselmouth.Sound(filename)
        getstats(sound)

        more = input("more? (y/n) ")

def from_file(filename):
    # obtain audio from the microphone
    r = sr.Recognizer()
    audio, speech = getwavspeech(filename, r)

    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
        f.close()

    sound = parselmouth.Sound(filename)
    stats = getstats(sound)

    return speech, stats

def get_prediction(classifier, speech):
    nltkspeech = texttyping.dialogue_act_features(speech)
    # print(nltkspeech)

    return classifier.classify(nltkspeech)

if __name__ == "__main__":
    # sound, speech = from_mic(sr.Recognizer())
    speech, stats = from_file("audiofiles/mic-results.wav")
    # print(speech)
    # printparams(stats)

    # classifier = texttyping.trainclassifier()

    filename = "classifiers/maxentclassifier.joblib"
    maxentclass = joblib.load(filename)

    speech1 = "is this a question"
    speech2 = "this is a statement"

    print(speech, ":", get_prediction(maxentclass, speech))
    print(speech1, ":", get_prediction(maxentclass, speech1))
    print(speech2, ":", get_prediction(maxentclass, speech2))
