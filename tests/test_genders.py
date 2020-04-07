from project1 import redactor

test_string = 'This is a test to make sure that words such as him, HER, and shE are redacted.'

#Tests the redact_gender function - should redact gendered words
def test_genders():
    
    print('\nUnredacted text: ' + test_string)
    text = redactor.redact_gender(test_string)
    assert len(text[1]) == 3
    print('Redacted text: ' + text[0])
