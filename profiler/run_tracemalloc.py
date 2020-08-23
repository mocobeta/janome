import tracemalloc
import sys
from janome.tokenizer import Tokenizer

repeat = 10
mmap = True
dump_file = 'memusage.dump'
if len(sys.argv) > 1 and sys.argv[1] == '-nommap':
    mmap = False
    dump_file = 'memusage_nommap.dump'

with open('text_lemon.txt') as f:
    s = f.read()

# Start tracing
tracemalloc.start(10)

# blocks allocated by initializing Tokenizer
t = Tokenizer(mmap=mmap)
snapshot1 = tracemalloc.take_snapshot()
top_stats1 = snapshot1.statistics('lineno')

with open(dump_file, 'w') as f:
    f.write('**Initializing Tokenizer**\n')
    f.write('[Top 10 lines]\n')
    for stat in top_stats1[:10]:
        f.write(str(stat))
        f.write('\n')
    f.write('\n')

# blocks allocated when tokenizing
list(t.tokenize(s))
snapshot2 = tracemalloc.take_snapshot()
top_stats2 = snapshot2.compare_to(snapshot1, 'lineno')
with open(dump_file, 'a') as f:
    f.write('**Running Tokenizer**\n')
    f.write('[Top 20 lines]\n')
    for stat in top_stats2[:20]:
        f.write(str(stat))
        f.write('\n')
    f.write('\n')
