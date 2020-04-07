from project1 import redactor

test_string = 'This is a test to make sure the files/stats are read in correctly: I ate three bananas 4 days ago.'

#Tests get_stats function in redactor
def test_stats():
    
    stats = []
    print('\nUnredacted text: ' + test_string)

    #Create file
    fname = 'docs/test.txt'
    f = open(fname , 'w+')
    f.close()
    
    output = 'otherfiles/'


    text = redactor.redact_names(test_string)
    no_words = text[2]
    assert no_words == 20
    stats.append(text[1])

    #genders
    stats.append('')
    #concepts
    stats.append('')
    #dates
    stats.append('')
    
    text = redactor.redact_numbers(text[0])
    #numbers - 2
    stats.append(text[1])
    
    #locations
    stats.append('')


    stats_ = redactor.get_stats(fname, output, stats, no_words)
    assert (stats_[3]) == 2

    print('Redacted text: ' + text[0])
