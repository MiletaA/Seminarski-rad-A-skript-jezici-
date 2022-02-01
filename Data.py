import os
import csv

#path za fajl
def join():
    directory = "Data"
    name = "usersdata.csv"
    filename = os.path.join(directory, name)
    return filename


#prilikom startovanja logina pravi se folder
def data():
    filename = join()
    d = {}
    # new = ['Tekuci racun','Ime i Prezime','PIN','Stanje Racuna','Vreme','Email adresa']
    new = []
    try:
        with open(filename, "a",newline="") as ap:
            if (os.path.getsize(filename)) <= 0:
                wr = csv.writer(ap)
                wr.writerow(new)
                ap.close()
                print ("Prvo napravite nalog!")                
                return

            else:
                with open(filename, "r",newline="") as rd:
                    r = csv.reader(rd)
                    for indiv_korisnik_info in r:
                        if (indiv_korisnik_info == ['']) or (indiv_korisnik_info == []):
                            continue
                            
                        else:
                            try:
                                indiv_korisnik_info[1] = (indiv_korisnik_info[1])
                                indiv_korisnik_info[3] = float(indiv_korisnik_info[3])
                                d[indiv_korisnik_info[0]] = indiv_korisnik_info[1],indiv_korisnik_info[2],indiv_korisnik_info[3],indiv_korisnik_info[4],indiv_korisnik_info[5],indiv_korisnik_info[6]
                              
                            except IndexError:
                                d[indiv_korisnik_info[0]] = indiv_korisnik_info[1],indiv_korisnik_info[2],indiv_korisnik_info[3],indiv_korisnik_info[4],indiv_korisnik_info[5],"None"
                    return d
    
    except (IOError or FileNotFoundError):
        os.mkdir("Data")
        data()
