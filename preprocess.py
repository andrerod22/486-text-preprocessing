# Andre Rodriguez
# andrerod

"""Title: text-preprocessing."""
import sys
import pdb
import re
from pathlib import Path
from porterStemmer import PorterStemmer
from collections import defaultdict
from itertools import chain

def default_value():
    return 1

def removeSGML(text):
    """Removes SGML tags from a given cranfield file."""
    filter = re.compile('<.*?>')
    return re.sub(filter, '', text)


def countCommas(word):
    """Counts Commas."""
    comma_count = 0
    for w in word:
        comma_count += 1 if w == ',' else comma_count
    return comma_count

def countPeriods(word):
    """Counts Periods."""
    period_count = 0
    for w in word:
        period_count += 1 if w == '.' else period_count
    return period_count

def investigatePeriod(word):
    """Checks if this is an abbreviation or acronym with one period"""
    # Abbreviation (period should be at the end) 
    if word[-1] != '.':
        return True
    
    # Sentence
    else:
        # Check if the word is in this general abbreviation table:
        general_abbreviations = [
            'dr.',
            'hon.',
            'mr.',
            'mrs.',
            'ms.',
            'prof.',
            'sr.',
            'jr.',
            'ave.',
            'dept.',
            'est.',
            'fig.',
            'hrs.',
            'obj.'
        ]
        lowered_word = word.lower()
        return True if lowered_word in general_abbreviations else False

def tokenizeText(text):
    """Seperates non-integral punctuation from words."""
    res = []
    for t in text:
        # if t == 'temperature': breakpoint()
        # Check for closed phrase ( word ):
        if len(t) > 2 and t[0] == '(' and t[-1] == ')':
            t = t[1:-1]
        
        # Check for phrase ( word : 
        elif t[0] == '(' and len(t) > 1 and t[-1] != ')':
            t = t[1:]
        
        # Check for phrase word ): 
        elif t[0] != '(' and len(t) > 1 and t[-1] == ')':
            t = t[:-1]

        # Check if comma in word:
        if ',' in t:
            if t == ',':
                res.append(t)
                continue
            commas = countCommas(t)
            if commas > 1:
                res.append(t)
            elif t[-1] == ',':
                res = res + [t[:-1],t[-1]]

        # Check if period in word:
        elif '.' in t:
            if t == '.':
                res.append(t)
                continue
            periods = countPeriods(t)
            if periods > 1:
                res.append(t)
                continue
            elif investigatePeriod(t):
                res.append(t)
                continue
            else:
                res = res + [t[:-1],t[-1]]
            
        # Check for apostrophe
        elif "'" in t:
            # Specific Cases
            if t.lower() == "i'm":
                res = res + ["I", "am"]
            elif t.lower() == "you're":
                res = res + ["You", "are"]
            elif t.lower() == "they're":
                res = res + ["They", "are"]
            elif t.lower() == "we're":
                res = res + ["We", "are"]
            elif t.lower() == "i'll":
                res = res + ["I", "will"]
            elif t.lower() == "we'll":
                res = res + ["We", "will"]
            elif t.lower() == "you'll":
                res = res + ["You", "will"]
            elif t.lower() == "he'll":
                res = res + ["He", "will"]
            elif t.lower() == "she'll":
                res = res + ["She", "will"]
            elif t.lower() == "they'll":
                res = res + ["They", "will"]
            elif t.lower() == "it'll":
                res = res + ["It", "will"]
            elif t.lower() == "don't":
                res = res + ["Do", "not"]
            elif t.lower() == "won't":
                res = res + ["Would", "not"]
            elif t.lower() == "can't":
                res = res + ["Can", "not"]
            elif t.lower() == "wasn't":
                res = res + ["Was", "not"]
            elif t.lower() == "isn't":
                res = res + ["Is", "not"]
            elif t.lower() == "i've":
                res = res + ["I", "have"]
            elif t.lower() == "could've":
                res = res + ["Could", "have"]
            elif t.lower() == "should've":
                res = res + ["Should", "have"] 
            elif t.lower() == "would've":
                res = res + ["Would", "have"]
            elif t.lower() == "he's":
                res = res + ["He", "is"]
            elif t.lower() == "she's":
                res = res + ["She", "is"]
            elif t.lower() == "it's":
                res = res + ["It", "is"]
            
            # Posessive Case:
            elif t[-1] == "'":
                res = res + [t[:-1], t[-1]]
            elif t[-1] == "s":
                res = res + [t[:-2], t[-2]]
        
        elif not all(bool(re.search(r"\s", x)) for x in t):
            res.append(t)
    return res
            

def removeStopWords(tokens, stopwords):
    """Removes stopwords."""
    return [token for token in tokens if token not in stopwords]

def stemWords(tokens):
    """Stems words using public porterstemmer."""
    res = []
    public_porter = PorterStemmer()
    for t in tokens:
        if "'" not in t and '.' not in t and ',' not in t and not t.isnumeric():
        #if t != "'" and t != '.' and t != ',' and t != '':
            res.append(public_porter.stem(t, 0, len(t) - 1))
    return res

def main():
    """Main driver for text-preprocessing."""
    # Read input directory and stopwords:
    input_path = Path(sys.argv[1])
    docs = [doc for doc in input_path.iterdir() if doc.is_file()]
    with open("stopwords", 'r') as input:
        stopwords = [line.replace('\n', '') for line in input]
    
    # Setup dictionary:
    word_count = 0
    word_freq = defaultdict(default_value)
    # Format document text and extract tokens:
    for doc in docs:
        raw = str()
        # breakpoint()
        # raw = open(doc, 'r').read()
        with open(doc, 'r', encoding='UTF-8') as read:
            for line in read:
                raw = raw + line
        if not raw: continue
        formatted_text = removeSGML(raw)
        text_list = formatted_text.split('\n')
        while '' in text_list:
            text_list.remove('')
        formatted_list = [text.split() for text in text_list]
        formatted_list2 = list(map(str, chain.from_iterable(formatted_list)))        
        extracted_tokens = tokenizeText(formatted_list2)
        extracted_tokens = removeStopWords(extracted_tokens, stopwords)
        extracted_tokens = stemWords(extracted_tokens)

        word_count += len(extracted_tokens)
        # Build Token Dictionary and reverse the order:
        for token in extracted_tokens:
            word_freq[token] += 1
    word_freq = {a: b for a, b in sorted(word_freq.items(), key=lambda item: item[1], reverse=True)}

    # Write to file output:
    with open("preprocess.output", "w", encoding='UTF-8') as w:
        w.write("Words " + str(word_count) + "\n" + "Vocabulary " + str(len(word_freq)) + "\n" + "Top 50 words\n")
        count = 0
        for word, freq in word_freq.items():
            if count == 50: break
            w.write(word + " " + str(freq) + "\n")
            count += 1
    
    # Unique Words in 25% Cranfield Collection 
    sum = 0
    unique_words = 0
    fourth_of_collection = word_count * 0.25
    for freq in word_freq.values():
        if sum > fourth_of_collection: break
        sum += freq
        unique_words += 1

    print("\nUnique Words in 25% of collection: " + str(unique_words))
    print("End of preprocess.py")

if __name__ == "__main__":
    main()
