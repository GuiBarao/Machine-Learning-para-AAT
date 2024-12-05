import sys
sys.path.insert(0, 'src')

from Texto import Texto
from Corretor import Corretor

def main():

    txt = Texto.xml_to_object(0, 'fundamental')
    print(txt.avaliacao)
    
if __name__ == '__main__':
    main()