import re
import time
import os, sys
import gzip
from pathlib import Path
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir) 


def extractFileData(file_text):

    punc1 = '''()[]{};:'"\|‘’<>`“”–+@#$=%^&*_~''' # for replacing with blank space not – is not - (the one here is an m dash)
    punc2 = '''/-…''' # for replacing with space
    punc3 = '''!?''' # end of sentence. Replace with periood
    nums = "1234567890"

    def clean_token(token):
        # begin character level analysis
        for character in token:
            # remove numbers
            if character in nums:
                if token.endswith("."):
                    return "."
                else:
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
                agg = ""
                for subToken in token.split():
                    agg += clean_token(subToken) + " "
                return agg
            # change punctuation endings
            if character in punc3:
                token = token.replace(character, ".")
        
        # remove specific tokens
        if token == "..." or token == "&MD;" or token == ".":
            return ""
        # remove abbreviations
        if "." in token:
            if token.lower() in abbreviations:
                token = token.replace(".", "")
                token = token.lower()
                if token == "us":
                    return "usa"
                if token == "art":
                    return "artificial"
                return token
            elif token.lower()[:-1] in abbreviations:
                token = token.replace(".", "")
                token = token.lower()
                if token == "uss":
                    return "usas"
                return token
        # removes accronyms such as r.j. or l.a. 
        if len(token) == 4:
            token = token.lower()
            if token[1] == "." and token[3] == ".":
                return token[0] + token[2]
        
        # replace sentences ending in 2 periods with one
        if token.endswith(".."):
            token = token.replace(".", "")
        return token.lower()

    paragraph_capture = "(?<=<p>\s)(.*?)(?=\s<p>)" # captures text between paragraphs
    data = re.findall(paragraph_capture, file_text, re.DOTALL) # list of phrases (things in between <p> tags)
    data = [x for x in data if (not "<" in x) and (not "&UR;" in x)] # removes phrases with nested tags or that contain &UR;
    data = " ".join(data)
    data = data.split() # splits into individual tokens
    clean_data = ""
    for token in data:
        clean_data += clean_token(token) + " "
    
    clean_data = re.sub('(?<=(\. ))(\w+\.)(?=\s)', "", clean_data) # removes single word sentences
    clean_data = re.sub('\.+ \.', ". ", clean_data) # removes null sentences. .Like this
    clean_data = re.sub(' +', ' ', clean_data) # removes multiple spaces
    return clean_data

def main():

    count = 0

    #import abbreviation words
    with open(os.path.join("data", "abbreviations.txt"), "rt") as f:
        global abbreviations 
        abbreviations = f.read().splitlines()
    # define paths and directory names
    if not os.path.isdir(os.path.join(parentdir, "data", "output")):
        os.mkdir(os.path.join(parentdir, "data", "output"))
    news_outlets = ["latwp", "nyt", "reuff", "reute", "wsj"]
	
    for outlet in news_outlets:
        outlet_dir = os.path.join(parentdir, "data", "NANTeC", outlet)

        i = 1 
        agg = ""
        for year_dir in os.listdir(outlet_dir):
            if year_dir[:3] == "199":
                year_dir = os.path.join(outlet_dir, year_dir)
                print(year_dir)
                for filename in os.listdir(year_dir):
                    if filename.endswith(".gz"):
                        count += 1
                        with gzip.open(os.path.join(year_dir, filename), mode = "rt", encoding="ISO-8859-1") as f:
                            file_text = f.read()
                            data = extractFileData(file_text)
                            agg += data

    with open(os.path.join("data", "clean_corpora", "NANTeC_clean.txt"), "wt") as f:
        f.write(agg)
    print(f"Ran in {round((time.time() - start_time), 2)} seconds.")
    print(count)

if __name__ == "__main__":

    start_time = time.time()
    print("Running script: clean.py")

    main()