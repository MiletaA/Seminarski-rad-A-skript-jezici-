import matplotlib.pyplot as plt
import csv
from Data import *
def grafikon():
    x = []
    y = []

    with open(r'C:\Users\admin\Desktop\Bankomat\Data\usersdata.csv','r') as csvfile:
        r = csv.reader(csvfile, delimiter = ',')
        next(r) #preskace prvu liniju
       
        for indiv_korisnik_info in r:
            if indiv_korisnik_info[0].startswith('#'):     
                pass
            elif indiv_korisnik_info[1].startswith('admin pristup'):     
                pass
         
            else:
                x.append(indiv_korisnik_info[1])
                y.append(float((indiv_korisnik_info[3])))
                
    plt.bar(x, y, color = 'b', width = 0.3, label = "kolicina novca")
    plt.xlabel('Imena')
    plt.ylabel('Stanje racuna')
    plt.title('Kolicina novca kod korisinika')
    plt.legend()
    plt.show()