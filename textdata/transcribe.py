#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

import argparse
import io
import os
import sys
import json

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

# [START speech_transcribe_sync]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config, audio)

    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

#     # [END speech_python_migration_sync_response]
# # [END speech_transcribe_sync]

    return format_result_into_json(response)

def transcribe_gs_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    # with io.open(speech_file, 'rb') as audio_file:
    #     content = audio_file.read()

    # audio = types.RecognitionAudio(content=content)
    audio = types.RecognitionAudio(uri=speech_file)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    # response = client.recognize(config, audio)
    response = client.long_running_recognize(config, audio)

    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

#     # [END speech_python_migration_sync_response]
# # [END speech_transcribe_sync]

    return format_result_into_json(response.result())

def makeline(res, num):
    vals = res['alternatives'][0]
    transcript = vals['transcript']
    words = vals['words']
    starttime = words[0]['start_time']
    endtime = words[len(words)-1]['end_time']

    retstr = str(transcript) + "," + str(starttime) + "," + str(endtime) + "," + str(num)
    return retstr

def getsentence(words, start, end):
    sent = ""
    for i in range(start, end+1):\
        sent += words[i]['word'] + " "
    return sent.replace(',', "").strip()

def makelines(words, total, num):
    lines = []
    for i in range(0, len(words), 2):
        first = words[i]
        last = words[i+1]
        # print(first['pos'], last['pos'])
        sent = [getsentence(total, first['pos'], last['pos']), str(first['start_time']), str(last['end_time']), str(num)]
        lines.append(sent)
    return lines

def getsents(words):
    sents = []
    wd = words[0]
    wd['pos'] = 0
    sents.append(wd)
    i = 1
    while i < len(words)-1:
        wd = words[i]
        wd['pos'] = i
        wd2 = words[i+1]
        wd2['pos'] = i + 1

        if '.' in wd['word'] or '?' in wd['word'] or '!' in wd['word']:
            sents.append(wd)
            i += 1
            sents.append(wd2)
        i += 1

    wd = words[len(words)-1]
    wd['pos'] = len(words)-1
    sents.append(wd)
    return sents

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    parser.add_argument("num", help="file num", default=None)

    args = parser.parse_args()

    if args.path.startswith('gs://'):
        filename = args.path.split("question_detection_audio")
        writefile = open("../audiofiles/transcripts/" + filename[1][:-3] + "csv", 'w')
        transcript = json.loads(transcribe_gs_file(args.path))
    else:
        filename = args.path.split("/splitfiles/")
        writefile = open(filename[0] + "/transcripts/" + filename[1][:-3] + "csv", 'w')

        transcript = json.loads(transcribe_file(args.path))

    words = []
    for res in transcript['results']:
        wds = res['alternatives'][0]['words']
        words += wds

    sents = getsents(words)

    flnm = filename[1][:-4]
    lines = makelines(sents, words, flnm)
    for line in lines:
        writefile.write(",".join(line) + "\n")
