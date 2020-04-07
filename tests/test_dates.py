from project1 import redactor

test_string = 'It was a cold, rainy night on Monday, November 1, 1975. Around 11:00 I saw a shadow moving in the forest. Forty-five years later, it is 2020 and I still think about that night.'

#Tests the redact+dates function
def test_dates():

    print('\nUnredacted text: ' + test_string)
    text = redactor.redact_dates(test_string)
    assert len(text[1]) >= 6
    print('Redacted text: ' + text[0])
