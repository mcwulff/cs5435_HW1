from bottle import (
    get,
    post,
    redirect,
    request,
    response,
    jinja2_template as template,
)

from app.models.user import create_user, get_user
from app.models.session import (
    delete_session,
    create_session,
    get_session_by_username,
    logged_in,
)

from app.models.breaches import get_breaches
from app.scripts.breaches import load_breaches

from app.util.hash import (hash_sha256, hash_pbkdf2, random_salt)


@get('/login')
def login():
    return template('login')

@post('/login')
def do_login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    error = None
    user = get_user(db, username)
    #Mine
    password = hash_pbkdf2(password, user.salt)
    print(user)
    if (request.forms.get("login")):
        if user is None:
            response.status = 401
            error = "{} is not registered.".format(username)
        elif user.password != password:
            response.status = 401
            error = "Wrong password for {}.".format(username)
        else:
            pass  # Successful login
    elif (request.forms.get("register")):
        if user is not None:
            response.status = 401
            error = "{} is already taken.".format(username)

######################## My Code ############################################

        #p,h,s = get_breaches(db, username)
        #print(p)

        #for i in range(len(p)):
            #if(password == p[i,password]):
                #error = "User/Password Combo Found in Breach"

        #hp = hash_sha256(password)
        #for i in range(len(h)):
            #if(hp == h[i, hashed]):
                #error = "User/Password Combo Found in Breach"

        #for i in range(len(s)):
           #sp = hash_pbkdf2(password, s[i][2])
           # if (sp == s[i][1]):
                #error = "User/Password Combo Found in Breach"

 ###################### My Code #############################################           
 ##Mine
        create_user(db, username, password)
    else:
        response.status = 400
        error = "Submission error."
    if error is None:  # Perform login
        existing_session = get_session_by_username(db, username)
        if existing_session is not None:
            delete_session(db, existing_session)
        session = create_session(db, username)
        response.set_cookie("session", str(session.get_id()))
        return redirect("/{}".format(username))
    return template("login", error=error)

@post('/logout')
@logged_in
def do_logout(db, session):
    delete_session(db, session)
    response.delete_cookie("session")
    return redirect("/login")


