import sys
sys.path.insert(0, 'src')

from Texto import Texto

def busca():
        
    id = 0

    while(True):

        try:
            txt = Texto.xml_to_object(id, 'kaggle')
            id += 1

            n = txt.n_whAdverb()

            if n != 0:
                print(id, '//', n)
        except:
            exit()


def main():

    busca()
    txt = Texto.xml_to_object(2, 'kaggle')
    print(txt.n_verb_thirdPersonSingPresent())


    

    


if __name__ == '__main__':
    main()