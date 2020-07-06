from app import app
from flask import render_template, request, redirect, jsonify, make_response, abort
from datetime import datetime
import os
from werkzeug.utils import secure_filename

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/")
def index():

    # print(app.config["DB_NAME"])
    # abort(500)
    print(f"Flask ENV is set to: {app.config['ENV']}")

    return render_template("public/index.html")

@app.route("/jinja")
def jinja():

    my_name = "Sakshi"
    age = 23
    langs = ["Python", "Java", "Bash", "C"]
    family = {
        "Suresh": 50,
        "Sunita": 45,
        "Nitika": 21,
        "Nikhil": 18
    }

    colors = ("Red", "Green")
    cool = True

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pulling repo {self.name}"

        def clone(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template design tutorial",
        url="https://github.com/sakshi1918/Python-learning"
    )

    def repeat(x, qty):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>THIS IS MY HTML</h1>"

    suspicious = "<script>alert('You Got Hacked!')</script>"

    return render_template(
        "public/jinja.html", my_name=my_name, age=age,
        langs=langs, family=family, colors=colors,
        cool=cool, GitRemote=GitRemote, repeat=repeat,
        my_remote=my_remote, date=date, my_html=my_html,
        suspicious=suspicious
    )

@app.route("/about")
def about():
    return "<h1> Hello There!!!</h1>"


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}


@app.route("/profile/<username>")
def profile_old(username):

    user = None
    if username in users:
        user = users[username]


    return render_template("public/profile.html", username=username, user=user)

@app.route("/multiple/<foo>/<bar>/<baz>")
def multi(foo, bar, baz):
    return f"foo is {foo} bar is {bar} baz is {baz}"


@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()

        response = {
            "message": "JSON recieved",
            "name": req.get("name")
        }

        res = make_response(jsonify(response), 200 )

        return res
    else:
        res = make_response(jsonify({"message": "No JSON recieved"}), 400)
        '''
        make_response is helpful in adding extra headers to the response
        '''

        return res


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res
    

@app.route("/query")
def query():
    print(request.query_string)
    if request.args:
        args = request.args
        serialized = ", ".join(f"{k}: {v}" for k,v in args.items())

        return f"(Query) {serialized}", 200
    else:
        return "No query received", 200


app.config["IMAGE_UPLOADS"] = "/home/temp/Documents/gitHub_repos/Flask-learning/FlaskApp/app/static/img/uploads/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEF", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 *1024


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False



@app.route("/upload-image", methods=["GET","POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            # Validation for file size
            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("File excceded maximum size")
                return redirect(request.url)

            image = request.files["image"]

            # Validations in image
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image Saved")
                return redirect(request.url)

    return render_template("public/upload_image.html")


from flask import send_from_directory, abort

"""
string:
int:
float:
path:
uuid:
"""

app.config["CLIENT_IMAGES"] = "/home/temp/Documents/gitHub_repos/Flask-learning/FlaskApp/app/static/client/img"
app.config["CLIENT_CSV"] = "/home/temp/Documents/gitHub_repos/Flask-learning/FlaskApp/app/static/client/csv"
app.config["CLIENT_REPORTS"] = "/home/temp/Documents/gitHub_repos/Flask-learning/FlaskApp/app/static/client/reports"

@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], 
            filename=image_name, 
            as_attachment = False
            )
    except FileNotFoundError:
        abort(404)


@app.route("/get-csv/<filename>")
def get_csv(filename):
    try:
        return send_from_directory(
            app.config["CLIENT_CSV"], 
            filename=filename, 
            as_attachment = True
            )
    except FileNotFoundError:
        abort(404)


@app.route("/get-report/<path:path>")
def get_report(path):
    try:
        return send_from_directory(
            app.config["CLIENT_REPORTS"], 
            filename=path, 
            as_attachment = True
            )
    except FileNotFoundError:
        abort(404)


@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)

    cookies = request.cookies

    flavor = cookies.get("flavor")
    choc_type = cookies.get("choco_type")
    chewy = cookies.get("chewy")
    print(flavor, choc_type, chewy)



    res.set_cookie(
        "flavor",
        value="choco chip",
        max_age=5,
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False
        # samesite=False
        )

    res.set_cookie("chocolate type", "dark")
    res.set_cookie("chewy", "yes")

    return res

from flask import session, url_for

app.config["SECRET_KEY"] = "dcdl0YnqjJd5hUlfte3wFw"

user = {
    "sahil": {
        "username": "sahil",
        "email": "sahil@gmail.com",
        "password": "hithere",
        "bio": "Best Friend of Sakshi"
    },
    "sakshi": {
        "username": "sakshi",
        "email": "sakshi@gmai.com",
        "password": "helloji",
        "bio": "Best friend of sahil"
    }
}

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        req = request.form

        username = req.get("username")
        password = req.get("password")

        if username not in user:
            print("Username not found!")
            return redirect(request.url)
        else:
            us = user[username]

        if not password == us["password"]:
            print("Incorrect Password")
            return redirect(request.url)
        else:
            session["USERNAME"] = us["username"]
            print("User added to session")
            return redirect(url_for("profile"))
        

    return render_template("public/sign_in.html")

@app.route("/profile")
def profile():
    print(session)
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        us = user[username]
        
        return render_template("public/profile.html", user=us)
    else:
        print("Username not found in session")
        return redirect(url_for("sign_in"))


@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)

    return redirect(url_for("sign_in"))


# Message flashing (feedback)

from flask import flash

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        # special type of dict which gives the form data
        req = request.form
        print(req)
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")

        if not len(password) >= 10:
            flash("Password must be atleast 10 charaters in length", "danger")
            return redirect(request.url)

        flash("Account Created", "success")

        return redirect(request.url)

    return render_template("public/sign_up.html") 