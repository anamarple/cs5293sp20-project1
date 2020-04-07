from project1 import redactor

test_string = "My name is Madison, but sometimes I go by Maddi by my friends."

#Tests the redact_names function
def test_names():
    
    print('\nUnredacted text: ' + test_string)
    text = redactor.redact_names(test_string)
    assert len(text[1]) == 2
    print('Redacted text: ' + text[0])
