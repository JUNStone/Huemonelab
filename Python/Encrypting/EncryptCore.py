import os
import rsa

def RSAInitialize(makeFile = True, keyFileName = "RSA") :
    '''
    Make a public key and private key.\n
    If {makeFile} is True, this function will make files of keys.\n
    File names will be "{keyFileName}.pub" and "{keyFileName}.pvk".\n
    returns a tuple of the public key and the private key.
    '''
    (publicKey, privateKey) = rsa.newkeys(2048)
    if makeFile:
        with open('{0}.pub'.format(keyFileName), 'w') as f:
            f.write('n:'+str(publicKey.n))
            f.write('\ne:'+str(publicKey.e))
        with open('{0}.pvk'.format(keyFileName), 'w') as f:
            f.write('n:'+str(privateKey.n))
            f.write('\ne:'+str(privateKey.e))
            f.write('\nd:'+str(privateKey.d))
            f.write('\np:'+str(privateKey.p))
            f.write('\nq:'+str(privateKey.q))
            #nedpq
    return (publicKey, privateKey)

def RSAGetPublicKey(keyFileName = "RSA.pub"):
    '''
    Get a public key that pre-generated.\n
    If there's no appropriate public key, this function will return None.
    '''
    pubKeyDict = dict()
    with open(keyFileName, 'r') as f:
        while True :
            s = f.readline()
            if not s :
                break
            s = s.split(':')
            if len(s) != 2:
                break
            pubKeyDict[s[0]] = s[1]
    
    n = int(pubKeyDict.get('n') or 0)
    e = int(pubKeyDict.get('e') or 0)
    if n != 0 and e != 0:
        return rsa.PublicKey(n, e)
    else :
        return None

def RSAGetPrivateKey(keyFileName = "RSA.pvk"):
    '''
    Get a private key that pre-generated.\n
    If there's no appropriate private key, this function will return None.
    '''
    pvKeyDict = dict()
    with open(keyFileName, 'r') as f:
        while True :
            s = f.readline()
            if not s :
                break
            s = s.split(':')
            if len(s) != 2:
                break
            pvKeyDict[s[0]] = s[1]
    n = int(pvKeyDict.get('n') or 0)
    e = int(pvKeyDict.get('e') or 0)
    d = int(pvKeyDict.get('d') or 0)
    p = int(pvKeyDict.get('p') or 0)
    q = int(pvKeyDict.get('q') or 0)
    #n,e,d,p,q = int(pvKeyDict.get('n') or 0), int(pvKeyDict.get('e') or 0), int(pvKeyDict.get('d') or 0), int(pvKeyDict.get('p') or 0), int(pvKeyDict.get('q') or 0)
    
    if n != 0 and e != 0 and d != 0 and p != 0 and q != 0:
        return rsa.PrivateKey(n,e,d,p,q)
    else :
        return None

def EncryptFiles(pub_key, dir = str | None, encodingType = 'utf-8'):
    '''
    Encrypt all files in {dir} by (RSA){pub_key}.\n
    Encrypted files will saved in "[filename].d/[filename].N.encrypted", N is counter starts from 0.\n
    If file has a extension with "encrypted" or "decrypted", will not encrypt.\n
    If file has a extension "d" or no extension, will not encrypt.\n
    This function will read/write files with {encodingType}.
    '''
    if type(dir) == str:
        os.chdir(dir)
    files = os.listdir()
    default_dir = os.getcwd()

    for file in files:
        output = file.split('.')
        doEncrypt = True
        if len(output) < 2 or output[len(output)-1] == "d" : doEncrypt = False
        for f in output:
            if "encrypted" in f or "decrypted" in f:
                doEncrypt = False
        if not doEncrypt : continue
        
        os.chdir(default_dir) # 기본 폴더를 작업 영역으로 지정
        txtFile = open(file, 'r', encoding=encodingType) #r,w,a
        os.makedirs(file + '.d', exist_ok=True, mode=777) # 파일별 폴더 생성
        os.chdir(default_dir + "/" + file + ".d") # 생성한 폴더를 작업 영역으로 지정
        
        print('Encrypting file:', file)
        ln = 0
        while True:
            line = txtFile.readline()
            if not line :
                break
            newFile = open(file + '.' + str(ln) + '.encrypted', 'wb')
            e = rsa.encrypt(line.encode(encodingType), pub_key)
            newFile.write(e)
            newFile.close()
            ln += 1
        
        txtFile.close()

def DecryptFiles(pvt_key, dir = str | None):
    '''
    Decrypt all files in {dir} by (RSA){pvt_key}.\n
    Detect folders(which stores encrypted files) with extension "d".\n
    List all the encrypted files that has a name of "[filename].d/[filename].N.encrypted",
    N is a counter starts from 0.\n
    If there's no [filename].0.encrypted, this function will end.
    '''
    if type(dir) == str:
        os.chdir(dir)
    files = os.listdir()
    default_dir = os.getcwd()

    for file in files:
        output = file.split('.')
        if len(output) < 2 or output[len(output)-1] != "d":
            continue

        try :
            os.chdir(default_dir + "/" + file)
        except :
            continue

        encrypted_files = os.listdir()
        base_file = ""
        for ef in encrypted_files:
            if '.0.encrypted' in ef :
                base_file = ef
                break
        if base_file == "" :
            return None
        
        decrypted_file = base_file.removesuffix('.0.encrypted')
        newFile = open(decrypted_file, 'w')
        
        decrypted_body = ""

        print('decrypting file:', decrypted_file)
        for i in range(len(encrypted_files)) :
            ef = decrypted_file + "." + str(i) + ".encrypted"
            if ef not in encrypted_files:
                print('there\'s no', ef)
                continue
            print('processing:', ef)
            e = open(ef, 'rb')
            line = b""
            while True:
                l = e.readline()
                if not l :
                    break
                line += l
            decrypted = rsa.decrypt(line, pvt_key)
            decrypted_body += decrypted.decode()
            e.close()

        newFile.write(decrypted_body)
        newFile.close()