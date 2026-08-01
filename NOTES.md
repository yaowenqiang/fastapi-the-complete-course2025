> uvicorn books:app --reload

> uvicorn books:app reload

> xh localhost:8000/books/book_one 

> %20 = space in a URL

> pip install sqlalchemy
> 
> sqlite> .mode column
  
> sqlite> .mode markdown
  
> sqlite> .mode box
  
> sqlite> .mode table

> sqlite3 will reuse the primary key if record is deleted
  
> pip install passlib
  
> pip install bcrypt==4.0.1
  
> pip install python-multipart

What is a JSON Web Token? 

+ JSON Web Token is a self-contained way to securely transmit data and information between two parties using a JSON Object.
+ JSON Web Token can be trusted because each JWT can be digitally signed, which in return allows the server to know if the JWT has been changed at all.
+ JWT should be used when dealing with authentication.
+ JWT is a great way for information to be exchanged between the server and client.

JSON web token structure 

+ A JSON Web Token is created of three separate parts separated by dots(.) which include:
  + Header:(a)
  + Payload:(b)
  + Signature:(c)

JWT Header

+ A JWT header usually consists of two parts:
  + (alg) the algorithm fo signing
  + 'typ' the specific type of token

The JWT header is then encoded using Base64 to create the first part of the JWT(a)

JWT Payload

A JWT Payload consists of the data.The payload data contains claims, and there are three different type of claims.

+ Registered
+ Public
+ Private

The JWT Payload is then encoded using Base64 to create the second part of the JWT

JWT Signature

A JWT Signature is created by using the algorithm in the header to hsah out the encoded header, encoded payload with secret.

The secret can be anything, but is save somewhere on the server that the client does not have access to

> https://www.jwt.io/

> uv pip install "python-jose[cryptography]"

> uv pip install python-jose

