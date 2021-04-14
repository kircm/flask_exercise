import sqlite3
from datetime import datetime
from datetime import timedelta

from flask import Flask, make_response
from flask import abort, url_for
from flask import request
from markupsafe import escape

app = Flask(__name__)
HOST_PORT = "http://127.0.0.1:5000"

connection = sqlite3.connect('snippets.db')
print("Opened database successfully")
connection.execute('CREATE TABLE IF NOT EXISTS snippets (name TEXT, expires_at datetime, snippet TEXT)')
connection.close


@app.route('/snippets', methods=['POST'])
def create_snippet():
    try:
        conn = sqlite3.connect('snippets.db')
        cur = conn.cursor()
        content = request.json
        name = content['name']

        existing = get_snippet_with_name(cur, name)
        if existing:
            conn.close()
            print("Snippet already exists in DB")
            abort(422)

        expires_in = content['expires_in']
        now = datetime.now()
        expires_at = now + timedelta(seconds=expires_in)
        snippet = escape(content['snippet'])
        cur.execute("INSERT INTO snippets (name,expires_at,snippet) VALUES(?, ?, ?)", (name, expires_at, snippet))
        conn.commit()

        new_snippet = get_snippet_with_name(cur, name)
        resp = make_response(new_snippet, 201)
        conn.close()
        return resp
    except Exception as e:
        if conn: conn.close()
        print(e)
        abort(400)


def get_snippet_with_name(cur, name):
    cur.execute("select name, expires_at, snippet from snippets where name = ?", (name,))
    snippet = cur.fetchone()
    if snippet:
        get_snippet_path = url_for('get_snippet', name=name)
        snippet_obj = {"url": f"{HOST_PORT}/{get_snippet_path}",
                       "name": f"{snippet[0]}",
                       "expires_at": f"{snippet[1]}",
                       "snippet": f"{snippet[2]}"}
        return snippet_obj
    else:
        return None


@app.route('/snippets/<name>', methods=['GET'])
def get_snippet(name=None):
    try:
        conn = sqlite3.connect('snippets.db')
        cur = conn.cursor()
        cur.execute("select snippet from snippets where name = ?", (name,))
        snippet = get_snippet_with_name(cur, name)
        if snippet:
            expires_at = snippet['expires_at']
            new_expires_at = datetime.fromisoformat(expires_at) + timedelta(seconds=30)
            cur.execute("UPDATE snippets SET expires_at=? WHERE name = ?", (new_expires_at, name))
            conn.commit()
            conn.close()
            return snippet
        else:
            abort(404)

    except Exception as e:
        if conn: conn.close()
        print(e)
        abort(404)
