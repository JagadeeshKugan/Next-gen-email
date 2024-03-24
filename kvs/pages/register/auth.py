import os
from firebase import firebase
from kvs.support.helper import Helper

firebase = firebase.FirebaseApplication('https://email-app-ba7ad-default-rtdb.firebaseio.com/', None)

class auther:
    data = {
    "email": "jaganchandru1568@gmail.com"
    ,"password": "Jagan1568"
    ,"code": "hbcvabvbaivdivnS"
    ,"codeword": "4312"
}
    

    def register(data):
        result = firebase.get('email-app-ba7ad-default-rtdb/Users','')
        passwrd = data["password"]
        hashed = Helper.Hash(passwrd) 
        data["password"] = hashed
        val = False
        codeword = Helper.rand()
        for i in  result.keys():
            if data["email"] == result[i]["email"]:
                print("email already exists")
                val = True                    
            if codeword == result[i]["codeword"]:
                codeword = Helper.rand()
        data.update({"codeword":codeword}) 
        Helper.speak( "Your code is "+str(codeword))
        print(data)
        res =""
        print(result)
        if val == False:
            firebase.post('email-app-ba7ad-default-rtdb/Users',data)
            print("added")
            res = "success"
        else:
            res = "user exists"
            print("user exist")
        result = firebase.get('email-app-ba7ad-default-rtdb/Users','')
        print(result)
        return res,codeword
    
    def loginwithcode(val):
        res = []
        try:
           
            result = firebase.get('email-app-ba7ad-default-rtdb/Users','')
            print(val)
            for i in result.keys():
                
                if result[i]["codeword"]==int(val):
                    print("fff")
                    res.append("success")
                    res.append(True)
                    res.append(result[i]["code"])
                    res.append(result[i]["email"])
                    res.append(result[i]["password"])
                    print(res,"ss")
                    return res
            
        except:
            print("error")
            return res
        
    def login(data):
        try:
            result = firebase.get('email-app-ba7ad-default-rtdb/Users','')
            print(result)
            for i in result.keys():
                print(result[i]["email"])
                password = data["password"]
                 
                hashed = Helper.Hash(password) 
                
                if data["email"] == result[i]["email"]:
                    if hashed == result[i]["password"]:
                        code = result[i]["code"]
                        return "success",True,code
        except : 
            print("error")

        return "null",False



