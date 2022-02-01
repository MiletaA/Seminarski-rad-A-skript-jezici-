import os, sys
import smtplib

def sendmail(adresa, msg, sbj = "BANKA"):
    clear = ('cls' if os.name == 'nt' else 'clear')
    try:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            print ("Molimo sačekajte...")
            server.starttls()
            server.login("sendermail112@gmail.com", "SenderMail123")
            os.system(clear)
            print ("Molimo sačekajte....")
            message = 'Subject: {}\n\n{}'.format(sbj, msg)
            server.sendmail("sendermail112@gmail.com", adresa, message)
            os.system(clear)
            print ("Molimo sačekajte.....")
            server.sendmail("sendermail112@gmail.com",str(adresa)+"\n"+str(msg))
            os.system(clear)
            print ("Molimo sačekajte......")
            server.quit()
            return True

        except Exception:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            os.system(clear)
            print ("Molimo sačekajte.....")
            server.starttls()
            server.login("sendermail112@gmail.com", "SenderMail123")
            os.system(clear)
            print ("Molimo sačekajte......")
            server.sendmail("sendermail112@gmail.com", str(adresa)+"\n"+str(msg))
            os.system(clear)
            print ("Molimo sačekajte.......")
            server.quit()
            return "Pogrešan mail"
    except Exception:
        return ""
        