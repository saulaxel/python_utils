import os
import fnmatch
import gzip
import bz2
import re
from io import TextIOWrapper

def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard
    pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')

        yield f
        f.close()


def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line



if __name__ == '__main__':
    expected_gen_find = (
        f'test_gen/{folder}/{letter}.txt'
            for folder in ('foo', 'bar')
                for letter in ('a', 'b', 'c')
    )
    got_gen_find = gen_find('[a-z].txt', 'test_gen/')

    assert set(expected_gen_find) == set(got_gen_find)

    files = gen_opener(gen_find('[a-z].*', 'test_gen/'))
    for file in files:
        assert isinstance(file, TextIOWrapper)


    def gen_generators():
        '''
        Este generador genera generador
        gen_concatenate tiene el deber de aplanar dichos generador
        para que actúe como un generador no anidado
        '''
        for i in range(3):
            yield (i for _ in range(3))

    got_concat = gen_concatenate(gen_generators())
    expected_concat = (0, 0, 0, 1, 1, 1, 2, 2, 2)
    assert expected_concat == tuple(got_concat)


    lines = [
        'c',
        'c++',
        'python',
        'python3',
        'java'
    ]

    filtered = gen_grep('python', lines)
    expected = ('python', 'python3')
    assert tuple(filtered) == expected
