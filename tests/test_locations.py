from project1 import redactor

test_string = 'Last year I went to Paris, and this year I am hoping to go to Las Vegas.'

#Tests the redact_loc function
def test_locs():

    print('\nUnredacted text: ' + test_string)
    text = redactor.redact_loc(test_string)
    assert len(text[1]) >= 2
    print('Redacted text: ' + text[0])
