import sys
sys.path.insert(0, 'src')

from Texto import Texto

import pandas as pd

def main():

    txt = Texto.xml_to_object(40, 'uol')
    print(txt.typeToken_ratio())
    print(txt.D_estimate())


if __name__ == '__main__':
    main()