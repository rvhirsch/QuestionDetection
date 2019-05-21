## Files
- audiodata/audioinfo.py: inside audiodata dir, run with $ python3 audioinfo.py
- audiofiles/splitaudio.py: splits audio into 1 minute increments, puts new files in splitfiles directory
- textdata/transcribe.py: takes 1 minute wav file and transcribes, splitting by sentence
- textdata/concatfiles.py: takes all transcriptions and puts them into single file
- textdata/transcribe.sh: inside textdata dir, run with $ ./transcribe.sh \[case-number\]

## Text
- sentences_google.csv: from google speech to text transcript
- sentences_ibm.csv: from ibm speech to text transcript

In each row:
1. full sentence text
2. sentence start time in audio files
3. sentence end time in audio file
4. corresponding audio file id
5. label: 0 = statement, 1 = question

## Audio

Input: vocal speech - one sentence
Output: 13 parameters based on slices of 0.08 sec

1. min pitch value
2. max pitch value
3. pitch range (max-min)
4. mean pitch
5. median pitch
6. check if pitch increases in 2nd half of statement
7. total pitch increasing
8. count of increasing slices
9. total pitch decreasing
10. count of decreasing slices
11. check if increasing total > decreasing total
12. count of nonzero pitches

## Audio Data Sources
- All via https://www.supremecourt.gov/oral_arguments/argument_audio/2018 
- 16-1498
- 17-204
- 17-290
- 17-532
- 17-571
- 17-647
- 17-1091
- 17-1094
- 17-1107
- 17-1174
- 17-1184
- 17-1201
- 17-1299
- 17-1307
- 17-1471
- 17-1484
- 17-1594
- 17-1606
- 17-1625
- 18-95
- 18-302
- 18-389
- 18-431
- 18-457
- 18-459
- 18-481
- 18-485
- 18-525

## Important Links

Parameters 1-12 based on: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.563.1655&rep=rep1&type=pdf

Some code based on:
- https://realpython.com/python-speech-recognition/
- https://datascience.stackexchange.com/questions/26427/how-to-extract-question-s-from-document-with-nltk

Packages:
- Parselmouth (https://github.com/YannickJadoul/Parselmouth)
- NLTK (http://www.nltk.org/book/ch02.html#sec-extracting-text-from-corpora, http://www.nltk.org/book/ch06.html, http://www.nltk.org/howto/classify.html)
- SpaCy (https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)

Convert MP3 to wav:
- https://www.online-convert.com/result/60d91ab3-c873-407f-888f-719c1f4f5006
