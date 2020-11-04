from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.policytree import PolicyParser
from charm.toolbox.node import *
import json
import random
import csv, ast
from charm.core.math.integer import integer,serialize,deserialize
import pickle

import flask
from flask import request, jsonify
import json
import time
import csv
app = flask.Flask(__name__)
app.config["DEBUG"] = True

class ABS:
    '''
    2B done
    '''
    def __init__(self,group):
        self.group = group

    def trusteesetup(self, attributes):
        '''
        Run by signature trustees
        returns the trustee public key

        Notice: Certain variables have been removed completely.
        G and H are handled by G1 and G2 type generators respectively,
        and the hash function is a generic one for the curve and can
        be derived from the group attribute.

        Attributes have to be appended to the end for global-ness
        '''
        tpk = {}
        tmax = 2*len(attributes)

        tpk['g'] = self.group.random(G1)
        
        for i in range(tmax+1): #provide the rest of the generators
            tpk['h{}'.format(i)] = self.group.random(G2)

        attriblist = {}
        counter = 2
        for i in attributes:
            attriblist[i] = counter
            counter += 1

        tpk['atr'] = attriblist
        
        return tpk

    def authoritysetup(self, tpk):
        '''
        Run by attribute-giving authority, takes tpk as parametre
        returns attribute master key and public key
        '''
        ask = {}
        apk = {}
        tmax = 2 * len(tpk['atr'])

        group = self.group
        a0,a,b = group.random(ZR), group.random(ZR), group.random(ZR)
        ask['a0'] = a0
        ask['a'] = a
        ask['b'] = b
        ask['atr'] = tpk['atr'] #this is for ease of usage

        apk['A0'] = tpk['h0'] ** a0
        for i in range(1,tmax+1): #rest of the whateverifys
            apk['A{}'.format(i)] = tpk['h{}'.format(i)] ** a

        for i in range(1,tmax+1):
            apk['B{}'.format(i)] = tpk['h{}'.format(i)] ** b

        apk['C'] = tpk['g'] ** group.random(ZR) #C = g^c at the end

        return ask,apk

    def generateattributes(self, ask, attriblist):
        '''
        returns signing key SKa
        '''
        ska = {}

        Kbase = self.group.random(G1) #"random generator" within G
        ska['Kbase'] = Kbase

        ska['K0'] = Kbase ** (1/ask['a0'])

        for i in attriblist:
            number = ask['atr'][i]
            ska['K{}'.format(number)] = Kbase ** (1 / (ask['a'] + number * ask['b']))

        return ska

    def sign(self, pk, ska, message, policy): #pk = (tpk,apk)
        '''
        return signature
        '''
        tpk,apk = pk
        lambd = {}

        M,u = self.getMSP(policy, tpk['atr'])

        mu = self.group.hash(message+policy)

        r = []
        for i in range(len(M)+1):
            r.append(self.group.random(ZR))

        lambd['Y'] = ska['Kbase'] ** r[0]
        lambd['W'] = ska['K0'] ** r[0]

        for i in range(1,len(M)+1):
            end = 0
            multi = ((apk['C'] * (tpk['g'] ** mu)) ** r[i])
            try: #this fills in for the v vector
                end = multi * (ska['K{}'.format(tpk['atr'][u[i-1]])] ** r[0])
            except KeyError:
                end = multi
            lambd['S{}'.format(i)] = end

        for j in range(1,len(M[0])+1):
            end = 0
            for i in range(1,len(M)+1):
                base = apk['A{}'.format(j)] * (apk['B{}'.format(j)] ** tpk['atr'][u[i-1]])
                exp = M[i-1][j-1] * r[i]
                end = end * (base ** exp)
            lambd['P{}'.format(j)] = end

        return lambd

    def verify(self, pk, sign, message, policy):
        '''
        return bool
        '''
        tpk,apk = pk
        M,u = self.getMSP(policy,tpk['atr'])

        mu = self.group.hash(message+policy)

        if sign['Y']==0 or pair(sign['Y'],tpk['h0']) != pair(sign['W'],apk['A0']):
            return False
        else:
            sentence = True
            for j in range(1,len(M[0])+1):
                multi = 0
                for i in range(1,len(M)+1):
                    a = sign['S{}'.format(i)]
                    b = (apk['A{}'.format(j)] * (apk['B{}'.format(j)] ** tpk['atr'][u[i-1]])) ** M[i-1][j-1]
                    multi = multi * pair(a,b)
                try:
                    after = pair(apk['C'] * tpk['g'] ** mu, sign['P{}'.format(j)])
                    pre = pair(sign['Y'],tpk['h{}'.format(j)])
                    if j == 1:
                        if multi != (pre * after):#after:
                            sentence = False
                    else:
                        if multi != (after):
                            sentence = False
                except Exception as err:
                    print(err)
            return sentence

    def getMSP(self,policy,attributes):
        '''
        returns the MSP that fits given policy

        utilizes the charm-crypto "policy -> binary tree" structure which has to be
        gone through only once

        target vector (1,0,....,0)
        '''
        u = {}
        counter = 0
        for i in attributes:
            u[counter] = i
            u[i] = counter
            counter += 1

        parser = PolicyParser()
        tree = parser.parse(policy)

        matrix = [] #create matrix as a dummy first (easy indexing)
        for i in range(len(attributes)):
            matrix.append([])

        counter = [1]
        def recursivefill(node,vector): #create MSP compatible rows
            if node.getNodeType() == OpType.ATTR:
                text = node.getAttribute()
                temp = list(vector)
                matrix[u[text]] = temp
            elif node.getNodeType() == OpType.OR:
                recursivefill(node.getLeft(),vector)
                recursivefill(node.getRight(),vector)
            else: #AND here, right?
                temp = list(vector)
                while(len(temp)<counter[0]):
                    temp.append(0)
                emptemp = []
                while(len(emptemp)<counter[0]):
                    emptemp.append(0)
                temp.append(1)
                emptemp.append(-1)
                counter[0] += 1
                recursivefill(node.getLeft(),temp)
                recursivefill(node.getRight(),emptemp)
        recursivefill(tree,[1])

        for i in matrix:
            while(len(i)<counter[0]):
                i.append(0)

        print(matrix)
        return matrix,u

    def encodestr(self, dicti):
        '''
        pairing group dict -> string
        for sending
        '''
        returnage = {}
        for i in dicti:
            returnage[i] = dicti[i]
            try:
                returnage[i] = self.group.serialize(returnage[i]).decode()
            except Exception:
                continue
        return json.dumps(returnage)

    def decodestr(self, stri):
        '''
        string -> pairing group dict
        for receiving
        '''
        dicti = json.loads(stri)
        for i in dicti:
            try:
                dicti[i] = self.group.deserialize(str.encode(dicti[i]))
            except Exception:
                continue
        return dicti

# if __name__ == "__main__":
    # group = PairingGroup('MNT159')
    # attributes = ['RIDWAN','32','AB','195','2020']

    # print('ATTRIBUTE TABLE: ',attributes)
    # absinst = ABS(group)
    
    # trustee_public_key = absinst.trusteesetup(attributes)
    
    # attribute_secret_key, attribute_public_key = absinst.authoritysetup(trustee_public_key)
    
    # signing_key = absinst.generateattributes(attribute_secret_key,['RIDWAN','32','AB','195','2020'])
    
    # sign = absinst.sign((trustee_public_key,attribute_public_key), signing_key, 'message', 'RIDWAN AND 32 AND AB AND 195 AND 2020')

    # trustee_public_key_encode = absinst.encodestr(trustee_public_key)
    # text_file = open("trustee_public_key.txt", "w")
    # n = text_file.write(trustee_public_key_encode)
    # text_file.close()

    # attribute_secret_key_encode = absinst.encodestr(attribute_secret_key)
    # text_file = open("attribute_secret_key.txt", "w")
    # n = text_file.write(attribute_secret_key_encode)
    # text_file.close()

    # attribute_public_key_encode = absinst.encodestr(attribute_public_key)
    # text_file = open("attribute_public_key.txt", "w")
    # n = text_file.write(attribute_public_key_encode)
    # text_file.close()

    # sign_encode = absinst.encodestr(sign)
    # text_file = open("sign.txt", "w")
    # n = text_file.write(sign_encode)
    # text_file.close()

    # file = open("sign.txt", "r")
    # b = file.read()
    # lam_decode = absinst.decodestr(b)
    
    # print("Generated trustee public key, attribute public key and sign")
    # print(absinst.verify((tpk,apk),lam_decode,'rar','RIDWAN'))
    
    # ska2 = absinst.generateattributes(ask,['RIDWAN','STUDENT'])
    # lam2 = absinst.sign((tpk,apk), ska2, 'rar', 'RIDWAN AND STUDENT')
    # print(absinst.verify((tpk,apk),lam2,'rar','RIDWAN AND STUDENT'))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/', methods=['POST'])
def verify_keys():
    print("api hit")
    # print(request.data)
    y = json.loads(request.data)
    # print("TPK\n")
    print(y['attributes'])
    print("-----------------------")
    print(y['tpk'])
    print("-----------------------")
    print(y['apk'])
    # print("SIGN\n")
    print("-----------------------")
    # print(y['sign'])
    
    attributes = y['attributes']
    attributes = sum([[i, 'AND'] for i in attributes], [])[:-1]
    predicate = ""
    for i in attributes:
        predicate = predicate + i +' '
    
    print(predicate)

    group = PairingGroup('MNT159')
    absinst = ABS(group)

    tpk = absinst.decodestr(y['tpk'])
    apk = absinst.decodestr(y['apk'])
    sign = absinst.decodestr(y['sign'])
    try:
        verification = str(absinst.verify((tpk,apk),sign,'message',predicate))
    except Exception:
        verification = "False"

    if verification=='True':
        response={"response":"True"}
    else:
        response={"response":"False"}
    return response


@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    print("api hit")
    # print(request.data)
    y = json.loads(request.data)
    id = y['id']
    tpk = y['tpk']
    apk = y['apk']
    sign = y['sign']
    attributes = y['attributes']

    print("******")
    print(id)

    print("Attributes from database: ", attributes)
    pred = attributes.split(" AND ")

    group = PairingGroup('MNT159')
    absinst = ABS(group)

    tpk = absinst.decodestr(y['tpk'])
    apk = absinst.decodestr(y['apk'])
    sign = absinst.decodestr(y['sign'])
    start = time.time()
    try:
        verification = str(absinst.verify((tpk,apk),sign,'message',attributes))
    except Exception:
        verification = "False"
    end = time.time()
    time_diff = end - start
    csvRow = str(id) + "," + attributes + "," +str(len(pred))+","+str(time_diff) + ","+verification

    with open('time.csv', 'a', newline='') as fd:
        fd.write("\n")
        fd.write(csvRow)

    print(verification)
    if verification=='True':
        response={"response":"True"}
    else:
        response={"response":"False"}
    return response

app.run(host='0.0.0.0', port=8004)