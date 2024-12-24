import sys
sys.path.insert(0, 'src')

from Texto import Texto

def main():

    txt = Texto.xml_to_object(0, 'kaggle')


    print(txt.nStopWords())
    
if __name__ == '__main__':
    main()