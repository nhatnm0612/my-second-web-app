from io import BytesIO
from LabourExport import *
from DBside import MyDatabase
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session


app            = Flask(__name__)
app.secret_key = "###Nh4t.N6uy3n.M1nh.(+84)-168-953-2822###"
ALLOWED        = set(["csv"])


def allowed_file(filename):
    return (("." in filename) and
            (filename.split(".")[-1] in ALLOWED))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        DB             = MyDatabase("NMN", "MyClass")
        DB.remove({})
        DB.log_out()
        flash("Deleted all member!", "danger")
        return redirect(url_for("about"))
    return render_template("home_page.html")


@app.route("/about/")
def about():
    return render_template("about_me.html")


@app.route("/new-member/", methods = ["GET", "POST"])
def new_member():
    DB              = MyDatabase("NMN", "MyClass")
    students        = []
    for document in DB.load():
        student     = Student(document["FamilyName"], document["GivenName"], document["Gender"],
                              document["DateOfBirth"], document["Certificate"])
        students.append(student.__repr__())
    DB.log_out()
    this_year       = datetime.datetime.today().year
    if request.method == "POST":
        firstname   = request.form["first-name"]
        familyname  = request.form["family-name"]
        gender      = request.form["gender"]
        month       = request.form["month"]
        date        = request.form["date"]
        year        = request.form["year"]
        certificate = request.form["certificate"]
        MONTH       = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                       "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        month       = MONTH[month]
        student     = Student(familyname, firstname, gender, "{}-{}-{}".format(year, month, date), certificate)
        if student.__repr__() not in students:
            DB.save(student.to_json())
            DB.log_out()
        flash("Added member!", "success")
        return redirect(url_for("about"))
    return render_template("new_member.html", this_year = this_year)


@app.route("/sort/<string:by_field>", methods = ["GET", "POST"])
def sort_by(by_field):
    DB                 = MyDatabase("NMN", "MyClass")
    MyClass            = LabourExportClass("MyClass")
    for document in DB.load():
        MyClass.new_student(Student(document["FamilyName"], document["GivenName"], document["Gender"],
                                    document["DateOfBirth"], document["Certificate"], document["_id"]))
    DB.log_out()
    if by_field       == "name":
        data           = []
        given, names   = MyClass.sort("name")
        for name in given:
            data.append(names[name])
    else:
        data           = MyClass.sort("age")
    if request.method == "POST":
        by             = request.form["filter-by"]
        value          = request.form["filter-value"]
        return redirect(url_for("filter", by = by.lower(), value = value))
    return render_template("sort_by.html", by_field = by_field, data = data)


@app.route("/filter/<string:by>/<string:value>", methods = ["GET", "POST"])
def filter(by, value):
    DB          = MyDatabase("NMN", "MyClass")
    MyClass     = LabourExportClass("MyClass")
    for document in DB.load():
        MyClass.new_student(Student(document["FamilyName"], document["GivenName"], document["Gender"],
                                    document["DateOfBirth"], document["Certificate"], document["_id"]))
    DB.log_out()
    data        = MyClass.filter_by(value, by)
    if request.method == "POST":
        by      = request.form["filter-by"]
        value   = request.form["filter-value"]
        return redirect(url_for("filter", by = by.lower(), value = value))
    return render_template("filter_by.html", by = by.lower(), value = value, data = data)


@app.route("/member/<string:ID>/", methods = ["GET", "POST"])
def member(ID):
    DB          = MyDatabase("NMN", "MyClass")
    this_year   = datetime.datetime.today().year
    for document in DB.load(find = {"_id": ObjectId(ID)}):
        student = Student(document["FamilyName"], document["GivenName"], document["Gender"],
                          document["DateOfBirth"], document["Certificate"], document["_id"])
    DB.log_out()
    data        = [student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID]
    if request.method == "POST":
        DB.remove({"_id": ObjectId(ID)})
        DB.log_out()
        flash("Deleted member!", "warning")
        return redirect(url_for("about"))
    return render_template("member.html",
                           age         = data[0],
                           name        = data[1],
                           DoB         = data[2],
                           gender      = data[3],
                           certificate = data[4],
                           ID          = data[5],
                           this_year   = this_year)


@app.route("/member/change/<string:ID>", methods = ["POST"])
def change(ID):
    DB          = MyDatabase("NMN", "MyClass")
    firstname   = request.form["first-name"]
    familyname  = request.form["family-name"]
    gender      = request.form["gender"]
    month       = request.form["month"]
    date        = request.form["date"]
    year        = request.form["year"]
    certificate = request.form["certificate"]
    MONTH       = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                   "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    month       = MONTH[month]
    student     = Student(familyname, firstname, gender, "{}-{}-{}".format(year, month, date), certificate)
    DB.update({"_id": ObjectId(ID)}, student.to_json())
    DB.log_out()
    flash("Updated member!", "info")
    return redirect(url_for("about"))


@app.route("/classify/<string:by>")
def classify(by):
    return render_template("classify.html", by = by)


@app.route("/plotting/<string:by>.png")
def plotting(by):
    DB          = MyDatabase("NMN", "MyClass")
    MyClass     = LabourExportClass("MyClass")
    for document in DB.load():
        MyClass.new_student(Student(document["FamilyName"], document["GivenName"], document["Gender"],
                                    document["DateOfBirth"], document["Certificate"], document["_id"]))
    DB.log_out()
    fig  = Figure()
    axis = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor("powderblue")
    if by in ["gender", "certificate"]:
        labels, sizes, explode = MyClass.classify(by)
        axis.pie(sizes, explode = explode, labels = labels, autopct = "%1.2f%%", shadow = True, startangle = 90)
        axis.axis("equal")
    elif by == "birth-month":
        data = MyClass.classify(by.replace("-", " "))
        axis.bar(data.keys(), data.values(), width = 0.6, color = "#3333ff")
        fig.autofmt_xdate(rotation = 30)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "image/png"
    return response
            

@app.route("/upload", methods = ["GET", "POST"])
def upload():
    DB              = MyDatabase("NMN", "MyClass")
    students        = []
    for document in DB.load():
        student     = Student(document["FamilyName"], document["GivenName"], document["Gender"],
                              document["DateOfBirth"], document["Certificate"])
        students.append(student.__repr__())
    DB.log_out()
    if request.method == "POST":
        file = request.files["input-file"]
        if file and allowed_file(file.filename):
            data = file.read().decode("utf-8")
            for line in data.split("\n"):
                if "Family" in line:
                    pass
                else:
                    line    = line.strip().split(", ")
                    student = Student(line[0], line[1], line[2], line[3], line[4])
                    if student.__repr__() not in students:
                        DB.save(student.to_json())
                        DB.log_out()
        flash("Successfully added file!", "success")
        return redirect(url_for("about"))
    return render_template("upload_page.html")

if __name__ == "__main__":
    app.run(debug = True)
