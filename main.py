

from flask import Flask, render_template


app = Flask(__name__)

posts = [
    {
        'author': 'Riaan Schuld',
        'title': 'Blogpost Test1',
        'content': 'Test for post 1',
        'datePosted' : 'April 2nd 2023'
    },
    {
        'author': 'Diana Collins',
        'title': 'Blogpost Test2',
        'content': 'Test for post 2',
        'datePosted' : 'April 2nd 2023'
    }
]

@app.route("/")
@app.route("/home")
def Home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def About():
    return render_template('about.html', title = 'About')

@app.route("/blog")
def Blog():
    return render_template('blog.html', posts=posts)



if __name__ == '__main__':
    app.run(debug=True)

