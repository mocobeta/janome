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

from collections import defaultdict

class TokenFilter(object):
    u"""
    Base TokenFilter class.

    A TokenFilter modifies or transforms the input token sequence according to the rule described in apply() method.
    Subclasses must implement apply() method.

    Added in *version 0.3.4*
    """
    def filter(self, tokens):
        return self.apply(tokens)

    def apply(self, tokens):
        raise NotImplementedError


class LowerCaseFilter(TokenFilter):
    u"""
    A LowerCaseFilter converts the surface and base_form of tokens to lowercase.

    Added in *version 0.3.4*
    """
    def apply(self, tokens):
        for token in tokens:
            token.surface = token.surface.lower()
            token.base_form = token.base_form.lower()
            yield token


class UpperCaseFilter(TokenFilter):
    u"""
    An UpperCaseFilter converts the surface and base_form of tokens to uppercase.

    Added in *version 0.3.4*
    """
    def apply(self, tokens):
        for token in tokens:
            token.surface = token.surface.upper()
            token.base_form = token.base_form.upper()
            yield token
    

class POSStopFilter(TokenFilter):
    u"""
    A POSStopFilter removes tokens associated with part-of-speech tags listed in the stop tags list and keeps other tokens.

    Tag matching rule is prefix-matching. e.g., if '動詞' is given as a stop tag, '動詞,自立,*,*' and '動詞,非自立,*,*' (or so) are removed.

    Added in *version 0.3.4*
    """
    def __init__(self, pos_list):
        u"""
        Initialize POSStopFilter object.

        :param pos_list: stop part-of-speech tags list.
        """
        self.pos_list = pos_list

    def apply(self, tokens):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                continue
            yield token


class POSKeepFilter(TokenFilter):
    u"""
    A POSKeepFilter keeps tokens associated with part-of-speech tags listed in the keep tags list and removes other tokens.

    Tag matching rule is prefix-matching. e.g., if '動詞' is given as a keep tag, '動詞,自立,*,*' and '動詞,非自立,*,*' (or so) are kept.

    Added in *version 0.3.4*
    """
    def __init__(self, pos_list):
        u"""
        Initialize POSKeepFilter object.

        :param pos_list: keep part-of-speech tags list.
        """
        self.pos_list = pos_list

    def apply(self, tokens):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                yield token


class CompoundNounFilter(TokenFilter):
    u"""
    A CompoundNounFilter generates compound nouns.

    This Filter joins contiguous nouns.
    For example, '形態素解析器' is splitted three noun tokens '形態素/解析/器' by Tokenizer and then re-joined by this filter.
    Generated tokens are associated with the special part-of-speech tag '名詞,複合,*,*'

    Added in *version 0.3.4*
    """
    def apply(self, tokens):
        _ret = None
        for token in tokens:
            if _ret:
                if token.part_of_speech.startswith(u'名詞') and _ret.part_of_speech.startswith(u'名詞'):
                    _ret.surface += token.surface
                    _ret.part_of_speech = u'名詞,複合,*,*'
                    _ret.base_form += token.base_form
                    _ret.reading += token.reading
                    _ret.phonetic += token.phonetic
                else:
                    ret = _ret
                    _ret = token
                    yield ret
            else:
                _ret = token
        if _ret:
            yield _ret


class ExtractAttributeFilter(TokenFilter):
    u"""
    An ExtractAttributeFilter extracts a specified attribute of Token.

    **NOTES** This filter must placed the last of token filter chain because return values are not tokens but strings.

    Added in *version 0.3.4*
    """
    def __init__(self, att):
        u"""
        Initialize ExtractAttributeFilter object.

        :param att: attribute name should be extraced from a token. valid values for *att* are 'surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading' and 'phonetic'.
        """
        if att not in ['surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading', 'phonetic']:
            raise Exception('Unknown attribute name: %s' % att)
        self.att = att

    def apply(self, tokens):
        for token in tokens:
            yield getattr(token, self.att)


class TokenCountFilter(TokenFilter):
    u"""
    An TokenCountFilter counts word frequencies in the input text. Here, 'word' means an attribute of Token.

    This filter generates word-frequency pairs sorted in descending order of frequency.

    **NOTES** This filter must placed the last of token filter chain because return values are not tokens but string-integer tuples.

    Added in *version 0.3.5*
    """
    def __init__(self, att='surface', sorted=False):
        u"""
        Initialize TokenCountFilter object.

        :param att: attribute name should be extraced from a token. valid values for *att* are 'surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading' and 'phonetic'.
        :param sorted: sort items by term frequency
        """
        if att not in ['surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading', 'phonetic']:
            raise Exception('Unknown attribute name: %s' % att)
        self.att = att
        self.sorted = sorted

    def apply(self, tokens):
        token_counts = defaultdict(int)
        for token in tokens:
            token_counts[getattr(token, self.att)] += 1
        if self.sorted:
            return ((k, v) for k, v in sorted(token_counts.items(), key=lambda x: x[1], reverse=True))
        else:
            return ((k, v) for k, v in token_counts.items())
