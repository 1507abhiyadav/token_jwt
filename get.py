# import ctypes
# from dataclasses import fields
import email
from json import decoder
from lib2to3.pgen2 import token
from urllib import response
from wsgiref import headers
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from array import array
from distutils.log import error
from genericpath import exists
from http import server
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import json.decoder
from pickle import TRUE
from types import NoneType
from unicodedata import decimal, name
from gc import collect
from http import client
from xml.dom.minidom import Element
import pymongo
from bson import decode, encode, json_util, ObjectId
try:
	client=pymongo.MongoClient('mongodb://localhost:27017/')
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

mydb = client['employee']  # database name
collection = mydb['employee']  # collection name
collection_1 = mydb['user'] # collection name
HOST = "127.0.0.1"
PORT = 8000

# employee =[{
#   "id":1,
#   "name":"abhishek"
# },
# { "id":2,
#   "name":"rakesh"
# }]
# print(employee)
expires= datetime.now() + timedelta(hours=24) -timedelta(hours=5)-timedelta(minutes=30)
# expires= datetime.utcnow() + timedelta(minutes=2)

class ServerHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-type','text/json')
      # #reads the length of the Headers
      length = int(self.headers['Content-Length'])
      # #reads the contents of the request
      content = self.rfile.read(length)
      temp = str(content).strip('b\'')
      self.end_headers()
      return temp 

    def error_function(self):
      self.send_response(400)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      self.wfile.write("Email not found".encode())

    def error_find(self):
      self.send_response(400)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      # self.wfile.write("id  already exist".encode())
      self.wfile.write(("Email already exist").encode())


################## GET METHOD  ################------>

    def do_GET(self):
        # length = int(self.headers['Content-Length'])
        # # print(length)
        # # # reads the contents of the request
        # content = self.rfile.read(length)
        # temp = str(content).strip('b\'') # data come from postman as string, when the use method post
        # print(temp)       
        try:
            # obj = json.loads(temp) # data convert as object use json.loads
            # print(obj) 
            # all = collection.find_one({'id':obj['id']}) # find the id in the database
            # all = collection.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
            all = collection.find()
            # print(all)
            data_all = json.loads(json_util.dumps(all))
            if len(data_all) == 0:
                  self.send_response(200)
                  self.send_header('Content-type','text/json')
                  self.end_headers()
                  self.wfile.write(("[]").encode())
            if all !=None:
              var_token= self.headers['Authorization'] # get the token from the header
              # print(var_token)
              token = var_token.split(" ")[1]
              if token == None:
                self.send_response(401)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(("Token not found").encode())
              try:
                decode_data = jwt.decode(token,key="secret", algorithms=['HS256'])
                # print(decode_data)
                for i in data_all:
                  self.send_response(200)
                  self.send_header('Content-type','text/json')
                  self.end_headers()
                  self.wfile.write(json.dumps(i).encode())
              except jwt.ExpiredSignatureError:
                self.send_response(401)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(("Token expired").encode())

              except  Exception as e:
                self.send_response(401)
                self.send_header('Content-type','text/json')
                self.end_headers()
                self.wfile.write(("Invalid token").encode())
           
        except Exception as e:
            # print(e)
            self.send_response(400)
            self.send_header('Content-type','text/plain')
            self.end_headers() 
            self.wfile.write(("error massege:"+str(e)).encode())
        except:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.wfile.write(("internal error"+str(e)).encode())
            
####  Sign Up method defination----->

####POST method defination----->
    def do_POST(self):
        if self.path == "/signup":
            length = int(self.headers['Content-Length']) 
            # # reads the contents of the request
            content = self.rfile.read(length)
            temp = str(content).strip('b\'') # data come from postman as string, when the use method post
            # print(temp)
            try:
                obj = json.loads(temp)# data convert as object use json.loads
                # print(obj)
                all = collection_1.find_one({'email':obj['email']}) # find the email in the database
                # all = collection.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
                # print(all)
                if all == None:
                    collection_1.insert_one(obj)
                    self.send_response(200)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(("Successfully signup").encode())
                    # self.wfile.write((token).encode())
                else:
                    self.error_find()
            
            except Exception as e:
                # print(e)
                self.send_response(400)
                self.send_header('Content-type','text/plain')
                self.end_headers() 
                self.wfile.write(("error massege:"+str(e)).encode())
            except:
                self.send_response(500)
                self.send_header('Content-type','text/plain')
                self.wfile.write(("internal error"+str(e)).encode())

        elif self.path == "/login":
            length = int(self.headers['Content-Length']) 
            # # reads the contents of the request
            content = self.rfile.read(length)
            temp = str(content).strip('b\'') # data come from postman as string, when the use method post
            # print(temp)
            # obj = json.loads(temp)
            try:
                obj = json.loads(temp)# data convert as object use json.loads
                # print(obj)
                all = collection_1.find_one({'email':obj['email'],'password':obj['password']}) # find the email and password in the database
                # print(all)
                data= json.loads(json_util.dumps(all))
                # print(data)
                if data == None:
                  self.send_response(400)
                  self.send_header('Content-type','text/plain')
                  self.end_headers()
                  self.wfile.write(("Email or Password Invalid").encode())
                payload={
                    'email':data['email'],
                    'exp':expires
                }
                token = jwt.encode(payload, key = "secret", algorithm = "HS256")
                # print(token)
                en_data ={
                    "token":token,
                    "status":200,
                    "message":"Successfully login"
                }
                # collection.insert_one(obj)
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                # self.wfile.write(("successfully login").encode())
                self.wfile.write(json_util.dumps(en_data).encode())
            except Exception as e:
                # print(e)
                self.send_response(400)
                self.send_header('Content-type','text/plain')
                self.end_headers() 
                self.wfile.write(("error massege:"+str(e)).encode())
            except:
                self.send_response(500)
                self.send_header('Content-type','text/plain')
                self.wfile.write(("internal error"+str(e)).encode())


        elif self.path == "/post":
            length = int(self.headers['Content-Length']) 
            # # reads the contents of the request
            content = self.rfile.read(length)
            temp = str(content).strip('b\'') # data come from postman as string, when the use method post
            # print(temp)
            try:
                obj = json.loads(temp) # data convert as object use json.loads
                # print(obj) 
                all = collection.find_one({'email':obj['email']}) # find the id in the database
                # all = collection.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
                # print(all)
                if all == None:
                  var_token= self.headers['Authorization'] # get the token from the header
                  # print(var_token)
                  token = var_token.split(" ")[1]
                  # print(token)
                  if (token == None):
                    self.send_response(401)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(("Token not found").encode())
                  try:
                    var_decode = jwt.decode(token, key = "secret", algorithms = ['HS256'])
                  # print(var_decode)
                    collection.insert_one(obj)
                    self.send_response(200)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(("Successfully post").encode())
                    
                  except jwt.ExpiredSignatureError:
                      self.send_response(401)
                      self.send_header('Content-type','text/plain')
                      self.end_headers()
                      self.wfile.write(("Token expired").encode())

                  except  Exception as e:
                    self.send_response(401)
                    self.send_header('Content-type','text/json')
                    self.end_headers()
                    self.wfile.write(("Invalid token").encode())
                else:
                  self.error_find()        
            except Exception as e:
                # print(e)
                self.send_response(400)
                self.send_header('Content-type','text/plain')
                self.end_headers() 
                self.wfile.write(("error massege:"+str(e)).encode())
            except:
                self.send_response(500)
                self.send_header('Content-type','text/plain')
                self.wfile.write(("internal error"+str(e)).encode())

### PUT method defination----->

    def do_PUT(self):
      length = int(self.headers['Content-Length'])
      # reads the contents of the request
      content = self.rfile.read(length)
      temp = str(content).strip('b\'') # # data come from postman as string , when the use method put
      # print(temp)
      try:
        obj = json.loads(temp)  # data convert as object id =4
        data = collection.find_one({'email':obj['email']})
        if data != None:
          var_token= self.headers['Authorization'] # get the token from the header
          # print(var_token)
          token = var_token.split(" ")[1]
          if (token == None):
            self.send_response(401)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(("Token not found").encode())

          try:
            var_decode = jwt.decode(token, key = "secret", algorithms = ['HS256'])
            # print(var_decode)
            collection.update_one({'email':obj['email']},{'$set':obj})
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(("Data successfully update").encode())
          
          except jwt.ExpiredSignatureError:
            self.send_response(401)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(("Token expired").encode())
          except Exception as e:
            self.send_response(401)
            self.send_header('Content-type','text/json')
            self.end_headers()
            self.wfile.write(("Invalid token").encode())
        else:
          self.error_function()

      except Exception as e:
        # print(e)
        self.send_response(400)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(("error massge:"+str(e)).encode())
      except:
        self.send_response(500)
        self.send_header('Content-type','text/plain')
        self.wfile.write(("internal error"+str(e)).encode())
        
## DELETE method defination----->

    def do_DELETE(self):
      length = int(self.headers['Content-Length']) #returns the content length (value of the header) as a string. # <--- Gets the size of data
      # reads the contents of the request
      content = self.rfile.read(length) # <--- Gets the data itself
      temp = str(content).strip('b\'') # data come from postman as string , when the use method delete  
      try:
        obj = json.loads(temp)  # date convert as object 
        all = collection.find_one({'email':obj['email']})
        if all != None:
        # print(all)
          var_token= self.headers['Authorization'] # get the token from the header
          # print(var_token)
          token = var_token.split(" ")[1]
          if (token == None):
            self.send_response(401)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(("Token not found").encode())
          try:
            var_decode = jwt.decode(token, key = "secret", algorithms = ['HS256'])
            # print(var_decode)
            collection.delete_one({'email':obj['email']})
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(("Data successfully delete").encode())
          except jwt.ExpiredSignatureError:
            self.send_response(401)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(("Token expired").encode())
          except Exception as e:
            self.send_response(401)
            self.send_header('Content-type','text/json')
            self.end_headers()
            self.wfile.write(("Invalid token").encode())
        else:
          self.error_function()
          
        
      except Exception as e:
        # print(e)
        self.send_response(400)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(("error  massge:"+str(e)).encode())
      except:
        self.send_response(500)
        self.send_header('Content-type','text/plain')
        self.wfile.write(("internal error"+str(e)).encode())

server= HTTPServer((HOST,PORT),ServerHTTP)
print("Server is running on port 8000")
server.serve_forever() 
