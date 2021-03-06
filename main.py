from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
#import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:blog@localhost:8889/blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hxixjx'

class BlogEntry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    entry = db.Column(db.String(255))
    #completed = db.Column(db.Boolean)

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry

    def is_valid(self):
        if self.title and self.entry :
            return True
        else:
            return False

@app.route('/add_a_new_post', methods=['POST', 'GET'])
def add_a_new_post():

        if request.method == 'POST':
            entry_title = request.form['title']
            entry_text  = request.form['entry']
            new_post = BlogEntry(entry_title, entry_text)

            if new_post.is_valid() == True:
                db.session.add(new_post)
                db.session.commit()
                url = "/blog?id=" + str(new_post.id)
                return redirect(url)
            else: #if the validation came up False
                flash("Error. Your blog entry requires a title and a text.")
                return render_template('add_a_new_post.html', title="Enter your blog here.", entry_title=entry_title, entry_text=entry_text)

        else: #it was a GET request, not a POST
            return render_template('add_a_new_post.html',title="Add a New Post")




@app.route('/', methods=['POST', 'GET'])
def index():

    return redirect("/blog")


@app.route("/blog")
def show_blogs():

    blog_id = request.args.get('id')
    if blog_id: #if the blog isn't empty
        blog = BlogEntry.query.get(blog_id)
        if blog:
        # return str(blog.title) + str(blog.entry)
            return render_template('blog.html', title=blog.title, blog=blog)
        else:
            flash("Invalid Blog ID")

    blogs = BlogEntry.query.all()
    return render_template('all_blogs.html', title="entry_title", blogs=blogs) #completed_tasks=completed_tasks)


@app.route("/updatedb")
def update_DB():

    db.drop_all()
    db.create_all()
    #return "updated db"
    return redirect("/")


if __name__ == '__main__':
    #db.drop_all()
    #db.create_all()
    app.run()
