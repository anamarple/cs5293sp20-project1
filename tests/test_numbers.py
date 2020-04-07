from project1 import redactor

test_string = 'I made a 100 on my text analytics project. The average score was somewhere between thirty six and seventy-five. I have $1,200 in my bank account.'

#Tests the redact_numbers function - redacts digits and words spelling out numbers
def test_numbers():

    print('\nUnredacted text: ' + test_string)
    text = redactor.redact_numbers(test_string)
    assert len(text[1]) >= 5
    print('Redacted text: ' + text[0])

