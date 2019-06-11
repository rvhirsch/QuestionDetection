from pydub import AudioSegment
from gtts import gTTS

import speech_recognition as sr
import string as STRING
import subprocess
import json
import os
import io

def format_result_into_json(result):
    json_result = {'results': []}

    for cur_result in result.results:
        speech_recognition_result = {
            'alternatives': []
        }
        for cur_alternative in cur_result.alternatives:
            speech_recognition_alternative = {
                'transcript': cur_alternative.transcript,
                'confidence': cur_alternative.confidence,
                'words': []
            }
            for word_info in cur_alternative.words:
                speech_recognition_alternative['words'].append({
                    'start_time': word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    'end_time': word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                    'word': word_info.word
                })
            speech_recognition_result['alternatives'].append(speech_recognition_alternative)
        json_result['results'].append(speech_recognition_result)

    return json.JSONEncoder(ensure_ascii=False).encode(json_result)

def rmpunctuation(sent):
    exclude = set(STRING.punctuation)
    exclude.remove("'")
    s = ''.join(ch for ch in sent if ch not in exclude)
    return s.lower()

def getspeech(filename):
    openfile = sr.AudioFile(filename)
    r = sr.Recognizer()
    with openfile as source:
        audio = r.record(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)

        return speech
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def getgooglespeech(speech_file):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    client = speech.SpeechClient()
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz= 24000, #48000,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)
    return format_result_into_json(response)

def formatresults(response):
    # results = json.loads(response)["results"]
    jstr = ""
    for res in json.loads(response)["results"]:
        jstr += res["alternatives"][0]["transcript"]
    return jstr

def getaudios(folderpath):
    for filename in os.listdir(folderpath):
        # print(filename + ":", getspeech(folderpath+filename))
        print(filename + ":")
        for sent in formatresults(getgooglespeech(folderpath+filename)).split(". "):
            print("\t"+sent)

def gettranscripts(folderpath):
    correct = 0
    incorrect = 0
    for filename in os.listdir(folderpath):
        f = open(folderpath+filename)
        # print(filename)
        for line in f:
            sent = line.split(",")[0]
            label = 1 if "?" in sent else 0
            # print(label, "/", filename, ":")

            try:
                # print("\t", sent)
                nopunct = rmpunctuation(sent)
                newsent = texttospeech(nopunct)
                # print("\t\tnew:", newsent)

                if "?" in sent and "?" in newsent:
                    correct += 1
                elif "." in sent and "." in newsent:
                    correct += 1
                else:
                    incorrect += 1
            except:
                continue

        f.close()

    print("correct:", correct)
    print("incorrect:", incorrect)

def mp3towav(src):
    dst = "temp.wav"
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

def texttospeech(sent):
    filename = "temp.mp3"
    tts = gTTS(sent, "en", slow=False)
    tts.save(filename)

    mp3towav(filename)
    wavfile = "temp.wav"
    googlespeech = getgooglespeech(wavfile)
    return formatresults(googlespeech)

if __name__=="__main__":
    # speech = getspeech("temp.wav")
    # getaudios(folderpath)

    folderpath = "../audiofiles/sentdata/" #17-290/transcripts/"

    for filename in os.listdir(folderpath):
        print(filename)
        gettranscripts(folderpath + filename + "/transcripts/")