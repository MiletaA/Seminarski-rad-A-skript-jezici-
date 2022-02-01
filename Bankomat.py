from getpass import getpass as gp
import os, csv

from Data import join,data
from slanje_mejla import sendmail
import time,datetime


stanje = 0.0



#nakon uspesnog prijavljivanja/registrovanja pokrece se funkcija bankomat
def bankomat(ime_prezime,Stanje,Pin,t_r,adresa):
    filename = join()
    clear = ('cls' if os.name == 'nt' else 'clear')
    print(("Postovani"),(ime_prezime.upper())+("!"))
    print("Dobrodosli \n")
    
    
    #izberi
    global stanje
    stanje += Stanje
    Opr = input("Izaberite jedno : \n1. Provera stanja \n2. Provera tekuceg racuna \n3. Depozit \n4. Podizanje novca \n5. Prenos novca \n6. Promena Pina \n0. Izlaz \n")
    os.system(clear)

    if not Opr.isdigit():
        Opr = 7

    while int(Opr) != 0:

        if int(Opr) == 1:
            os.system(clear)
            print (":: Moje Stanje : ","{:,} ::".format(stanje),"\n")

        elif int(Opr) == 2:
            os.system(clear)
            print(":: Tekuci Racun =",t_r,":: \n")

        #Depozit
        elif int(Opr) == 3:
            os.system(clear)
            Depozit(stanje, adresa)
        #Podizanje novca
        elif int(Opr) == 4:
            os.system(clear)
            podizanjenovca(stanje, adresa)

        #Prenos novca
        elif int(Opr) == 5:
            os.system(clear)
            if stanje < 0.0:
                print ("Nemate dovoljno novca za tranzakciju")

            else:
                tekuci_racun = input('Unesite tekuci racun: ') 
                if (tekuci_racun == t_r):
                    os.system(clear)
                    print("Prenos nije moguc,to je Vas tekuci racun")
                else:
                    kolicina_novca = prenos_novca(tekuci_racun, stanje, t_r, adresa)
                    stanje -= float(kolicina_novca)


        #Promena Pina 
        elif int(Opr) == 6:
            os.system(clear)
            Pin = promena_pina(Pin, adresa)
        
        
        else:
            os.system(clear)
            print (":: Doslo je do greske,molimo pokusajte ponovo ::")

   

        #da ne ulazi u beskonacan loop
        Opr = input(":: Izaberite jedno : \n1. Provera stanja \n2. Provera tekuceg racuna \n3. Depozit \n4. Podizanje novca \n5. Prenos novca \n6. Promena Pina \n0. Izlaz \n")
        if not Opr.isdigit():
            Opr = 7
            os.system(clear)

    os.system(clear)
    print ("::: Hvala Vam na koriscenju! :::\n::: Srdacan Pozdrav! :::")
    

    with open(filename,'a+',newline="") as ap: #a+ zapisuje na kraju
        re_new = [t_r,ime_prezime,str(Pin),str(stanje),time.strftime('%d-%b-%Y at %I:%M %p'),adresa]
        w = csv.writer(ap)
        w.writerow(re_new)
        ap.close()
    return
#Depozit 
def Depozit(Stanje, adresa):
    clear = ('cls' if os.name == 'nt' else 'clear')
    global stanje
    print(":: Depozit ::")
    try:
        kolicina_uplate = input("Unesite zeljenu kolicinu u dinarima: ")

        #ne sme negativno 
        if float(kolicina_uplate) >= 0.0:
            #ne sme preko 14 cifri
            if (len(kolicina_uplate) > 14) or ((len(str(float(kolicina_uplate)+stanje))) > 14):
                os.system(clear)
                print (':: Ogranicenje iznosa je prekoraceno! ::')
                return

            #Depozit povecan u brojacu
            else:
                stanje += float(kolicina_uplate)
                os.system(clear)
                MSG = "Uspesno ste uplatili novac "+str(kolicina_uplate)+"\n\nVase stanje: "+str(stanje)
                msg = sendmail(adresa, MSG)
                os.system(clear)
                if not (msg == True): print(msg)
                print(":: Uspesno ste uplatili novac",kolicina_uplate,"::",'\n')
                return

        elif float(kolicina_uplate) < 0.0:
            os.system(clear)
            #Ako unese negativno
            print (":: Greska pri unosu. ::\n")
            return Depozit(stanje, adresa)

        else:
            os.system(clear)
            print (":: Greska pri unosu. ::\n")
            return Depozit(stanje, adresa)

    except ValueError:
        os.system(clear)
        print (":: Greska pri unosu. ::\n")
        return Depozit(stanje, adresa)

#Podizanje novca
def podizanjenovca(Stanje, adresa):
    clear = ('cls' if os.name == 'nt' else 'clear')
    global stanje
    print(":: Podizanje novca ::")
    #Ako nema novca
    if float(stanje) <= 0.0:
        print (":: Podizanje novca nije uspelo! ::\n:: Stanje racuna: ",stanje,"::","\n:: Molimo Vas prvo uplatite novac! ::\n")
        return

    else:
        try:
            podizanje_novca = input("Unesite zeljenu kolicinu(din): ")
            os.system(clear)

            #Ako unese negativno
            if float(podizanje_novca) < 0.0:
                os.system(clear)
                print (":: Greska pri unosu. ::\n")
                return podizanje_novca(stanje, adresa)

            elif float(podizanje_novca) <= stanje:
                stanje -= float(podizanje_novca)
                MSG = "Uspesno ste podigli novac "+str(podizanje_novca)+"\n\nVase stanje: "+str(stanje) 
                msg = sendmail(adresa, MSG)
                os.system(clear)
                if not (msg == True): print(msg)
                print(":: Uspesno ste podigli novac",podizanje_novca,"::",'\n')
                return

            else:
                os.system(clear)
                print (":: Podizanje novca nije uspelo! ::\n:: Moje stanje :",stanje,"::","\n")
            return podizanjenovca(stanje, adresa)

        except ValueError:
            os.system(clear)
            print (":: Greska pri unosu. ::\n")
            return podizanjenovca(stanje, adresa)

#promena pina
def promena_pina(Pin, adresa):
    clear = ('cls' if os.name == 'nt' else 'clear')
    os.system(clear)
    pin_brojac_unosa = 0
    print(":: Unesite zeljeni pin:....::")
    while pin_brojac_unosa != 3:
        print(":: Broj preostalih pokusaja :",(3-pin_brojac_unosa),"::")
        pin = str(gp ("Unesite pin : "))
        os.system(clear)

        if (len(pin) == 4) and (pin.isdigit() == True):
            if not pin == Pin:
                os.system(clear)
                pin_potvrda = str(gp ("Potvrdite Pin : "))

                if pin == pin_potvrda:
                    Pin = pin
                    os.system(clear)
                    MSG = "Uspesno ste promenili pin,novi pin je:" + Pin 
                    msg = sendmail(adresa, MSG)
                    os.system(clear)
                    if not (msg == True): print(msg)
                    print(':: Pin uspesno promenjen! ::\n')
                    return(Pin)

                else:
                    os.system(clear)
                    print(":: Pin neuspesno promenjen ::")
                    print (":: Pinovi se ne poklapaju ::\n")
                    pin_brojac_unosa +=1

            else:
                pin_brojac_unosa += 1
                os.system(clear)
                print(":: Pin neuspesno promenjen ::")
                print(":: Unesite novi pin ::\n")


        else:
            pin_brojac_unosa += 1
            os.system(clear)
            print(":: Pin neuspesno promenjen ::")
            print(":: Pogresan pin ::\n")
    return(Pin)
#prenos novca
def prenos_novca(tekuci_racun, balans, t_r, adresa):
    import time,datetime
    clear = ('cls' if os.name == 'nt' else 'clear')
    os.system(clear)

    d = data()
    filename = join()
    kolicina_novca = 0.0

    print (":: Unesite kolicinu za prenos ::")
    ugasen_nalog = str('#'+tekuci_racun)
    #ako nije aktivan(ima # pre tekuceg racuna)
    if ugasen_nalog in d.keys():
        os.system(clear)
        print (":: Tekuci racun nije aktivan ::")
        return kolicina_novca

    elif tekuci_racun in d.keys():
        try:
            kolicina_novca = input("Unesite zeljenu kolicinu(din): ")
            #ne sme minus
            if float(kolicina_novca) < 0.0 or ('-' in kolicina_novca):
                os.system(clear)
                print (":: Greska pri unosu. ::\n")
                return prenos_novca(tekuci_racun, balans, t_r, adresa)
            #nema dovoljno novca
            elif float(kolicina_novca) > float(balans):
                os.system(clear)
                print (":: Ne mozete izvrsiti tranzakciju! ::\n:: Moje stanje : ",balans,"::","\n")
                return prenos_novca(tekuci_racun, balans, t_r, adresa)

            else:
                os.system(clear)
                print(":: Tekuci Racun :",tekuci_racun,"::")
                print(":: Ime i Prezime :",d[tekuci_racun][0],"::")
                print(":: Uneta kolicina za prenos = ","{:,} ::".format(float(kolicina_novca)),"\n")

                confirm = input("Molimo Vas potvrdite \n1. Da \n2. Ne \n")

                if (confirm == '1'):
                        with open(filename,'a+',newline="") as ap:
                            trenutni_balans = balans
                            balans = str(float(d[tekuci_racun][2]) + float(kolicina_novca))
                            re_new = [tekuci_racun,d[tekuci_racun][0],d[tekuci_racun][1],balans,d[tekuci_racun][3],d[tekuci_racun][4]]
                            w = csv.writer(ap)
                            w.writerow(re_new)
                            ap.close()

                        os.system(clear)
                        MSG_from = "Uspesno ste uplatili(din) :  "+str(kolicina_novca)+" Na tekuci racun :"+str(tekuci_racun)+"\n\nVase stanje nakon uplate: "+str(float(trenutni_balans) - float(kolicina_novca))
                        MSG_to = "Uspesno ste primili novac(din) "+str(kolicina_novca)+" Od tekuci racun "+str(t_r)+"\n\nVase stanje: "+str(float(balans))
                        sendmail(adresa, MSG_from)
                        msg2 = sendmail(d[tekuci_racun][4], MSG_to)
                        os.system(clear)
                        if not (msg2 == True): print(msg2)
                        print(":: Zeljena kolicina uspesno uplacena!::")
                        return kolicina_novca
                else:
                    kolicina_novca = 0
                    os.system(clear)
                    print(":: Zeljena kolicina nije uspesno uplacena! ::")
                    return kolicina_novca

        except ValueError as err:
            os.system(clear)
            print("Greska :",err)
            print(":: Greska pri unosu. ::\n")
            return prenos_novca(tekuci_racun, balans, t_r, adresa)
    else:
        os.system(clear)
        print (":: Doslo je do neslaganja,pokusajte ponovo ::")
        return kolicina_novca
