# snippet handler

The base API has been implemented considering:

- the host and port is configurable in global var HOST_PORT which has
  default value: "http://127.0.0.1:5000"

- The DB connection is oppened and closed at each interaction with the user

- If a user tries to insert a new snippet with a name already present in DB
  an error 422 is returned 
  
