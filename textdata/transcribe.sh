#!/usr/bin/env bash

# make folders for files/transcripts
folder="../audiofiles/sentdata/$1/"
mkdir -p "$folder"

folder="../audiofiles/sentdata/$1/splitfiles/"
mkdir -p "$folder"

folder="../audiofiles/sentdata/$1/transcripts/"
mkdir -p "$folder"

# split audio into 1 minute increments
echo "splitting files"

output=$(python3 ../audiofiles/splitaudio.py $1)

echo "done splitting"

# transcribe split files
filename="../audiofiles/sentdata/$1/splitfiles/$1-part"
num=$(ls -1 "../audiofiles/sentdata/$1/splitfiles/" | wc -l)

for i in `seq 1 $num`;
do
    echo "transcribing: $filename$i.wav"

    # echo tofile: ../audiofiles/transcripts/17-1594-part$i.json
    output=$(python3 transcribe.py $filename$i.wav $i)
    # echo $output >> sents.csv
done

echo "done transcribing"

echo "concatting files"

output=$(python3 concatfiles.py "$filename")

echo "done with file $1.wav"
