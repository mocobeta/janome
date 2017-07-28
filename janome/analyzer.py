# -*- coding: utf-8 -*-

# Copyright 2015 moco_beta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .tokenizer import Tokenizer
from .charfilter import *
from .tokenfilter import *


class Analyzer(object):
    def __init__(self, char_filters=[], tokenizer=Tokenizer(), token_filters=[]):
        self.char_filters = char_filters
        self.tokenizer = tokenizer
        self.token_filters = token_filters

    def analyze(self, text):
        for cfilter in self.char_filters:
            text = cfilter.filter(text)
        tokens = self.tokenizer.tokenize(text)
        for tfilter in self.token_filters:
            tokens = tfilter.filter(tokens)
        return tokens

