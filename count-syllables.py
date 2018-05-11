#!/usr/bin/env python

import os
import json
import nltk
import sys
from pprint import pprint

USABLE_POS_TAGS = {
    'CC': 'coordinating conjunction',
    'CD': 'cardinal digit',
    'DT': 'determiner',
    'EX': 'existential there (like: "there is" ... think of it like "there exists"',
    'FW': 'foreign word',
    'IN': 'preposition/subordinating conjunction',
    'JJ': 'adjective	"big"',
    'JJR': 'adjective, comparative	"bigger"',
    'JJS': 'adjective, superlative	"biggest"',
    'LS': 'list marker	1)',
    'MD': 'modal	could, will',
    'NN': 'noun, singular "desk"',
    'NNS': 'noun plural	"desks"',
    'NNP': 'proper noun, singular	"Harrison"',
    'NNPS': 'proper noun, plural	"Americans"',
    'PDT': 'predeterminer	"all the kids"',
    'POS': 'possessive ending	parent\'s',
    'PRP': 'personal pronoun	I, he, she',
    'PRP': '	possessive pronoun	my, his, hers',
    'RB': 'adverb	very, silently,',
    'RBR': 'adverb, comparative	better',
    'RBS': 'adverb, superlative	best',
    'RP': 'particle	give up',
    'TO': 'to	go "to" the store.',
    'UH': 'interjection	errrrrrrrm',
    'VB': 'verb, base form	take',
    'VBD': 'verb, past tense	took',
    'VBG': 'verb, gerund/present participle	taking',
    'VBN': 'verb, past participle	taken',
    'VBP': 'verb, sing. present, non-3d	take',
    'VBZ': 'verb, 3rd person sing. present	takes',
    'WDT': 'wh-determiner	which',
    'WP': 'wh-pronoun	who, what',
    'WP': '	possessive wh-pronoun	whose',
    'WRB': 'wh-abverb	where, when',
}

def print_err(s):
    sys.stderr.write(s + '\n')
    sys.stderr.flush()

class Syllables:
    def __init__(self, basedir):
        self.basedir = basedir
        self.words = {}
        for filename in os.listdir(basedir):
            fullpath = os.path.join(basedir, filename)
            if filename.endswith('-syllable-words.txt'):
                try:
                    syllable_count = int(filename.split('-', 2)[0])
                except Exception as e:
                    print 'Failed filename parse:', filename, e
                    continue
                for line in open(fullpath):
                    self.words[line.strip()] = syllable_count
        print_err('Loaded %d words' % len(self.words))

if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    syllables = Syllables('wordsbysyllables')
    input_text = '''\
Whitecaps on the bay:
A broken signboard banging
In the April wind.'''
    tokens = nltk.word_tokenize(input_text)
    tags = nltk.pos_tag(tokens)
    keep = []
    skip = []
    for word, pos in tags:
        if pos in USABLE_POS_TAGS:
            keep.append({
                'word':word,
                'pos':pos,
                'syllables':syllables.words.get(word.lower(), 0),
            })
        else:
            skip.append((word, pos))
    result = {
        'text':input_text,
        'tokens':keep,
        'ignored':skip,
        'syllables':sum([w['syllables'] for w in keep]),
        'unknown':[w['word'] for w in keep if w['syllables'] == 0],
    }
    print json.dumps(result)
