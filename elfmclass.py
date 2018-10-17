#!/usr/bin/python3

import os
import subprocess as sp

# In each music directory, we convert all musics to .wav format
# We only convert those that haven't been converted yet

def toRaw():
    # Get file names
    files = sp.check_output(["ls"]).decode("utf8").strip().split("\n")

    # Get files that are already in wav format
    wav = []
    for f in files:
        parts = f.split(".")
        if parts[-1] == "wav":
            wav.append(''.join(parts[:-1]))

    # Get files that haven't been converted yet
    toConvert = []
    for f in files:
        parts = f.split(".")
        ext = parts[-1] # extension
        stem = ''.join(parts[:-1]) # filename without extension
        if ext != "wav" and stem not in wav:
            toConvert.append(f)

    print("Of all {} files, {} are already converted. We will convert {}.".format(
        len(files), len(files) - len(toConvert), len(toConvert))
        )

    # Convert files to wav
    for file in toConvert:
        stem = ''.join(file.split(".")[:-1])
        retval = sp.run(
            ["ffmpeg", "-i", file, "-ab", "160k",
             "-ac", "2", "-ar", "44100", "-vn", stem + ".wav"]
            ).returncode
        if(retval != 0):
            print("Sorry, could not convert file '{}', so we will ignore it for now.".format(file))

try:
    os.chdir("./music_negative/")
except:
    print("Couldn't chdir. We are on dir: " + os.getcwd())

toRaw()

os.chdir("..")
try:
    os.chdir("./music_positive/")
except:
    print("Couldn't chdir. We are on dir: " + os.getcwd())

toRaw()

os.chdir("..")

