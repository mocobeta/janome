from cProfile import Profile
from pstats import Stats
import sys
from janome.tokenizer import Tokenizer

repeat = 10
mmap = True
dump_file = 'tokenizer.profile'
if len(sys.argv) > 1 and sys.argv[1] == '-nommap':
    mmap = False
    dump_file = 'tokenizer_nommap.profile'

t = Tokenizer(mmap=mmap)

with open('text_lemon.txt') as f:
    s = f.read()

profiler = Profile()
profiler.runcall(lambda: [list(t.tokenize(s)) for i in range(repeat)])

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('tottime')
stats.print_stats()
stats.dump_stats(dump_file)
print(f'Result was dumped to {dump_file}.')
