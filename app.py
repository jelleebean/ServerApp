from typing import Final
from flask import Flask, render_template, session, redirect, request, flash
# from requests.auth import HTTPBasicAuth
import sqlite3


app = Flask(__name__)
app.secret_key = b'my little secret'

DBNAME: Final[str] = "./sqlite0.db"


@app.route("/")
def firstrun():
    return render_template('indexblock.html')


@app.route("/addservices")
def availableServices():
    DB = DBNAME
    conn = sqlite3.connect(DB)

    availableServices = None

    if 'username' in session:
        print("Show available services")

        availableServicesCursor = getAvailServices(conn)

        availableServices = availableServicesCursor.fetchall()
    else:
        return (redirect("/signin"))

    return (render_template("availservicesblock.html", availServices = availableServices))


@app.route("/dashboard")
def dashboard():
    servicesExist = False

    if 'username' in session:
        print("Show Dashboard")
        conn = sqlite3.connect(DBNAME)

        userServicesCursor = getUserServices(conn, session['id'])

        userServices = userServicesCursor.fetchall()

        if userServices is not None:
            print("No services")
        else:
            print("services exists")
            servicesExist = True
    else:
        print("Redirect to signin")
        return redirect("/signin")

    if servicesExist:
        return(render_template("dashboardblock.html"))
    else:
        return(render_template("dashboardemptyblock.html"))


@app.route("/signin")
def signin():
    if 'username' in session:
        print("signin: You're logged in")
    else:
        print("sigin: You need to login")
    return render_template('signinblock.html')


@app.route("/authenticate", methods=['POST', 'GET'])
def authenticate():

    DB = DBNAME
    conn = sqlite3.connect(DB)

    valid = False
    url = "/signin"

    if request.method == 'POST':
        userExists = authenticateUserdb(conn, request.form['username'], request.form['password'])

        if  userExists is not None:
            session['username'] = request.form['username']
            session['id'] = userExists
            print("You have logged in")
            valid = True
        else:
            print("You credentials were incorrect")
            removeSession()

    if valid == True:
        url = "/"

    return(redirect (url))


@app.route("/signout")
def signout():
    removeSession()
    print("Logged out..redirecting")
    return redirect(('/'))


def removeSession():
    if session.get('username'):
        session.pop('username')

    if session.get('id'):
        session.pop('id')


# @app.route("/clienta")
# def another():
#     result = requests.get("http://10.88.0.45")
#     return(result.text)

# @app.route('/overview')
# def overview():
#     result = request.get("https://traefik.localhost/api/overview", verify=False,
#                           auth = HTTPBasicAuth('admin-traefik-jl', 'me2i812'))
#     return(result.text)


def getUserServices(conn, userid):
    cursor = conn.cursor()

    userServicesSql = "SELECT * from user_service where id_user = ?;"

    userServices = cursor.execute(userServicesSql, (userid, ))

    print("userServices:", userServices)

    return userServices


def getAvailServices(conn):
    cursor = conn.cursor()

    availServicesSql = "SELECT * from avail_service;"

    availableServices = cursor.execute(availServicesSql)

    return availableServices


def authenticateUserdb(conn, username, password):
    status = None

    cursor = conn.cursor()

    authsql = "SELECT username, password, id FROM user WHERE username = '" + username + "' AND password = '" + password + "';"

    usernameExists = cursor.execute(authsql)


    username = usernameExists.fetchone()

    if username is not None:
        status = username[2]
    return status


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)

