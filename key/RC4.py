#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: @manojpandey

# Python 3 implementation for RC4 algorithm
# Brief: https://en.wikipedia.org/wiki/RC4

# Will use codecs, as 'str' object in Python 3 doesn't have any attribute 'decode'
import codecs
import string
import secrets

MOD = 256

def KSA(key):
    ''' Key Scheduling Algorithm (from wikipedia):
        for i from 0 to 255
            S[i] := i
        endfor
        j := 0
        for i from 0 to 255
            j := (j + S[i] + key[i mod keylength]) mod 256
            swap values of S[i] and S[j]
        endfor
    '''
    key_length = len(key)
    # create the array "S"
    S = list(range(MOD))  # [0,1,2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values

    return S


def PRGA(S):
    ''' Psudo Random Generation Algorithm (from wikipedia):
        i := 0
        j := 0
        while GeneratingOutput:
            i := (i + 1) mod 256
            j := (j + S[i]) mod 256
            swap values of S[i] and S[j]
            K := S[(S[i] + S[j]) mod 256]
            output K
        endwhile
    '''
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    ''' Takes the encryption key to get the keystream using PRGA
        return object is a generator
    '''
    S = KSA(key)
    return PRGA(S)


def encrypt_logic(key, text):
    ''' :key -> encryption key used for encrypting, as hex string
        :text -> array of unicode values/ byte string to encrpyt/decrypt
    '''
    # For plaintext key, use this
    key = [ord(c) for c in key]
    # If key is in hex:
    # key = codecs.decode(key, 'hex_codec')
    # key = [c for c in key]
    keystream = get_keystream(key)

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    return ''.join(res)


def encrypt(key, plaintext):
    ''' :key -> encryption key used for encrypting, as hex string
        :plaintext -> plaintext string to encrpyt
    '''
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext)


def decrypt(key, ciphertext):
    ''' :key -> encryption key used for encrypting, as hex string
        :ciphertext -> hex encoded ciphered text using RC4
    '''
    ciphertext = codecs.decode(ciphertext, 'hex_codec')
    res = encrypt_logic(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')


def Rc4_key(key, text, cipher = 0):
    alphabet = string.ascii_letters + string.digits

    #print(key)
    #key = 'not-so-random-key'  # plaintext
    plaintext = text  # plaintext
    # encrypt the plaintext, using key and RC4 algorithm
    ciphertext = encrypt(key, plaintext)
    '''print('plaintext:', plaintext)
    print('ciphertext :', ciphertext)'''
    # ..
    # Let's check the implementation
    # ..
    #ciphertext = '2D7FEE79FFCE80B7DDB7BDA5A7F878CE298615476F86F3B890FD4746BE2D8F741395F884B4A35CE979'

    # change ciphertext to string again
    decrypted =" "
    try:
        decrypted = decrypt(key, text)
        print(11111111111)
    except:
        pass
    #print('decrypted:', decrypted)

    if cipher:
        #print('\nCongrats ! You made it.')
        return ciphertext
    elif not cipher :
        return decrypted
    else:
        #print('Shit! You pooped your pants ! .-.')
        pass

    # until next time folks !


def test():

    # Test case 1
    # key = '4B6579' # 'Key' in hex
    # key = 'Key'
    # plaintext = 'Plaintext'
    # ciphertext = 'BBF316E8D940AF0AD3'
    assert(encrypt('Key', 'Plaintext')) == 'BBF316E8D940AF0AD3'
    assert(decrypt('Key', '8A7D0EB37F9974FF8FF9DA0839245D25B37B1C91828815B4BE9148')) == 'Plaintext'

    # Test case 2
    # key = 'Wiki' # '57696b69'in hex
    # plaintext = 'pedia'
    # ciphertext should be 1021BF0420
    assert(encrypt('Wiki', 'pedia')) == '1021BF0420'
    assert(decrypt('Wiki', '1021BF0420')) == 'pedia'

    # Test case 3
    # key = 'Secret' # '536563726574' in hex
    # plaintext = 'Attack at dawn'
    # ciphertext should be 45A01F645FC35B383552544B9BF5
    assert(encrypt('Secret','Attack at dawn')) == '45A01F645FC35B383552544B9BF5'
    assert(decrypt('Secret','45A01F645FC35B383552544B9BF5')) == 'Attack at dawn'

if __name__ == '__main__':
    main()