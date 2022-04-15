# Run with "python <path_to_file> <"i" for indicorp or "n" for nantec> <minimum count needed to represent word as vec>

from gensim.models import Word2Vec
import os, sys
from pathlib import Path
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
import argparse

def create_sentences(text, key):

    if key == "n":
        sents = text.split(".")
        # removes spaces at beginning and ends of sentences. Only uses sentences of length > 1/
        sents = [sent.strip() for sent in sents if len(sent) > 1]
        tokenized_sents = [x.split(" ") for x in sents]
        return tokenized_sents

    elif key == "i":
        sents = text.split("\n")
        # removes spaces and periods at beginning and end of sentences. Only use sentences of length > 1
        sents = [sent.strip(". ") for sent in sents if len(sent) > 1]
        tokenized_sents = [x.split(" ") for x in sents]
        return tokenized_sents

    else:
        sys.exit("Invalid key. Use \"nantec\" or \"indicorp\"")


def train_w2v(text, count, name, output_path, key):

    sentences = create_sentences(text, key)

    model = Word2Vec(sentences=sentences, min_count=count, sg=1, vector_size=200)
    model.save(os.path.join(output_path, name+".bin"))
    #model.save(text.split("/")[-1]+".model")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("key") # 'n' for NANTeC or 'i' for Indicorp
    parser.add_argument("min_count") # minimum number word occurrences in a corpus 
    args = parser.parse_args()
 
    key = args.key
    min_count = args.min_count
    
    inputf = ""
    if key == "i":
        inputf = os.path.join(parentdir, "data", "clean_corpora", "indicorp_clean.txt")
    elif key == "n":
        inputf = os.path.join(parentdir, "data", "clean_corpora", "NANTeC_clean.txt")
    else:
        sys.exit("Invalid key. Use \"i\" for indicorp or \"n\" for NANTeC")
    
    output_path = os.path.join(parentdir, "models")

    with open(inputf) as file:
        text = file.read()

    name = inputf.split("/")[-1][:-4]
    train_w2v(text, int(min_count), name, output_path, key)
    
        
if __name__ == "__main__":

    main()


















