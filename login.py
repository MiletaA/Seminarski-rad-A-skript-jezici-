import time,datetime
import os, sys, csv, re
import random as rd
from getpass import getpass as gp


from Bankomat import bankomat
from Data import data,join
from t_r_gen import tekuci_racun_gen
from slanje_mejla import sendmail
from graph import *



#Cisti terminal
clear = ('cls' if os.name == 'nt' else 'clear')

#main funkcije
def login_user():
    
    d = data()

    user = input("Izaberite jedno : \n1. Prijavljivanje \n2. Registracija naloga \n3. Gasenje naloga  \n0. Izlaz \n")
    os.system(clear)

    if not str(user).isdigit():
        print ("Molimo Vas izaberite ponovo,greska pri biranju.")
        return login_user()

    #Prijavljivanje
    if int(user) == 1:
        os.system(clear)
        login(d)

    #Registracija naloga
    elif int(user) == 2:
        os.system(clear)
        novi_nalog()
    #Gasenje naloga
    elif int(user) == 3:
        os.system(clear)
        gasenje_naloga()
    
    #Izlaz
    elif int(user) == 0:
        print ("Dovidjenja!")
   

    #Greska pri unosu(ni jedan broj od navedenih) ponovno pokretanje programa 
    else:
        print ("Greska pri biranju,molimo Vas izaberite ponovo. '",user,"'")
        return login_user()

    return

#Prijavljivanje (1)
def login(d):
    os.system(clear)
    ime_prezime = input("Prijavljivanje\n Unesite ime i prezime : ")
    entry = 0
    if (d == None):
        os.system(clear)
        print ("Molimo Vas prvo napravite nalog!")
        return novi_nalog()
    
    for a in ime_prezime:
        if ((ord(a) >= 65) and (ord(a) <= 90)) or ((ord(a) >= 97) and (ord(a) <= 122)) or (ord(a) == 32):
            continue
        else:
            os.system(clear)
            print ("Mozete koristiti mala ili velika slova i razmak!")
            return login_user()

    for parametar in d.keys():
        if ime_prezime.lower() in d[parametar]:
            t_r = parametar
            break
        else:
            t_r = None
    
    if t_r == None:
        os.system(clear)
        print("Korisnik ne postoji/Pogresno ime!")
        return login_user()

    elif t_r.startswith('#'):
        os.system(clear)
        print("Nalog je De-Aktiviran")
        return login_user()

    #Admin pristup
    elif (ime_prezime.lower() == 'admin pristup'):
        return admin_block(t_r)
    #korisnici block
    elif not (ime_prezime.lower() == 'admin pristup'):
        while int(entry) != 3:
            print("Broj preostalih pokusaja :",(3-entry))
            pin = str(gp("Unesite pin : "))

            if pin == d[t_r][1]:
                Pin = pin
                Stanje = d[t_r][2]
                E_mail_adresa = d[t_r][4]
                os.system(clear)
                return bankomat(ime_prezime,Stanje,Pin,t_r,E_mail_adresa)

            else:
                entry += 1
                os.system(clear)
                print ("Pogresan Pin!")
        os.system(clear)
        print ("Neuspelo prijavljivanje\n")
        return login_user()

    else:
        os.system(clear)
        print ("Korisnik ne postoji!")
        return login_user()


#novi nalog
def novi_nalog():
    import time,datetime

    filename = join()
    ime_prezime1 = input("Registracija korisnika\n Ime : ")
    os.system(clear)
    ime_prezime2 = input("Prezime: ")

    if (ime_prezime1.isalpha() == False) or (ime_prezime2.isalpha() == False) or (ime_prezime1 == ime_prezime2):
        os.system(clear)
        print ("Pogresan unos!")
        return novi_nalog()

    #automatski generisan pin
    auto_gen_pin = rd.randint(1000,9999)
    os.system(clear)
    ime_prezime = (ime_prezime1.lower())+' '+(ime_prezime2.lower())
    t_r = tekuci_racun_gen(ime_prezime)
    
    E_mail_adresa = input("Unesite e-mail adresu : ")
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", E_mail_adresa):
        os.system(clear)
        E_mail_adresa = "Nije unet email" 
        print("Mail adresa ne postoji")

    else:
        E_mail_adresa = E_mail_adresa

    print("Pin : ",auto_gen_pin)
    confirm = input("Da li Zelite da koristite ovaj pin ? \n1. Da \n2. Ne \n")

    if (confirm == '1'):
        os.system(clear)
        
        print ("Ime i Prezime :",ime_prezime1+' '+ime_prezime2,"\nTekuci Racun :",t_r,"\nPin :",auto_gen_pin)
        confirm = input("Potvrdi. \n1. Da \n2. Ne \n")

        if (confirm == '1'):
            os.system(clear)
            with open(filename, "a+",newline="") as wr: #a+ appending dodajuci
                ime_prezime = (ime_prezime)
                new = [t_r,ime_prezime,auto_gen_pin,'0.0',time.strftime('%d-%b-%Y at %I:%M %p'),E_mail_adresa]

                w = csv.writer(wr)
                w.writerow(new)
                wr.close()
                MSG = "Informacije o nalogu"+"\n\n"+"Tekuci Racun : "+t_r +"\n" "Pin:" + str(auto_gen_pin)
                vr = sendmail(E_mail_adresa, MSG)
                vr = E_mail_adresa
                os.system(clear)
                if not (vr == True): print(vr)
                print ("Uspesno ste napravili nalog! \n")
                return login_user()

        elif (confirm == '2'):
            os.system(clear)
            print ("Nalog nije napravljen!")
            return login_user()

        else:
            os.system(clear)
            print ("Nije dobar unos,pokusajte ponovo!")
            return novi_nalog()
    #promena auto-gene pina
    else:
        os.system(clear)
        pin_count = 0
        print("Zeljeni Pin....")
        while pin_count != 3:
            print("Preostalo pokusaja :",(3-pin_count))
            pin = str(gp ("Unesite Pin: "))
            os.system(clear)

            if (len(pin) == 4) and (pin.isdigit() == True):
                os.system(clear)
                confirm_pin = str(gp ("Potvrdite Pin : "))

                if pin == confirm_pin:
                    os.system(clear)
                    print ("Ime i Prezime :",ime_prezime1+' '+ime_prezime2,"\nTekuci Racun :",t_r,"\nPin :",pin)
                    confirm = input("Potvrdi. \n1. Da \n2. Ne \n")

                    if (confirm == '1'):
                        os.system(clear)
                        with open(filename, "a+",newline="") as wr:
                            new = [t_r,ime_prezime,pin,'0.0',time.strftime('%d-%b-%Y at %I:%M %p'),E_mail_adresa]

                            w = csv.writer(wr)
                            w.writerow(new)
                            wr.close()
                            MSG = "Informacije o nalogu"+"\n\n"+"Tekuci Racun : "+t_r +"\n" "Pin:" + str(pin)
                            vr = sendmail(E_mail_adresa, MSG)
                            os.system(clear)
                            if not (vr == True): print(vr)
                            print ("Uspesno ste napravili nalog! \n")
                            return login_user()

                    elif (confirm == '2'):
                        os.system(clear)
                        print ("Nalog nije napravljen!")
                        return login_user()

                    else:
                        os.system(clear)
                        print ("Nalog nije napravljen!")
                        return novi_nalog()

                else:
                    print ("Pin-ovi nisu isti!")
                    pin_count +=1

            else:
                pin_count = pin_count
                os.system(clear)
                print ("Pogresan pin")

        os.system(clear)
        print ("Nalog nije napravljen!")
        return login_user()
#Gasenje naloga
def gasenje_naloga():
    d = data()
    filename = join()

    os.system(clear)
    t_r = input("Gasenje naloga\nUnesite Tekuci Racun : ")

    if t_r in d.keys():
        acc_pin = str(gp("Unesite Pin: "))

        if acc_pin == d[t_r][1]:
            os.system(clear)
            print ("Gasenje naloga :",d[t_r][0])
            confirm = input("Potvrdi. \n1. Da \n2. Ne \n")

            if (confirm == '1') :
                os.system(clear)
                d[('#'+t_r)] = d.pop(t_r)
                with open(filename,"w",newline="") as rd:
                    r = csv.writer(rd)
                    r.writerow([])
                    rd.close()
                with open(filename,"a",newline="") as ow:
                    for parametar in d.keys():
                        parametri = (d[parametar][0])
                        over_write = [parametar,parametri,str(d[parametar][1]),str(d[parametar][2]),str(d[parametar][3]),str(d[parametar][4])]
                        o = csv.writer(ow)
                        o.writerow(over_write)
                    ow.close()
                    print ("Gasenje naloga je uspesno \n")
                    return login_user()

            elif (confirm == '2'):
                os.system(clear)
                print ("Gasenje naloga je neuspesno")
                return login_user()

            else:
                os.system(clear)
                print ("Gasenje naloga je neuspesno")
                return login_user()

        else:
            os.system(clear)
            print ("Pin-ovi nisu isti!")
            return login_user()

    elif ("#"+t_r) in d.keys():
        os.system(clear)
        print("Nalog je već ugasen!")
        return login_user()

    else:
        os.system(clear)
        print ("Doslo je do greske,pokusajte ponovo.")
        return login_user()
#admin block
def admin_block(t_r):
    d = data()
    pin = str(gp("Unesite Pin: "))
    if pin == d[t_r][1]:
        del d[t_r] #da se admin nalog ne prikazuje
        os.system(clear)
        print (time.strftime('Datum:%d-%b-%Y \nVreme:%I:%M %p'))
        print ("::: Dobrodosli(admin panel) :::\n\n:: Izaberite nesto od ponudjenih opcija ::")
        ad = input("1. Broj korisnika \n2. Broj aktivnih naloga \n3. informacije o aktivni korisnicima  \n4. Aktivnosti korisnika \n5. Pronadji nalog \n6. Ugasite nalog \n7. Grafikon \n0. Izlaz\n")
        while ad != '0':

            if ad == '1':
                os.system(clear)
                aktivni_korisnici, ugaseni_korisnici = 0, 0
                for korisnici in d.keys():
                    if not korisnici.startswith('#'):
                        aktivni_korisnici += 1
                    else:
                        ugaseni_korisnici += 1

                print(":: Korisnici ::")
                print("Aktivni korisnici :",aktivni_korisnici)
                print("Ugaseni korisnici :",ugaseni_korisnici,'\n')

            elif ad == '2':
                os.system(clear)
                aktivni_korisnici = 0
                print (":: Broj aktivnih naloga ::")
                for korisnici in d.keys():
                    if not korisnici.startswith('#'):
                        aktivni_korisnici += 1
                        print ("Aktivni korisnici",aktivni_korisnici,':',d[korisnici][0])
                print('\n')

            elif ad == '3':
                os.system(clear)
                print (":: O korisnicima ::")
                for korisnik_info in d.keys():
                    if not korisnik_info.startswith('#'):
                        print ("Tekuci Racun :",korisnik_info,"Ime i Prezime =",d[korisnik_info][0],", Pin :",d[korisnik_info][1],", Stanje Racuna :","{:,}".format(d[korisnik_info][2]))
                print('\n')

            elif ad == '4':
                os.system(clear)
                print (":: Aktivnosti korisnika ::")
                for korisnik_info in d.keys():
                    if not korisnik_info.startswith('#'):
                        print ("Tekuci Racun :",korisnik_info,"Korisnik:",d[korisnik_info][0],"je prethodno bio prijavljen",d[korisnik_info][3])
                print('\n')

            elif ad == '5':
                os.system(clear)
                t_r_find = str(input('Unesite Tekuci Racun(12 cifara) : '))

                if t_r_find in d.keys():
                    print("Status naloga : Aktiviran")
                    print("Ime i Prezime :",d[t_r_find][0])
                    print("Pin :",d[t_r_find][1])
                    print("Stanje Racuna :","{:,}".format(d[t_r_find][2]))

                elif ("#"+t_r_find) in d.keys():
                    print("Status naloga : Ugasen")
                    print("Ime i Prezime :",d[("#"+t_r_find)][0])
                    print("Pin :",d[("#"+t_r_find)][1])
                    print("Stanje Racuna :","{:,}".format(d[("#"+t_r_find)][2]))

                else:
                    os.system(clear)
                    print("Nalog nije pronadjen.")

            elif ad == '6':
                os.system(clear)
                return gasenje_naloga()
            elif ad == '7':
                os.system(clear)
                grafikon() 
                return admin_block(t_r)


            ad = input("1. Broj korisnika \n2. Broj aktivnih naloga \n3. informacije o aktivnim korisnicima  \n4. Aktivnosti korisnika \n5. Pronadji nalog \n6. Ugasite nalog \n7. grafikon\n0. Izlaz\n")
        os.system(clear)
        return login_user()

    else:
        os.system(clear)
        return login_user()

try:
    os.system(clear)
    login_user()

except Exception as exc:
    os.system(clear)
    print ("Doslo je do greske: %s" %exc)
    print ("Izvinjavamo se.\nDovidjenja!")
