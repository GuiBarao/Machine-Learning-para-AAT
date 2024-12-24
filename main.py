import sys
sys.path.insert(0, 'src')

from Texto import Texto

import pandas as pd

def main():

    txt = Texto.xml_to_object(1, 'uol')
    print(txt.redacao)
    print(txt.nWords())
    print(txt.nSentences())
    print(txt.dale_chall())


if __name__ == '__main__':
    main()