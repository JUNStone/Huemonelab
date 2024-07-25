import EncryptCore
import os
import time

def GenerateKey():
    print('Enter directory in which to save the key(empty if you want to store in {0}): '.format(os.getcwd()), end='')
    directory = input()
    os.chdir(directory)

    print('Enter file in which to save the key: ', end='')
    keyFileName = input()
    print('Generating public/private rsa key pair...')
    EncryptCore.RSAInitialize(True, keyFileName)

    print("{0} and {1} have generated in {2}".format(keyFileName+".pub", keyFileName+".pvk", directory))
    print("If you do encryption/decryption, will be executed in RSA2048.")
    print("!!! Please take care of keeping public/private key !!!")
    print("If you lose it, it will never given again.")

def EncryptFiles():
    print('Enter the directory where a public key file placed: ', end='')
    directory = input()
    os.chdir(directory)

    print('Enter the name of public key file(include file extension): ', end='')
    keyFileName = input()
    # NOTE: files with no extension will be disabled
    # if ".pub" not in keyFileName:
    #     keyFileName += ".pub"
    pub = EncryptCore.RSAGetPublicKey(keyFileName)
    if pub == None:
        print('Wrong file! Please check file and try again.')
        return None
    
    print('Public key recognized successfully!')
    time.sleep(0.5)
    
    print('Enter the directory to encrypt.')
    print('NOTE: ALL FILES in directory will be encrypted.')
    dirToEncrypt = input()
    EncryptCore.EncryptFiles(pub, dirToEncrypt)    

def DecryptFiles():
    print('Enter the directory where a private key file placed: ', end='')
    directory = input()
    os.chdir(directory)

    print('Enter the name of private key file(include file extension): ', end='')
    keyFileName = input()
    # NOTE: files with no extension will be disabled
    # if ".pvk" not in keyFileName:
    #     keyFileName += ".pvk"
    pvk = EncryptCore.RSAGetPrivateKey(keyFileName)
    if pvk == None:
        print('Wrong file! Please check file and try again.')
        return None
    
    print('Private key recognized successfully!')
    time.sleep(0.5)
    
    print('Enter the directory to decrypt.')
    print('NOTE: ALL FILES in directory will be decrypted.')
    dirToDecrypt = input()
    EncryptCore.DecryptFiles(pvk, dirToDecrypt)

def MainLoop() :
    while True:
        print("******************** Select Mode ********************")
        print("1. Generate Key(G)")
        print("2. Encrypt files(E)")
        print("3. Decrypt files(D)")
        print("4. Quit(Q)")
        print("!!! Input only a number or a capital letter !!!")
        print("Enter the mode: ", end='')
        mode = input()
        if mode == "1" or mode == "G" :
            GenerateKey()
        elif mode == "2" or mode == "E":
            EncryptFiles()
        elif mode == "3" or mode == "D":
            DecryptFiles()
        elif mode == "4" or mode == "Q":
            print("Bye bye~")
            break
        else:
            print("Wrong Input. please try again.")
            time.sleep(1.5)