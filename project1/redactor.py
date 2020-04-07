import argparse
import glob
import nltk
from nltk import pos_tag, sent_tokenize, WhitespaceTokenizer
import unicodedata
import string
import spacy


###################################################################################
#Takes the input, reads the files, and outputs redacted files to specified location
def main(input_, output_, names_, genders_, dates_, concept_, numbers_, locations_, stats_):

    files = glob.glob('docs/' + input_)
    #Goes through each file in glob
    for file in files:
    
        print('************************************************** ' + file + ':\n')        
        #Opens file, reads content of file, then closes file
        file_o = open(file, 'r')
        contents =  file_o.read()
        file_o.close()
        
        #List to hold redacted words
        stats = []
        #List that holds concept(s) to redact
        concepts = concept_
        
        '''Get number of words in file'''
        text = redact_names(contents)
        no_words = text[2]
        text = contents

        '''Redact Names'''
        if(names_):
            #Add redacted names to list
            text = redact_names(contents)
            names = text[1]
            stats.append(names)
            text = text[0]
        else:
            stats.append('')

        '''Redact Genders'''
        if(genders_):
            text = redact_gender(text)
            #Adds redacted 'gendered' words to list
            gendered = text[1]
            stats.append(gendered)
            text = text[0]
        else:
            stats.append('')

        '''Redact Concept(s)'''
        if(concept_):
            text = redact_concepts(text, concepts)
            #Adds redacted synonyms of concept(s) to list
            syns = text[1]
            stats.append(syns)
            text = text[0]
        else:
            stats.append('')

        '''Redact Dates'''
        if(dates_):
            text = redact_dates(text)
            #Adds redacted date terms to list
            dates = text[1]
            stats.append(dates)
            text = text[0]
        else:
            stats.append('')
        
        '''Redact Numbers'''
        if(numbers_):
            text = redact_numbers(text)
            #Adds redacted numbers to list
            numbers = text[1]
            stats.append(numbers)
            text = text[0]
        else:
            stats.append('')
        

        '''Redact Locations'''
        if(locations_):
            text = redact_loc(text)
            #Adds redacted locations to list
            locs = text[1]
            stats.append(locs)
            text = text[0]
        else:
            stats.append('')

        print(text)
        if(stats_):
            stats = get_stats(file, output_, stats, no_words)         
        

        #Writes redacted file to given output location
        new_file = file.replace('docs/', output_)
        f = open(new_file + '.redacted', 'w+')
        f.write(text)
        f.close()


##################################################################################
#Writes number of words redacted/which words are redacted for each category
def get_stats(fileName, outputLoc, stats_, no_words):
    
    #Write stats to specified output location
    new_file = fileName.replace('docs/', outputLoc)
    f = open(new_file + '.stats', 'w+')

    print('Stats for File: ' + fileName + '\n')
    print('Total Number of Words (Separated by Whitespace): ' + str(no_words) + '\n')
    f.write('***Stats for File: ' + fileName + '***\n\n')
    f.write('Total Number of Words (Separated by Whitespace): ' + str(no_words) + '\n\n\n')


    names = len(stats_[0])
    print('Number of Names Redacted: ' + str(len(stats_[0])))
    print((', '.join(stats_[0])) + '\n')
    f.write('***Number of Names Redacted: ' + str(len(stats_[0])) + '\n\n')
    f.write((', '.join(stats_[0])) + '\n\n\n')

    genders = len(stats_[1])
    print('Number of Gendered Words Redacted: ' + str(len(stats_[1])))
    print((', '.join(stats_[1]))+ '\n')
    f.write('***Number of Gendered Words Redacted: ' + str(len(stats_[1])) + '\n\n')
    f.write((', '.join(stats_[1])) + '\n\n\n')

    dates = len(stats_[3])
    print('Number of Date-Related Words Redacted: ' + str(len(stats_[3])))
    print((', '.join(stats_[3])) + '\n')
    f.write('***Number of Date-Related Words Redacted: ' + str(len(stats_[3])) + '\n\n')
    f.write((', '.join(stats_[3])) + '\n\n\n')

    numbers = len(stats_[4])
    print('Number of Number-Related Words Redacted: ' + str(len(stats_[4])))
    print((', '.join(stats_[4])) + '\n')
    f.write('***Number of Number-Related Words Redacted: ' + str(len(stats_[4])) + '\n\n')
    f.write((', '.join(stats_[4])) + '\n\n\n')
 
    locations = len(stats_[5])
    print('Number of Locations Redacted: ' + str(len(stats_[5])))
    print((', '.join(stats_[5])) + '\n')
    f.write('***Number of Locations Redacted: ' + str(len(stats_[5])) + '\n\n')
    f.write((', '.join(stats_[5])) + '\n\n\n')

    concepts = len(stats_[2])
    print('Number of Concept-Related Words Redacted: ' + str(len(stats_[2])))
    print((', '.join(stats_[2])) + '\n')
    f.write('***Number of Concept-Related Words Redacted: ' + str(len(stats_[2])) + '\n\n')
    f.write((', '.join(stats_[2])) + '\n')

    f.close()
    return(names, genders, dates, numbers, locations, concepts)


##################################################################################
#Redacts given list of items from given text
def redact_items(red_list, contents):

    redacted = [] #list to return, holds redacted text
    
    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)
    
    for sentence in sentences:
        #Tokenize sentence into words
        ws = WhitespaceTokenizer()
        words = ws.tokenize(sentence)
        
        #Goes through each word to see if it's in the redaction list
        for word in words:
            #Redact word
            if(word in red_list):
                r = '\u2588' * len(word)
                redacted.append(r)
            else:
                redacted.append(word)
    
    redacted = (' '.join(redacted))
    return(redacted)


#################################################################################
#Redacts NNP (Proper nouns aka names)
def redact_names(contents):
 
    redacted = [] #list to return, holds redacted text
    nnp = [] #list to hold proper nouns
    redact = [] #list that holds words to redact

    no_words = 0

    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)
    
    for sentence in sentences:
        #Tokenize sentence into words, tag words' pos
        ws = WhitespaceTokenizer()
        words = ws.tokenize(sentence)
        tagged = nltk.pos_tag(words)

        #Goes through each word to see if it's an NNP
        for word,tag in tagged:
            #If an NNP, add to nnp list
            if(tag == 'NNP'):
                nnp.append(word)
        
        #Checks words to see if any are/contain NNP words
        for word in words:
            i = 0
            no_words = no_words + 1
            while i < len(nnp):
                if(nnp[i] in word):
                    redact.append(word)
                    break
                else:
                    i = i + 1

    redacted = redact_items(redact, contents)
    return(redacted, redact, no_words)


#################################################################################
#Redacts gender
def redact_gender(contents):

    #List of gendered words
    genders = ['he', "hes", 'her', 'she', "shes", 'him', 'his', 'woman', 'man', 'lady', 'ladies',  'girl', 'boy', 'women', 'men', 'son', "son's", 'daughter', "daughters", 'father', "fathers", 'mother', 'sister','brother', 'herself', 'himself', "mothers", 'female', 'male']

    redacted = [] #list to return, holds redacted tex
    redact = [] #list that holds words to redact

    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)

    for sentence in sentences:
        #Tokenize sentence into words
        ws = WhitespaceTokenizer()
        words = ws.tokenize(sentence)
        
        #Ignores upper/lower case and punction marks
        for word in words:
            w = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf8') 
            if((w.translate(str.maketrans('','', string.punctuation)).casefold() in genders)):
                redact.append(word)

    redacted = redact_items(redact, contents)
    return(redacted, redact)


#################################################################################
#Redacts numbers (numeric and spelled out)
def redact_numbers(contents):
    
    #List of numbers (spelled out)
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'teen', 'twenty', 'thirty', 'forty', 'fifty', 'hundred', 'thousand', 'million']
    
    redacted = [] #list to return, holds redacted tex
    redact = [] #list that holds words to redact
    
    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)
    
    for sentence in sentences:
        #Tokenize sentence into words
        ws = WhitespaceTokenizer()
        words = ws.tokenize(sentence)
        
        #Ignores upper/lower case and punction marks
        for word in words:
            i = 0
            while i < len(numbers):
                if(numbers[i] in word.casefold()):
                    redact.append(word)
                    break
                else:
                    i = i + 1
            
            #searches for digits in each word
            digits = re.findall(r'\d+', word)
            if digits:
                redact.append(word)
    
    redacted = redact_items(redact, contents)
    return(redacted, redact)


#################################################################################
# Redacts words relating to concept(s)
from nltk.corpus import wordnet
def redact_concepts(contents, concepts):

    synonyms = [] #will hold list of synonyms
    redacted = [] #return this; will hold redacted text
    redact = [] #holds list of words to redact
    
    #Makes list of synonyms of concept(s)
    for i in concepts:
        for syn in wordnet.synsets(i):
            for l in syn.lemma_names():
                synonyms.append(l)
    
    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)
    
    for sentence in sentences:
        #Tokenize sentence into words
        ws = WhitespaceTokenizer()
        words = ws.tokenize(sentence)
       
        has_syn = 0
        #Checks words to see if any are/contain the synonyms
        for word in words:
            i = 0
            while i < len(synonyms):
                if(synonyms[i] in word.casefold()):
                    has_syn = 1
                    break
                else:
                    i = i + 1

        #If so, all words in sentence are to be redacted
        if(has_syn == 1):
            for word in words:
                redact.append(word)

    redacted = redact_items(redact, contents)
    return(redacted, redact)


#################################################################################
# Redacts dates - years, months, days of the week, time
from dateparser.search import search_dates
import re
def redact_dates(contents):
    
    redacted = [] #return this; holds redacted text
    redact =[] #holds list of words to redact

    dates = []
    dates_ = []
    time = []
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    #Search for dates in text
    dates = search_dates(contents)
    if dates:
        for i in dates:
            #print(i[0])
            dates_.append(i[0])

    ws = WhitespaceTokenizer()
    #Find DD, YYYY | D, YYYY | DD{st, nd, rd, th]} YYYY format and split by ws
    for i in dates_:
        ddyyyy = re.findall(r'\d{1,2}[\,|st|nd|rd|th]+\s+\d{4}', i)
        for d in ddyyyy:
            tokens = ws.tokenize(d)
            for t in tokens:
                dates_.append(t)

    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)
    
    for sentence in sentences:
        #Tokenize sentence into words
        words = ws.tokenize(sentence)
        
        #Checks words to see if any contain dates
        for word in words:
            i = 0
            while i < len(dates_):
                if(dates_[i] in word):
                    redact.append(word)
                    break
                else:
                    i = i + 1

        #Ignores upper/lower case and punction marks
        for word in words:
            if((word.translate(str.maketrans('','', string.punctuation)).casefold() in months)):
                redact.append(word)

    #Add words matching HH:MM or YYYY format
    time = re.findall(r'\d{1,2}[-\:\s]\d{2}|\d{4}|[(]+\d{1,2}[-\:\s]\d{2}', contents)
    for t in time:
        redact.append(t)
    
    redacted = redact_items(redact, contents)   
    return(redacted, redact)


#################################################################################
#Redacts Locations
nlp = spacy.load("en_core_web_sm")
from nltk.corpus import stopwords
def redact_loc(contents):

    redacted = [] #list to return, holds redacted text
    nnp = [] #list to hold proper nouns
    redact = [] #list that holds words to redact
    
    #Tokenize text into sentences
    default_st = nltk.sent_tokenize
    sentences = default_st(text = contents)
    
    loc = []
    loc_ = []
    stop_words = set(stopwords.words('english'))
    ws = WhitespaceTokenizer()
    
    for sentence in sentences:
        #Tag GPE words in each sentence
        doc = nlp(sentence)
        for ent in doc.ents:
            if(ent.label_ == 'GPE'):
                loc.append(ent.text)
                #Strip stop words and separate by ws
                for l in loc:
                    tokens = ws.tokenize(l)
                    for t in tokens:
                        if t not in stop_words:
                            loc_.append(t)
                                
        words = ws.tokenize(sentence)
        #Checks words to see if any are/contain GPE words
        for word in words:
            i = 0
            while i < len(loc_):
                if(loc_[i] in word):
                    redact.append(word)
                    break
                else:
                    i = i + 1

    redacted = redact_items(redact, contents)
    return(redacted, redact)


###############################################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Detect and Redact Sensitive Items')

    parser.add_argument('--input', type = str, required = True, help = 'Name of .txt file(s) to redact. Assuming in subfolder ~/docs')
    parser.add_argument('--output', type = str, required = True, help = 'Location to output redacted files')
    parser.add_argument('--names', action = 'store_true', help = 'Turns redaction flag on: Names')
    parser.add_argument('--genders', action = 'store_true', help ='Turns redaction flag on: Genders')
    parser.add_argument('--dates', action = 'store_true', help = 'Turns redaction flag on: Dates')
    parser.add_argument('--concept', nargs = '*', help = "Redacts all portions of text that have anything to do with said concept(s). Format: --concept 'word1' 'word2' etc")
    parser.add_argument('--numbers', action = 'store_true', help = 'Turns redaction flag on: Numbers')
    parser.add_argument('--locations', action = 'store_true', help = 'Turns redaction flag on: Locations')
    parser.add_argument('--stats', action = 'store_true', help = 'Name of file(s) to receive summary of redaction process. Returns types and counts of redacted terms and the stats of each redacted file(s)')

    args = parser.parse_args()
    #print(args)
    if args.input and args.output:
        main(args.input, args.output, args.names, args.genders, args.dates, args.concept, args.numbers, args.locations, args.stats)
