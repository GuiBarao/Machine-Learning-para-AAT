import sys
sys.path.insert(0, 'src')

from Texto import Texto

import pandas as pd

def main():

    txt = Texto.xml_to_object(340, 'uol')
    print(txt.redacao)
    print(txt.n_genitiveMarker())


if __name__ == '__main__':
    main()