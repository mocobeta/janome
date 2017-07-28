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


class TokenFilter(object):
    def filter(self, tokens):
        return self.apply(tokens)

    def apply(self, tokens):
        for token in tokens:
            yield token


class LowerCaseFilter(TokenFilter):
    def apply(self, tokens):
        for token in tokens:
            token.surface = token.surface.lower()
            yield token


class UpperCaseFilter(TokenFilter):
    def apply(self, tokens):
        for token in tokens:
            token.surface = token.surface.upper()
            yield token
    

class POSFilter(TokenFilter):
    def __init__(self, pos_list):
        self.pos_list = pos_list

    def apply(self, tokens):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                continue
            yield token


class POSKeepFilter(TokenFilter):
    def __init__(self, pos_list):
        self.pos_list = pos_list

    def apply(self, tokens):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                yield token


class CompoundNounTokenFilter(TokenFilter):
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


class ExtractAttributeTokenFilter(TokenFilter):
    def __init__(self, att):
        if att not in ['surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading', 'phonetic']:
            raise Exception('Unknown attribute name: %s' % att)
        self.att = att

    def apply(self, tokens):
        for token in tokens:
            yield getattr(token, self.att)