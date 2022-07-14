from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db

app = Flask(__name__)
users = web.UserStore()
version = "1.4.2"

@app.route("/")
def index():
    vists = db["vists"]
    name = web.auth.name
    if name != "":
        if name != "GoodVessel92551":
            db["vists"] = vists + 1
        return redirect("/home")
    else:
        db["vists"] = vists + 1
        return render_template("index.html", version=version)
    


@app.route("/home")
@web.authenticated
def home():
    name = web.auth.name
    names = db["names"]
    online = db["online"]
    try:
        color = users.current["color"]
    except:
        users.current["color"] = ["#f6600","#a8531a"]
    if name not in names:
        users.current["color"] = ["#f6600","#a8531a"]
        users.current["time"] = [0,10,0]
        names.append(name)
        db["names"] = names
    else:
        if name in online:
            online.remove(name)
        online.append(name)
        print(online)
        db["online"] = online
    return render_template("home.html", name=name, version=version, color=color)


@app.route("/admin")
@web.authenticated
def admin():
    name = web.auth.name
    if name == "GoodVessel92551":
        user = db["names"]
        views = db["vists"]
        users2 = db["names2"]
        views2 = db["vists2"]
        user = len(user)
        db["names2"] = user
        db["vists2"] = views
        color = users.current["color"]
        return render_template("admin.html", color=color,name=name,users=user,views=views,users2=users2,views2=views2, version=version)
    else:
        return render_template("no.html")


@app.route("/admin/users")
@web.authenticated
def adminusers():
    name = web.auth.name
    user = db["names"]
    online = db["online"]
    if name == "GoodVessel92551":
        color = users.current["color"]
        return render_template("users.html", color=color, name=name,online=online, users=user, version=version)
    else:
        return render_template("no.html")


@app.route("/admin/analytics")
@web.authenticated
def analytics():
    name = web.auth.name
    user = db["names"]
    views = db["vists"]
    bug = db["Bug"]
    feed = db["Feed"]
    bug = len(bug) / 3
    feed = len(feed) / 3
    user = len(user)
    if name == "GoodVessel92551":
        db["names2"] = user
        db["vists2"] = views
        color = users.current["color"]
        return render_template("analytics.html", color=color,name=name,users=user,views=views,bug=bug,feed=feed, version=version)
    else:
        return render_template("no.html")


@app.route("/admin/suggestions")
@web.authenticated
def feedback():
    name = web.auth.name
    user = db["names"]
    bug = db["Bug"]
    feed = db["Feed"]
    bug = len(bug) / 3
    feed = len(feed) / 3
    if name == "GoodVessel92551":
        color = users.current["color"]
        return render_template("suggestions.html", color=color,name=name, users=user,bug=bug,feed=feed, version=version)
    else:
        return render_template("no.html")


@app.route("/bugs", methods=["POST", "GET"])
@web.authenticated
@web.per_user_ratelimit(
    max_requests = 2,
    period = 600,
    get_ratelimited_res=(lambda left: f"Too many requests, try again after {left} sec"),
)
def setbugs():
    name = web.auth.name
    bug = db["Bug"]
    color = users.current["color"]
    if request.method == "POST":
        if len(bug)/3 > 100:
            return render_template("error.html",error="There are too meny bugs reports at the moment")
        else:
            title2 = request.form["title"]
            description2 = request.form["description"]
            if len(title2) > 41 or len(description2) > 121:
                return render_template("leng.html", name=name)
            elif len(title2) == 0 or len(description2) == 0:
                return render_template("error.html",error="Put something in you bug report")
            else:
                bug.append(profanity.censor(title2))
                bug.append(profanity.censor(description2))
                name2 = web.auth.name
                bug.append(name2)
                db["Bug"] = bug
                
                return redirect("/home")
    else:
        return render_template("makebug.html", color=color, name=name, version=version)


@app.route("/admin/suggestions/bugs/get", methods=["GET", "POST"])
@web.authenticated
def get_bugs():
    color = users.current["color"]
    bug = db["Bug"]
    name = web.auth.name
    if request.method == "POST":
        bug = []
        db["Bug"] = bug
        return redirect("/admin/suggestions")
    elif name == "GoodVessel92551":
        return render_template("getbug.html", color=color, name=name, bug=bug)

    else:
        return render_template("no.html")


@app.route("/admin/alive")
@web.authenticated
def alive():
    return render_template("no.html")


@app.route("/number")
@web.authenticated
def number():
    color = users.current["color"]
    name = web.auth.name
    return render_template("number.html", color=color, name=name, version=version)


@app.route("/feedback", methods=["POST", "GET"])
@web.authenticated
@web.per_user_ratelimit(
    max_requests = 2,
    period = 600,
    get_ratelimited_res=(lambda left: f"Too many requests, try again after {left} sec"),
)
def setfeed():
    color = users.current["color"]
    name = web.auth.name
    bug = db["Feed"]
    if request.method == "POST":
        if len(bug)/3 > 100:
            return render_template("error.html",error="There are too meny feedback suggestions at the moment")
        else:
            title2 = request.form["title"]
            description2 = request.form["description"]
            if len(title2) > 41 or len(description2) > 121:
                return render_template("leng.html", name=name)
            elif len(title2) == 0 or len(description2) == 0:
                return render_template("error.html",error="Please put something in you feedback suggestion")
            else:
                bug.append(profanity.censor(title2))
                bug.append(profanity.censor(description2))
                name2 = web.auth.name
                bug.append(name2)
                db["Feed"] = bug
                return redirect("/home")
    else:
        return render_template("makefeed.html", color=color, name=name, version=version)


@app.route("/admin/suggestions/feedback/get", methods=["GET", "POST"])
@web.authenticated
def get_feed():
    color = users.current["color"]
    feed = db["Feed"]
    name = web.auth.name
    if request.method == "POST":
        feed = []
        db["Feed"] = feed
        return redirect("/admin/suggestions")
    elif name == "GoodVessel92551":
        return render_template("getfeed.html", color=color, name=name, feed=feed)


@app.route("/time/time")
@web.authenticated
def time():
    color = users.current["color"]
    name = web.auth.name
    return render_template("time.html", color=color, name=name, version=version)


@app.route("/calculator")
@web.authenticated
def maths():
    color = users.current["color"]
    name = web.auth.name
    return render_template("maths.html", color=color, name=name, version=version)


@app.route("/tasks", methods=["GET", "POST"])
@web.authenticated
def tasks():
    color = users.current["color"]
    name = web.auth.name
    try:
        users.current["tasks"]
    except:
        users.current["tasks"] = []
        users.current["tasks_id"] = 0
        tasks = users.current["tasks"]
    else:
        tasks = users.current["tasks"]
    return render_template("tasks.html", color=color, name=name, tasks=tasks, version=version)


@app.route("/tasks/make", methods=["GET", "POST"])
@web.authenticated
def task_make():
    color = users.current["color"]
    name = web.auth.name
    if request.method == "POST":
        if len(users.current["tasks"]) / 3 < 2:
            id = users.current["tasks_id"]
            tasks = users.current["tasks"]
            title = request.form["title"]
            description = request.form["description"]
            tasks.append(title.title())
            tasks.append(description)
            tasks.append(int(id))
            users.current["tasks_id"] = id + 1
            users.current["tasks"] = tasks
            return redirect("/tasks")
        else:
            return render_template("error.html",error="You have used up all of your task slots")
    else:
        return render_template("maketasks.html", color=color, name=name, version=version)


@app.route("/tasks/complete", methods=["GET", "POST"])
@web.authenticated
def task_remove():
    color = users.current["color"]
    name = web.auth.name
    if request.method == "POST":
        tasks = users.current["tasks"]
        id = request.form["id"]
        for i in range(len(tasks)):
            if tasks[i] == int(id):
                tasks.pop(i)
                tasks.pop(i - 1)
                tasks.pop(i - 2)
                users.current["tasks"] = tasks
                break
        return redirect("/tasks")
    else:
        return render_template("removetasks.html", color=color, name=name, version=version)


@app.route('/sw.js', methods=['GET'])
def sw():
    return current_app.send_static_file('sw.js')

@app.route("/time/countdown-timer")
@web.authenticated
def countdown_timer():
    color = users.current["color"]
    name = web.auth.name
    countdown = users.current["time"]
    return render_template("countdown.html", color=color, name=name,time=countdown, version=version)

@app.route("/time/countdown/make", methods=["GET", "POST"])
@web.authenticated
def countdown_make():
    color = users.current["color"]
    name = web.auth.name
    if request.method == "POST":
        time = []
        hour = request.form["hour"]
        min = request.form["min"]
        sec = request.form["sec"]
        try:
            int(hour)
            int(min)
            int(sec)
        except:
            return "You need to enter a number"
        else:
            if hour == "" or min == "" or sec == "":
                return render_template("error.html",error="Enter a number")
            elif int(hour) > 24 or int(sec) > 60 or int(min) > 60 or int(hour) < 0 or int(sec) < 0 or int(min) < 0:
                return render_template("error.html",error="One of the numbers is to big or small")
            else:
                time.append(hour)
                time.append(min)
                time.append(sec)
                print(time)
                users.current["time"]=time
                return redirect("/time/countdown")
    else:
        return render_template("makecoutdown.html", color=color, name=name, version=version)

@app.route("/time/stopwatch")
@web.authenticated
def stopwatch():
    color = users.current["color"]
    name = web.auth.name
    return render_template("stopwatch.html", color=color, name=name, version=version)

@app.route("/time")
@web.authenticated
def time_home():
    color = users.current["color"]
    name = web.auth.name
    return render_template("time_home.html", color=color, name=name, version=version)
    
@app.route("/changelog")
@web.authenticated
def changelog():
    color = users.current["color"]
    name = web.auth.name
    return render_template("change.html", color=color, name=name, version=version)

@app.route("/shell")
@web.authenticated
def shell():
    color = users.current["color"]
    name = web.auth.name
    return render_template("shell.html", color=color, name=name)

@app.route("/games")
@web.authenticated
def games():
    color = users.current["color"]
    name = web.auth.name
    return render_template("game.html", color=color, name=name, version=version)


@app.route("/color", methods=["GET", "POST"])
@web.authenticated
def color():
    color = users.current["color"]
    name = web.auth.name
    if request.method == "POST":
        color_1 = request.form["color1"]
        color_2 = request.form["color2"]
        print(color_1+" "+color_2)
        users.current["color"] = [color_1,color_2]
        return redirect("/home")
    else:
        return render_template("make_color.html", color=color, name=name, version=version)




web.run(app, port=8080, debug=True)
