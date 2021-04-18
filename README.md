# snippet service

- Simple API to store and retireve snippets of text with an expiration date

- Usage:

```
export FLASK_APP=main.py
export FLASK_ENV=development

flask run
```


The base API has been implemented considering:

- the host and port is configurable in global var HOST_PORT which has
  default value: "http://example.com"

- The DB connection is oppened and closed at each interaction with the user

- If a user tries to insert a new snippet with a name already present in DB
  an error 422 is returned 
  
