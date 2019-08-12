from program import app
from flask import render_template  # ?


# @ called decorator and it is used to ‘augment’ function definitions.
# Flask uses route() to say that if the browser requests the address / (the default, or home address),
# then our app should route that request to this function.
@app.route('/')
def hello_world():
    author1 = "Svitlana Zaster"
    name1 = "Sveta"
    return render_template('index.html', author=author1, name=name1)


@app.route('/index')
def index():
    author1 = "Svitlana Zaster"
    name1 = "Sveta"
    return render_template('index.html', author=author1, name=name1)


@app.route('/100Days')
def p100Days():
    return render_template('100Days.html')


@app.route('/animals')
def animals():
    return render_template('animals.html')


@app.route('/cats')
def cats():
    return render_template('cats.html')


if __name__ == "__main__":
    app.run()
