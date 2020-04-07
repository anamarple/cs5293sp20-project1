from project1 import redactor

test_string = "I'm not sure if I ever want to have kids. I mean I have my dog. My dog is my fur baby and I love him. My dog helps me feel better."

#Tests the redact_concepts function - should redact synonyms to concepts
def test_concepts():

    print('\nUnredacted text: ' + test_string)
    concepts = ['children', 'help']
    text = redactor.redact_concepts(test_string, concepts)
    
    #Should redact sentences 1, 3, and 4
    assert len(text[1]) >= 26
    print('Redacted text: ' + text[0])
