import sys
import re
import os
import time
from pathlib import Path
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir) 
from tqdm import tqdm


def clean_line(line):
    punc1 = '''()[]{};:'"\|‘’<>`“”–+@#$=%^&*_~''' # for replacing with blank space not – is not - (the one here is an m dash)
    punc2 = '''/- …''' # for replacing with space (note " " is a hexidecimal space...)
    punc3 = '''!?.''' # end of sentence. Will remove all and add to end.
    nums = "1234567890"
    
    def clean_token(token):
        
        # change specified acronyms
        if token.lower() == "u.s.":
                    return "usa"
        if token.lower() == "art.":
            return "artificial"
        
        # begin character level analysis
        for character in token:
            # remove tokens containing numbers
            if character in nums:
                return ""
            # replace comma with a space. Sentences like this appear: "However,he was there"
            if character == ",":
                token = token.replace(character, " ")
            # remove punctuation in punc1
            if character in punc1: 
                token = token.replace(character, "")
            # split and recursively handle multi-word tokens
            if character in punc2 or (("..." in token) and (not token.endswith("..."))):
                token = token.replace(character, " ")
                innerAgg = ""
                for subToken in token.split():
                    innerAgg += clean_token(subToken) + " "
                return innerAgg[:-1]
            # change punctuation endings
            if character in punc3:
                token = token.replace(character, "")
        
        return token.lower()

    cleanLine = ""
    # remove non-ascii characters (hexadecimal)
    line = re.sub(r'[^\x00-\x7F]+','', line)
    # remove sentences containing links
    if "https" in line:
        return "-1"
    # clean tokens
    for token in line.split():
        cleanLine += clean_token(token) + " "
    # replace double spaces
    cleanLine = re.sub(r" +", " ", cleanLine)
    # remove spaces before periods.
    cleanLine = re.sub(r" +\.", ".", cleanLine)
    # eliminate single word sentences
    if len(cleanLine) <= 1:
        return "-1"
    # return sentence (final whitespace in sentence removed, period appended)
    else:
        return cleanLine[:-1] + "."


def main():

    start_time = time.time()
    count = 0
    agg = ""
    outfile = os.path.join(parentdir, "data", "clean_corpora", "indicorp_clean_large.txt")

    with open(os.path.join(parentdir, "data", "indicorp", "en", "en.txt")) as myfile:
        for line in myfile:
            cleanLine = clean_line(line) + " "
            if not cleanLine == "-1 ":
                agg += cleanLine + "\n"
                count += len(cleanLine.split())
            if time.time() - start_time > 15:
                start_time = time.time()
                print(f"{count} words")

    with open(outfile, "wt") as f:
        f.write(agg)

if __name__ == "__main__":

    start_time = time.time()
    print("Running script: clean.py")

    main()