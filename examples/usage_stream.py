from janome.tokenizer import Tokenizer
from io import open

print('Tokenize (stream mode)')
t = Tokenizer()

with open('text_lemon.txt', encoding='utf-8') as f:
    text = f.read()
    for token in t.tokenize(text, stream=True):
        print(token)
