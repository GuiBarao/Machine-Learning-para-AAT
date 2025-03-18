import sys
sys.path.insert(0, 'src')

from Texto import Texto

def busca():
        
    id = 0

    while(True):


        txt = Texto.xml_to_object(id, 'uol')
        id += 1
        print(id)
        print("---",txt.height_treeSentence(),"---")


def main():
    
    busca()

    txt = Texto.xml_to_object(18, 'uol')
    print(txt.height_treeSentence())



    

    


if __name__ == '__main__':
    main()