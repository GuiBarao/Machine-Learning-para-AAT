from spellchecker import SpellChecker

spell = SpellChecker(language='pt')
word = "faldu"
corrected_text = spell.correction(word)
print(corrected_text) 
