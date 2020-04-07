# CS 5293, Spring 2020 Project 1

###### The Redactor

###### Ana Marple

## Intro
-----------
This program allows the user to redact certain content from .txt documents to protect potentially sensitive information. Different **redaction flags** can be implemented to redact entity types of the user's choice. The following flags are **optional**:

* ```--names```
* ```--genders```
* ```--dates```
* ```--concept```
* ```--numbers```
* ```--locations```

The user must direct the program where to find the .txt files, and where to output the resulting .redacted files. Therefore, the following flags are **required**:

* ```--input```
* ```--output```

Additionally, statistics of the redacted file(s) can be generated to the same location indicated by the ```--output``` flag, resulting in files with the .stats extension. This flag is **optional**, but insightful: 

* ```--stats```

## Installation
----------------
1. Install the package
```bash
pip install project1
```
2. Go into the shell
```bash
pipenv shell
```
3. Make sure neccessary packages are downloaded
```bash
python setup.py install
```
Note: Python 3.7 was used in the making of this program.

## Folder Structure
----------------------
Below is the tree structure for this project. The main module is redactor.py, which contains all of the neccessary functions.

```
├── COLLABORATORS
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── build
│   ├── bdist.linux-x86_64
│   └── lib
│       └── project1
│           ├── __init__.py
│           └── redactor.py
├── dist
│   └── project1-1.0-py3.7.egg
├── docs
│   ├── file01.txt
│   ├── file02.txt
│   ├── file03.txt
│   ├── file04.txt
│   ├── file05.txt
│   └── test.txt
├── otherfiles
│   ├── file01.txt.redacted
│   ├── file01.txt.stats
│   ├── file02.txt.redacted
│   ├── file02.txt.stats
│   ├── file03.txt.redacted
│   ├── file03.txt.stats
│   ├── file04.txt.redacted
│   ├── file04.txt.stats
│   ├── file05.txt.redacted
│   ├── file05.txt.stats
│   └── test.txt.stats
├── project1
│   ├── __init__.py
│   └── redactor.py
├── project1.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── requirements.txt
├── setup.cfg
├── setup.py
└── tests
    ├── test_concepts.py
    ├── test_dates.py
    ├── test_genders.py
    ├── test_locations.py
    ├── test_names.py
    ├── test_numbers.py
    └── test_stats.py
```

For example, the files in the ```docs/``` folder were used to create and test the program. The input command was ```--input '*.txt'``` (the program was written assuming the input files would be located in the ```docs/``` folder). The output location was specified as ```otherfiles/```, resulting in the .redacted files in said folder. Additionally, ```--stats``` was flagged which resulted in the .stats files in said location, as  well.

### Usage
------------
The command used to execute the program was:
```bash
	pipenv run python project1/redactor.py 
	--input '*.txt' 
	--genders --names --dates
	--locations --numbers
	--concept children jail
	--stats 
	--output 'otherfiles/'
```

#### Notes:
1. Flags can be listed in any order.
2. The only required flags are ```--input``` and ```--output```.
3. There can be **multiple concepts**. List the flag once, followed by each desired concept to redact **separated by a whitespace**, as shown in the command above.


## Required Flags
-------------------

### Input
The ```--input '*.txt'``` command specifies the location/name/type of file to be redacted. In this program, the files to be redacted are assumed to be **only** .txt files and located in the ```docs/``` folder. If there are multiple .txt files in the location, all will be read by the glob.

### Output
The ```--output 'otherfiles/'``` command specifies the location/name/type of the redacted file to be placed. Each file output will have the .redacted extention. Each of the .redacted files will contain the text, but redacted using the unicode full block character to cover sensitive text.


## Redaction Flags
--------------------

### Names
The ```--names``` flag triggers the redact_names function:
```python 
def redact_names(contents):
```
The parameter takes in the text and returns the redacted text, the list of names redacted, and the number of words in the document. First, the text was tokenized into sentences using the Natural Language Toolkit's (NLTK)```nltk.sent_tokenize``` method. Then, each sentence was further tokenized into words using the WhitespaceTokenizer. Again using nltk, each word was categorized using Parts of Speech (POS) tagging. Those were that were tagged as 'NNP' (Proper nouns) were added to the redaction list. The redact_items function was then called (as it is in every function listed below):
```python def redact_items(red_list, contents):```
This function takes in the list of words to redact and the text, and returns the text with the 'red_list' words replaced by the unicode full block character.

### Genders:
The ```--genders``` flag triggers the redact_gender function:
```python
def redact_gender(contents):
```
The parameter takes in the text and returns the redacted text and the list of gender-related words redacted. The list of gender-related words decided was:
```python 
genders = ['he', "hes", 'her', 'she', "shes", 'him', 'his', 'woman', 'man', 'lady', 'ladies',  'girl', 'boy', 'women', 'men', 'son', "son's", 'daughter', "daughters", 'father', "fathers", 'mother', 'sister','brother', 'herself', 'himself', "mothers", 'female', 'male']
```
The text was tokenized into sentences using the NLTK sentence tokenization method. Then, each sentence was further tokenized into words using the WhitespaceTokenizer. Each word was stripped of ascii characters so that all of the puncuation could be stripped. The word was made all lowercase using .casefold() and then was compared to each of the gendered words in the list. If it matched the word was added to the redaction list and the redact_items function was called.

### Dates
The ```--dates``` flag triggers the redact_dates function:
```python 
def redact_dates(contents):
```
The parameter takes in the text and returns the redacted text and the list of date-related words redacted. In my opinion, this was the most difficult function because of the punctuation and various formats of dates. I tried to redact anything that:
* Was tagged as a date by the search_dates methods from the dateparser.search package
* Was In the 'months' list (which helf days of the week and months)
* Matched the following formats: HH:MM | YYYY | MM, YYYY | MM(st, nd, rd, th) YYYY
These were added to one large 'dates' list.
The text was tokenized into sentences using the NLTK sentence tokenization method. Then, each sentence was further tokenized into words using the WhitespaceTokenizer. The program ran through each word to see if it contained any words from the 'dates' list.
If so, the word was added to the redaction list. Then the redat_items function was called.

### Numbers
The ```--numbers``` flag triggers the redact_numbers function:
```python
def redact_numbers(contents):
```
The parameter takes in the text and returns the redacted text and the list of number-related words redacted. The text was tokenized into sentences using the NLTK sentence tokenization method. Then, each sentence was further tokenized into words using the WhitespaceTokenizer. The program ran through each word to see if it contained any words from the 'numbers' list:
```python  
numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'teen', 'twenty', 'thirty', 'forty', 'fifty', 'hundred', 'thousand', 'million']
```
If so, the word was added to the redaction list. Then, regular expressions was used to find all of the words containing digits, and was added to the redaction list. Then the redat_items function was called.

### Locations
The ```--locations``` flag triggers the redact_loc function:
```python 
def redact_loc(contents):
```
The parameter takes in the text and returns the redacted text and the list of location-related words redacted. First, the text was tokenized into sentences using the NLTK sentence tokenization method. Then, each sentence was further tokenized into words using the WhitespaceTokenizer. Using spacy's ```nlp``` package, each word was categorized as a type of entity. Those were that were tagged as 'GPE' (Geopolitical entity) were added to the redaction list. The redact_items function was then called.

### Concept
The ```--concept`` flag triggers the redact_concepts function:
```python 
def redact_concepts(contents, concepts):
```
The parameters takes in the text and list of concepts and returns the redacted text and the list of words redacted. This function cycled through each concept word and added the synonyms of each to a list using ```wordnet``` from ```nltk.corpus```. The text was tokenized into sentences using the NLTK sentence tokenization method. Then, each sentence was further tokenized into words using the WhitespaceTokenizer. The program ran through each word to see if it contained any words from the 'synonyms' list. If so, every word from that **sentence** was added to the redaction list. Then the redat_items function was called.


## Stats
----------
The ```--stats``` flag generates a .stats file that contains the total number of words in the document (separated by whitespace), the number of words redacted for each flag, as well as the words that were redacted for that flag category. An example can be seen below:

```
***Stats for File: docs/file02.txt***
Total Number of Words (Separated by Whitespace): 471

***Number of Names Redacted: 49
Florida, Thursday., Tonya, Ethridge, McKinley,, New, Year's, Eve, Pensacola,, Daniel, Leonard, Wells,, Renee, McCall,, NBC, News, Thursday., Darryl's, Bar, Grille,, McKinley, Jan., McKinley,, Thursday., DNA, McKinley's, Wells', Wells, March, Police, DNA, Tonya, Wells', DNA, Pensacola, Mike, Wood, Tonya's, Tonya., Wells, Escambia, County, Jail, Wednesday, Wells, Wood, Thursday., McCall, McCall

***Number of Gendered Words Redacted: 23
man, mother, she, sister,, son., boy, mother,, daughter, him,, he, his, her, her, he, He, she's, her, her, his, daughter's, him., She, his

***Number of Date-Related Words Redacted: 9
23,, 1,, 1985., today., may, may, may, may, 1985

***Number of Number-Related Words Redacted: 8
35, 57,, 62,, 35, 18-month-old, 4, 35-year, one

***Number of Locations Redacted: 0

***Number of Concept-Related Words Redacted: 0
```

The stats flag signals the get_stats function:
```python 
def get_stats(fileName, outputLoc, stats_, no_words):
```
The parameters are the name of the file whose stats are being processed, the output location to place the .stats file, the stats list from the main function, and the number of words (separated by whitespace) in the file.


## Testing
------------
There are seven tests to diagnose the program, all located in the ```tests/``` folder. There is a 'test_concepts.py' to test that more than one concept can be added and that the **whole sentence** containing the synonyms will be redacted. The 'test_dates.py' checks if days of the week, years, months, and days are redacted. The 'test_genders.py' checks if any of the words are in the gender list as described earlier and redacts them. The 'test_names.py' tests that all proper nouns are redacted. The 'test_locations.py' makes sure 'GPE' spacy-tagged words are redacted. The 'test_number.py' checks that all words containing or describing digits are redacted and the 'test_stats.py' tests the output of the statistics function.

Command to run pytest:
```bash
pytest -p no:warnings -s
```


#### File Sources
------
1. File01.txt: https://nypost.com/2020/03/21/inside-the-double-life-of-a-nyc-preacher-charged-in-cold-case-murder/
2. File02.txt: https://www.nbcnews.com/news/us-news/florida-man-arrested-35-year-old-cold-case-murder-thanks-n1164051
3. File03.txt: https://www.woodtv.com/news/michigan/murder-charge-filed-in-1983-white-cloud-cold-case/
4. File04.txt: https://www.crimescene.com/file-elvis/2724-elvis-incident-rpt
5. File05.txt: https://famous-trials.com/sam-sheppard/8-reports

#### References
------
https://github.com/vishnuvikash/Redactor-Unredactor/blob/master/redactor/redactor.py
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
https://spacy.io/usage/linguistic-features#pos-tagging
https://blog.xrds.acm.org/2017/07/power-wordnet-use-python/
https://machinelearningmastery.com/clean-text-machine-learning-python/


