import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from dic import SystemDictionary
SYS_DIC = SystemDictionary(".")
import struct
import logging
import sys

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    words_file = sys.argv[1]
    WORDS = []
    with open(words_file) as f:
        for line in f:
            word = line.strip()
            WORDS.append(word)
    invalid_count = 0
    for word in WORDS:
        (matched, outputs) = SYS_DIC.matcher.run(word.encode('utf8'))
        if not matched:
            print('No match for %s' % word)
            invalid_count += 1
        for o in outputs:
            try:
                struct.unpack('I', o)
            except:
                print('Invalid output for %s, %s' % (word, str(o)))
                invalid_count += 1
    print('invalid outputs = %d' % invalid_count)

