import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from dic import SystemDictionary
SYS_DIC = SystemDictionary("ipadic")