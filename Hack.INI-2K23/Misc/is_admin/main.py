#!/usr/bin/env python3

#from flag import Flag
#from flag import notFlag
import re

pattern = r'^[a-zA-Z_]*$'

def valid(text):
    return  re.match(pattern, text) 

class User:
    def __init__(self):
        self.__admin = False

    def isAdmin(self):
        if self.__admin:
            print(Flag)
        else :
            print("self.__admin=",self.__admin)
            print(f"key={key} value={value}")
            #print(notFlag)
        exit()

user = User()

print("You only get one chance ...")
key = input("Key : ").strip()
value = input("Value : ").strip()


if valid(key) or valid(value):
    print("passed")
    setattr(user,key,value)

user.isAdmin()
