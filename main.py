from better_profanity import profanity
from datetime import datetime
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db

app = Flask(__name__)
users = web.UserStore()
version = "1.0.1"

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
        return render_template("index.html")
    


@app.route("/home")
@web.authenticated
def home():
    name = web.auth.name
    names = db["names"]
    if name in names:
        pass
    else:
        users.current["time"] = [0,10,0]
        names.append(name)
        db["names"] = names
    return render_template("home.html", name=name, version=version)


@app.route("/admin")
@web.authenticated
def admin():
    name = web.auth.name
    users = db["names"]
    views = db["vists"]
    users2 = db["names2"]
    views2 = db["vists2"]
    print(users)
    users = len(users)
    if name == "GoodVessel92551":
        db["names2"] = users
        db["vists2"] = views
        return render_template("admin.html",name=name,users=users,views=views,users2=users2,views2=views2)
    else:
        return render_template("no.html")


@app.route("/admin/users")
@web.authenticated
def adminusers():
    name = web.auth.name
    users = db["names"]
    if name == "GoodVessel92551":
        return render_template("users.html", name=name, users=users)
    else:
        return render_template("no.html")


@app.route("/admin/analytics")
@web.authenticated
def analytics():
    name = web.auth.name
    users = db["names"]
    views = db["vists"]
    bug = db["Bug"]
    feed = db["Feed"]
    bug = len(bug) / 3
    feed = len(feed) / 3
    users = len(users)
    if name == "GoodVessel92551":
        db["names2"] = users
        db["vists2"] = views
        return render_template("analytics.html",name=name,users=users,views=views,bug=bug,feed=feed)
    else:
        return render_template("no.html")


@app.route("/admin/suggestions")
@web.authenticated
def feedback():
    name = web.auth.name
    users = db["names"]
    bug = db["Bug"]
    feed = db["Feed"]
    bug = len(bug) / 3
    feed = len(feed) / 3
    if name == "GoodVessel92551":
        return render_template("suggestions.html",name=name, users=users,bug=bug,feed=feed)
    else:
        return render_template("no.html")


@app.route("/bugs", methods=["POST", "GET"])
@web.authenticated
def setbugs():
    name = web.auth.name
    bug = db["Bug"]
    now = datetime.now()
    now2 = now.strftime("%y%m%d%H%M")
    now3_5 = now.strftime("%d/%m/%y %H:%M UTC")
    print(now3_5[9:11])
    i=int(now3_5[9:11])+1
    now3 = now3_5[0:7]+" "+str(i)+now3_5[11:]
    print(now3)
    try:
        cooldown = users.current["cooldown"]
    except:
        users.current["cooldown"]="N/A"
        cooldown = users.current["cooldown"]
        print("new")
    else:
        cooldown = users.current["cooldown"]
        if cooldown != "N/A":
            if int(now2)-int(cooldown[0:10]) < 100:
                return "You recenty posted a bug report or feedback suggestion please try again at: "+cooldown[10:]
    if request.method == "POST":
        if len(bug)/3 > 100:
            return "There are too meny bugs in the system please try again later :("
        else:
            title2 = request.form["title"]
            description2 = request.form["description"]
            if len(title2) > 41 or len(description2) > 121:
                return render_template("leng.html", name=name)
            elif len(title2) == 0 or len(description2) == 0:
                return "Please put something in you bug report"
            else:
                users.current["cooldown"] = now2+now3
                
                bug.append(profanity.censor(title2))
                bug.append(profanity.censor(description2))
                name2 = web.auth.name
                bug.append(name2)
                db["Bug"] = bug
                return redirect("/home")
    else:
        return render_template("makebug.html", name=name)


@app.route("/admin/suggestions/bugs/get", methods=["GET", "POST"])
@web.authenticated
def get_bugs():
    bug = db["Bug"]
    name = web.auth.name
    if request.method == "POST":
        bug = []
        db["Bug"] = bug
        return redirect("/admin/suggestions")
    elif name == "GoodVessel92551":
        return render_template("getbug.html", name=name, bug=bug)

    else:
        return render_template("no.html")


@app.route("/admin/alive")
@web.authenticated
def alive():
    return render_template("no.html")


@app.route("/number")
@web.authenticated
def number():
    name = web.auth.name
    return render_template("number.html", name=name)


@app.route("/feedback", methods=["POST", "GET"])
@web.authenticated
def setfeed():
    name = web.auth.name
    bug = db["Feed"]
    now = datetime.now()
    now2 = now.strftime("%y%m%d%H%M")
    now3_5 = now.strftime("%d/%m/%y %H:%M UTC")
    print(now3_5[9:11])
    i=int(now3_5[9:11])+1
    now3 = now3_5[0:7]+" "+str(i)+now3_5[11:]
    print(now3)
    try:
        cooldown = users.current["cooldown"]
    except:
        users.current["cooldown"]="N/A"
        cooldown = users.current["cooldown"]
        print("new")
    else:
        cooldown = users.current["cooldown"]
        if cooldown != "N/A":
            if int(now2)-int(cooldown[0:10]) < 100:
                return "You recenty posted a bug report or feedback suggestion please try again at: "+cooldown[10:]
    if request.method == "POST":
        if len(bug)/3 > 100:
            return "There are too meny bugs in the system please try again later :("
        else:
            title2 = request.form["title"]
            description2 = request.form["description"]
            if len(title2) > 41 or len(description2) > 121:
                return render_template("leng.html", name=name)
            elif len(title2) == 0 or len(description2) == 0:
                return "Please put something in you feedback suggestion"
            else:
                users.current["cooldown"] = now2+now3
                
                bug.append(profanity.censor(title2))
                bug.append(profanity.censor(description2))
                name2 = web.auth.name
                bug.append(name2)
                db["Feed"] = bug
                return redirect("/home")
    else:
        return render_template("makefeed.html", name=name)


@app.route("/admin/suggestions/feedback/get", methods=["GET", "POST"])
@web.authenticated
def get_feed():
    feed = db["Feed"]
    name = web.auth.name
    if request.method == "POST":
        feed = []
        db["Feed"] = feed
        return redirect("/admin/suggestions")
    elif name == "GoodVessel92551":
        return render_template("getfeed.html", name=name, feed=feed)


@app.route("/time/time")
@web.authenticated
def time():
    name = web.auth.name
    return render_template("time.html", name=name)


@app.route("/calculator")
@web.authenticated
def maths():
    name = web.auth.name
    return render_template("maths.html", name=name)


@app.route("/tasks", methods=["GET", "POST"])
@web.authenticated
def tasks():
    name = web.auth.name
    try:
        users.current["tasks"]
    except:
        users.current["tasks"] = []
        users.current["tasks_id"] = 0
        tasks = users.current["tasks"]
    else:
        tasks = users.current["tasks"]
    return render_template("tasks.html", name=name, tasks=tasks)


@app.route("/tasks/make", methods=["GET", "POST"])
@web.authenticated
def task_make():
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
            return "You have reached your max amount of tasks"
    else:
        return render_template("maketasks.html", name=name)


@app.route("/tasks/complete", methods=["GET", "POST"])
@web.authenticated
def task_remove():
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
        return render_template("removetasks.html", name=name)


@app.route('/sw.js', methods=['GET'])
def sw():
    return current_app.send_static_file('sw.js')

@app.route("/time/countdown")
@web.authenticated
def countdown():
    name = web.auth.name
    time = users.current["time"]
    print(time)
    return render_template("countdown.html", name=name, time=time)

@app.route("/time/countdown/make", methods=["GET", "POST"])
@web.authenticated
def countdown_make():
    name = web.auth.name
    if request.method == "POST":
        time = []
        hour = request.form["hour"]
        min = request.form["min"]
        sec = request.form["sec"]
        if hour == "":
            hour = 0
        elif min == "":
            min = 0
        elif sec == "":
            sec = 0
        elif int(hour) > 24:
            hour = 24
        elif int(min) > 60:
            min = 60
        elif int(sec) > 60:
            sec = 60
        time.append(hour)
        time.append(min)
        time.append(sec)
        print(time)
        users.current["time"]=time
        return redirect("/time/countdown")
    else:
        return render_template("makecoutdown.html", name=name)

@app.route("/time/stopwatch")
@web.authenticated
def stopwatch():
    name = web.auth.name
    return render_template("stopwatch.html", name=name)

@app.route("/time")
@web.authenticated
def time_home():
    name = web.auth.name
    return render_template("time_home.html", name=name, version=version)
    
@app.route("/changelog")
@web.authenticated
def changelog():
    name = web.auth.name
    return render_template("change.html", name=name, version=version)

@app.route("/shell")
@web.authenticated
def shell():
    name = web.auth.name
    return render_template("shell.html", name=name)
web.run(app, port=8080, debug=True)
