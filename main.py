import sys
sys.path.insert(0, 'src')

from Texto import Texto

def busca():
        
    id = 0

    while(True):

        try:
            txt = Texto.xml_to_object(id, 'kaggle')
            id += 1
            print(id)
            print(txt.height_treeSentence())
            print('foi')
        except:
            exit()


def main():
    busca()
    txt = Texto.xml_to_object(2, 'kaggle')
    print(txt.averageDistance_neighboringPoints_cos())


    

    


if __name__ == '__main__':
    main()