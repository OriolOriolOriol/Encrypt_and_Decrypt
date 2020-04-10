from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random,sys
import getpass
import pyttsx3 

line="#insert_your_personal_password"
nome_script, primo = sys.argv

#LEGGERE IL FILE DECRIPTATO
def read():
    file=open("pass.txt", 'r')
    Testo=file.read()
    print (Testo)
    file.close()

#FUNZIONE PER CRIPTARE IL FILE
def encrypt(key, filename):
        chunksize = 64 * 1024
        outFile = os.path.join(os.path.dirname(filename), "(encrypted)"+os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = ''
        for i in range(16):
                IV += chr(random.randint(0, 0xFF))
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(filename, "rb") as infile:
                with open(outFile, "wb") as outfile:
                        outfile.write(filesize)
                        outfile.write(IV)
                        while True:
                                chunk = infile.read(chunksize)
                               
                                if len(chunk) == 0:
                                        break
 
                                elif len(chunk) % 16 !=0:
                                        chunk += ' ' *  (16 - (len(chunk) % 16))
 
                                outfile.write(encryptor.encrypt(chunk))



#FUNZIONE PER DECRIPTARE IL FILE
def decrypt(key, filename):
        outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
        chunksize = 64 * 1024
        with open(filename, "rb") as infile:
                filesize = infile.read(16)
                IV = infile.read(16)
                decryptor = AES.new(key, AES.MODE_CBC, IV)
               
                with open(outFile, "wb") as outfile:
                        while True:
                                chunk = infile.read(chunksize)
                                if len(chunk) == 0:
                                        break
 
                                outfile.write(decryptor.decrypt(chunk))
 
                        outfile.truncate(int(filesize))      

#FUNZIONE PRINCIPALE

go=1
while go==1:
    engine=pyttsx3.init()
    engine.setProperty('volume', 0.9)
    password= getpass.getpass()
    password=primo

    
    
    if password!=line:
        engine.say("Passowrd Errata")
        print("Password Errata \n")
        engine.runAndWait()
                
    else:
        engine.say("Passowrd Corretta")
        print("Password Corretta \n")
        engine.runAndWait()
        if os.path.exists('C:\\Users\\claud\\Desktop\\KIRA\\PROGETTO__KIRA\\BOT_TELEGRAM\\pass.txt'):
            filename ="pass.txt"
                    
            if os.path.basename(filename).startswith("(encrypted)"):  #startswith controlla che la stringa inizi con "(encrypted)"
                engine.say("Faile gia' criptato...")
                engine.runAndWait()
                print ("File gia' criptato...\n")
                pass
                
            else:
                encrypt(SHA256.new(password).digest(), str(filename))
                engine.say("Faile criptato con successo")
                print ("File %s criptato  con successo " %str(filename))
                engine.runAndWait()
            engine.runAndWait()
        else:
            filename = "(encrypted)pass.txt"
            if not os.path.exists(filename):
                engine.say("Il faile non esiste...\n Hai sbagliato a scriverlo oppure non esiste proprio")
                print("Il file non esiste...\n Hai sbagliato a scriverlo oppure non esiste proprio\n") 
                engine.runAndWait()
                sys.exit(0)

            elif not filename.startswith("(encrypted)"):
                engine.say("Il faile non e' stato criptato")
                print ("Il file non e' stato criptato..\n")
                engine.runAndWait()
                sys.exit()

            else:
                decrypt(SHA256.new(password).digest(),str(filename))
                engine.say("Faile decriptato con successo")
                print ("File %s decriptato con successo " %str(filename))
                print("\n")
                read()
                os.remove(filename)
                engine.runAndWait()

    

    engine.say("Vuoi fare altre operazioni?")
    engine.runAndWait()
    continuare=input("Vuoi fare altre operazioni(si/no)?: ")
    if continuare=="no":
        sys.exit()
            
  

