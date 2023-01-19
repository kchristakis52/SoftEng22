from flask import Flask, render_template

# create app and set directory for html code (default is "./templates")
app = Flask(__name__, template_folder="../frontend")


@app.route("/")
def questionnaire_test():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
