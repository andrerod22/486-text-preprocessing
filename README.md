# Information Retrieval Project

## Overview
This project focuses on text preprocessing for information retrieval tasks. It provides functionalities to preprocess text data, including removing SGML tags, tokenizing text, removing stopwords, stemming words, and generating word frequency statistics. Additionally, it includes a language identification module using bigram language models.

## Purpose
The purpose of this project is to prepare text data for information retrieval tasks such as document indexing, search, and analysis. By preprocessing the text and identifying the language of documents, we aim to improve the efficiency and effectiveness of information retrieval algorithms.

## Features
- **SGML Tag Removal:** Removes SGML tags from input text.
- **Tokenization:** Splits text into tokens while handling punctuation and special cases.
- **Stopword Removal:** Filters out common stopwords from the text.
- **Stemming:** Reduces words to their root form using the Porter stemming algorithm.
- **Word Frequency Analysis:** Generates word frequency statistics for the preprocessed text.
- **Language Identification:** Identifies the language of documents using bigram language models.

## How to Use
1. **Clone the Repository:** Clone this repository to your local machine.
2. **Install Dependencies:** Ensure you have Python installed. No additional dependencies are required.
3. **Run the Script:** Execute the `preprocess.py` or `languageIdentification.py` script and provide the necessary input files or directories.
4. **View Output:** The script will generate output files containing the results of preprocessing or language identification. From the cranfield documents I used for this project, I reached an accurarcy of 98%.

## Contribution
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- The Porter stemming algorithm implementation is adapted from [this source](link-to-source).
- Special thanks to [contributors' names] for their contributions to this project.

## Contact
For any inquiries or questions, please contact [your email address].
