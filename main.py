import sys
sys.path.insert(0, 'src')

from Texto import Texto

def busca():
        
    id = 0

    while(True):


        txt = Texto.xml_to_object(id, 'uol')
        id += 1
        print(id)
        print("---",txt.averageEuclideanDistance_betweenCentroidAndEachPoint(),"---")


def main():
    
    busca()

    txt = Texto.xml_to_object(180, 'kaggle')
    print(txt.redacao)
    print(txt.janelas_deslizantes())



    

    


if __name__ == '__main__':
    main()