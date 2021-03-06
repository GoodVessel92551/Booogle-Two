from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db
from datetime import datetime
import os,json,requests

app = Flask(__name__)
users = web.UserStore()
version = "1.10"
apikey = os.environ["API"]
base_url = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/")
def index():
    name = web.auth.name
    vists = db["vists"]
    if name != "GoodVessel92551":
        db["vists"] = vists + 1
    if name != "":
        return redirect("/home")
    return render_template("index.html", version=version)
    


@app.route("/home")
@web.authenticated
def home():
    name = web.auth.name
    names = db["names"]
    online = db["online"]
    try:
        users.current["data"]
    except:
        try:
            users.current["cps_time"]
            users.current["theme"]
            users.current["color"]
            users.current["photo"]
            users.current["city"]
            users.current["units"]
        except:
            users.current["data"] = ["system",["#ff6600","#a8531a"],"green2",10,[0,10,0],"london","metric"]
        else:
            users.current["data"] = [users.current["theme"],["#ff6600","#a8531a"],users.current["photo"],users.current["time"],[0,10,0],users.current["city"],"metric"]
            del users.current["city"]
            del users.current["units"]
            del users.current["cps_time"]
            del users.current["theme"]
            del users.current["color"]
            del users.current["photo"]
    if name not in names:
        names.append(name)
        db["names"] = names
    if name in online:
        for i in range(len(online)):
            if online[i] == name:
                online.pop(i)
                online.pop(i)
                break
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M UTC")
    online.append(name)
    online.append(now)
    db["online"] = online
    color = users.current["data"][1]
    return render_template("home.html", name=name, version=version, photo=users.current["data"][2], color=color, theme=users.current["data"][0])


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
        color = users.current["data"][1]
        return render_template("admin.html", color=color, theme=users.current["data"][0],name=name,users=user,views=views,users2=users2,views2=views2, version=version, photo=users.current["data"][2])
    else:
        return render_template("no.html")


@app.route("/admin/users")
@web.authenticated
def adminusers():
    name = web.auth.name
    user = db["names"]
    online = db["online"]
    if name == "GoodVessel92551":
        color = users.current["data"][1]
        return render_template("users.html", color=color, theme=users.current["data"][0], name=name,online=online, users=user, version=version, photo=users.current["data"][2])
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
    theme_count = db["theme_count"]
    bug = len(bug) / 3
    feed = len(feed) / 3
    user = len(user)
    if name == "GoodVessel92551":
        db["names2"] = user
        db["vists2"] = views
        color = users.current["data"][1]
        return render_template("analytics.html", color=color, theme=users.current["data"][0],name=name,users=user,views=views,bug=bug,feed=feed, version=version, photo=users.current["data"][2], theme_count=theme_count)
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
        color = users.current["data"][1]
        return render_template("suggestions.html", color=color, theme=users.current["data"][0],name=name, users=user,bug=bug,feed=feed, version=version, photo=users.current["data"][2])
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
    color = users.current["data"][1]
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
        return render_template("makebug.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/admin/suggestions/bugs/get", methods=["GET", "POST"])
@web.authenticated
def get_bugs():
    color = users.current["data"][1]
    bug = db["Bug"]
    name = web.auth.name
    if request.method == "POST":
        bug = []
        db["Bug"] = bug
        return redirect("/admin/suggestions")
    elif name == "GoodVessel92551":
        return render_template("getbug.html", color=color, theme=users.current["data"][0], name=name, bug=bug, photo=users.current["data"][2])

    else:
        return render_template("no.html")


@app.route("/admin/alive")
@web.authenticated
def alive():
    return render_template("no.html")


@app.route("/number")
@web.authenticated
def number():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("number.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/feedback", methods=["POST", "GET"])
@web.authenticated
@web.per_user_ratelimit(
    max_requests = 2,
    period = 600,
    get_ratelimited_res=(lambda left: f"Too many requests, try again after {left} sec"),
)
def setfeed():
    color = users.current["data"][1]
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
        return render_template("makefeed.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/admin/suggestions/feedback/get", methods=["GET", "POST"])
@web.authenticated
def get_feed():
    color = users.current["data"][1]
    feed = db["Feed"]
    name = web.auth.name
    if request.method == "POST":
        feed = []
        db["Feed"] = feed
        return redirect("/admin/suggestions")
    elif name == "GoodVessel92551":
        return render_template("getfeed.html", color=color, theme=users.current["data"][0], name=name, feed=feed, photo=users.current["data"][2])


@app.route("/time/time")
@web.authenticated
def time():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("time.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/calculator")
@web.authenticated
def maths():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("maths.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/tasks", methods=["GET", "POST"])
@web.authenticated
def tasks():
    color = users.current["data"][1]
    name = web.auth.name
    try:
        users.current["tasks"]
    except:
        users.current["tasks"] = []
        users.current["tasks_id"] = 0
        tasks = users.current["tasks"]
    else:
        tasks = users.current["tasks"]
    return render_template("tasks.html", color=color, theme=users.current["data"][0], name=name, tasks=tasks, version=version, photo=users.current["data"][2])


@app.route("/tasks/make", methods=["GET", "POST"])
@web.authenticated
def task_make():
    color = users.current["data"][1]
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
        return render_template("maketasks.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/tasks/complete", methods=["GET", "POST"])
@web.authenticated
def task_remove():
    color = users.current["data"][1]
    name = web.auth.name
    if request.method == "POST":
        tasks = users.current["tasks"]
        id = request.form["id"]
        for i in range(len(tasks)):
            if tasks[i] == int(id):
                print(tasks)
                tasks.pop(i)
                tasks.pop(i-1)
                tasks.pop(i-2)
                users.current["tasks"] = tasks
                break
        return redirect("/tasks")
    else:
        return render_template("removetasks.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/sw.js", methods=["GET"])
def sw():
    return current_app.send_static_file("sw.js")

@app.route("/time/countdown-timer")
@web.authenticated
def countdown_timer():
    color = users.current["data"][1]
    name = web.auth.name
    countdown = users.current["data"][4]
    return render_template("countdown.html", color=color, theme=users.current["data"][0], name=name,time=countdown, version=version, photo=users.current["data"][2])

@app.route("/time/countdown/make", methods=["GET", "POST"])
@web.authenticated
def countdown_make():
    color = users.current["data"][1]
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
                users.current["data"][4]=time
                return redirect("/time/countdown-timer")
    else:
        return render_template("makecoutdown.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])

@app.route("/time/stopwatch")
@web.authenticated
def stopwatch():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("stopwatch.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])

@app.route("/time")
@web.authenticated
def time_home():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("time_home.html", name=name, version=version, photo=users.current["data"][2], color=color, theme=users.current["data"][0])
    
@app.route("/changelog")
@web.authenticated
def changelog():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("change.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])

@app.route("/shell")
@web.authenticated
def shell():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("shell.html", color=color, theme=users.current["data"][0], name=name)

@app.route("/games")
@web.authenticated
def games():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("game.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])


@app.route("/color", methods=["GET", "POST"])
@web.authenticated
def color():
    color = users.current["data"][1]
    name = web.auth.name
    if request.method == "POST":
        color_1 = request.form["color1"]
        color_2 = request.form["color2"]
        print(color_1+" "+color_2)
        users.current["data"][1] = [color_1,color_2]
        return redirect("/home")
    else:
        return render_template("make_color.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])

@app.route("/theme", methods=["GET", "POST"])
@web.authenticated
def theme():
    color = users.current["data"][1]
    name = web.auth.name
    if request.method == "POST":
        theme = request.form["theme"]
        users.current["data"][0] = theme
        if name != "GoodVessel92551":
            db["theme_count"] += 1
        return redirect("/home")
    else:
        return render_template("theme.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])

@app.route("/background")
@web.authenticated
def background():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("image.html", color=color, theme=users.current["data"][0], name=name,version=version, photo=users.current["data"][2])

@app.route("/background/pick", methods=["GET", "POST"])
@web.authenticated
def pick():
    if request.method == "POST":
        url = request.full_path
        users.current["data"][2]=url[17:]
    return redirect("/home")


@app.route("/weather", methods=["GET", "POST"])
@web.authenticated
def weather():
    if request.method == "POST":
        users.current["data"][5] = request.form["city"]
    weather_list=[]
    city = users.current["data"][5]
    unit = users.current["data"][6]
    url = base_url + "&units="+unit+"&appid=" + apikey + "&q=" + city
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] == 200:
        main = data["main"]
        name = data["name"]
        wind = data["wind"]
        weather = data["weather"]
        type = weather[0]["description"]
        icon = weather[0]["icon"]
        temp = int(main["temp"])
        feel = int(main["feels_like"])
        min = int(main["temp_min"])
        max = int(main["temp_max"])
        humid = int(main["humidity"])
        speed = int(wind["speed"])
        deg = int(wind["deg"])
        weather_list.append(type)
        weather_list.append(temp)
        weather_list.append(feel)
        weather_list.append(min)
        weather_list.append(max)
        weather_list.append(humid)
        weather_list.append(name)
        weather_list.append(speed)
        weather_list.append(icon)
        weather_list.append(deg)
    else:
        users.current["data"][5] = "london"
        return render_template("error.html", error="City dose not exsist")
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("weather.html", color=color, theme=users.current["data"][0], name=name,version=version, photo=users.current["data"][2], weather=weather_list, unit=users.current["data"][6])

@app.route("/weather/change", methods=["GET", "POST"])
@web.authenticated
def weather_change():
    if users.current["data"][6] == "metric":
        users.current["data"][6] = "imperial"
    else:
        users.current["data"][6] = "metric"
    return redirect("/weather")

@app.route("/images")
@web.authenticated
def images():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("images.html", color=color, theme=users.current["data"][0], name=name,version=version, photo=users.current["data"][2])

@app.route("/convert")
@web.authenticated
def convert():
    color = users.current["data"][1]
    name = web.auth.name
    return render_template("convert.html", color=color, theme=users.current["data"][0], name=name,version=version, photo=users.current["data"][2])

@app.route("/cps")
@web.authenticated
def cps():
    return render_template("cps.html", color=users.current["data"][1], theme=users.current["data"][0], name=web.auth.name,version=version, photo=users.current["data"][2], time=users.current["data"][3])

@app.route("/cps/make", methods=["GET", "POST"])
@web.authenticated
def cps_make():
    color = users.current["data"][3]
    name = web.auth.name
    if request.method == "POST":
        time = []
        sec = request.form["sec"]
        try:
            int(sec)
        except:
            return "You need to enter a number"
        else:
            if sec == "":
                return render_template("error.html",error="Enter a number")
            elif int(sec) < 0:
                return render_template("error.html",error="One of the numbers is to big or small")
            else:
                time.append(sec)
                print(time)
                users.current["data"][3]=time
                return redirect("/cps")
    else:
        return render_template("makecps.html", color=color, theme=users.current["data"][0], name=name, version=version, photo=users.current["data"][2])
@app.route("/logout")
@web.authenticated
def logout():
    return render_template("index.html", version=version)

web.run(app, port=8080, debug=True)
