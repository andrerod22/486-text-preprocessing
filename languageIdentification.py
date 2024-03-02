# Andre Rodriguez
# andrerod

import pdb
import sys
import re
import math
from collections import defaultdict
from collections import Counter
from pathlib import Path
from itertools import chain



def default_value():
    return 1

def trainBigramLanguageModel(text_file):
    """Training Function."""
    c_freq = defaultdict(default_value)
    b_freq = defaultdict(default_value)
    
    # Char Freq
    c_freq = Counter(text_file[idx] for idx in range(len(text_file) - 1))
    #c_freq = sorted(c_freq)

    # Bigram Freq
    b_freq = Counter(text_file[idx : idx + 2] for idx in range(len(text_file) - 1))
    # b_freq = sorted(b_freq)
    # breakpoint()
    trained_language = {
        'c-freq': c_freq,
        'b-freq': b_freq
    }
    return trained_language

def identifyLanguage(line, language_freqs):
    """Verifies language."""
    candidates = defaultdict(default_value)
    for l in language_freqs.keys():
        probability = 1
        for word in line:
            probability = 1
            next_letter = 1
            for char in word:
                s = char
                b = char + word[next_letter] if next_letter < len(word) else None
                single_char = language_freqs[l]['c-freq'][s] if s in language_freqs[l]['c-freq'] else 0
                double_char = language_freqs[l]['b-freq'][b] if b in language_freqs[l]['b-freq'] else 0
                next_letter += 1
                probability *= (double_char + 1) / (single_char + len(language_freqs[l]['c-freq']))
            candidates[l] *= math.sqrt(probability)
    return max(candidates, key=candidates.get)



def main():
    """Main driver for language identification"""
    # Open the training data:
    input_path = Path(sys.argv[1])
    training_folder = input_path / "training/"
    language_files = [language for language in training_folder.iterdir() if language.is_file()]
    languages = [str(name)[str(name).rfind('/') + 1:] for name in language_files]
    language_freqs = dict(list())
    l = 0
    # Begin training models for each language:
    for file in language_files:
        str_text = open(str(file), 'r', encoding='latin1').read()
        language_freqs[languages[l]] = trainBigramLanguageModel(str_text)
        l += 1

    # Determine Best language for each file: 
    test_file = input_path / "test"
    extracted_text = open(str(test_file), 'r', encoding='latin1').read()
    
    # Write to languageIdentification.out:
    with open('languageIdentification.output', 'w') as f:
        lot = 1
        extracted_text = extracted_text.split('\n')
        for et in extracted_text:
            # EOF
            if len(et) == 0: break
            proposed_language = identifyLanguage(et.split(), language_freqs)
            f.write(str(lot) + " " + proposed_language + "\n")
            lot += 1

if __name__ == "__main__":
    main()
