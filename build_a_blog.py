from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import html
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def reroute():
    return redirect  ('/blog')


@app.route('/blog', methods=['GET'])
def main():
    bloglist=Blog.query.all()
    return render_template('main_form.html',bloglist=bloglist)
        
        
            
@app.route('/blog_view', methods=['GET','POST'])
def view():
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']

        errors=False
        title_error=''
        if new_title == '':
            title_error="Please provide a title"
            errors=True
            #need error return
        body_error=""
        if new_body=='':
            body_error="please fill in the body"
            errors=True
            #need error return
        if errors == True:
            return render_template("entry_form.html",title_error=title_error,body_error=body_error)
        
        
        new_entry=Blog(new_title,new_body)
        db.session.add(new_entry)
        db.session.commit()

        
        # return render_template("blog_view.html?"+blogid)
        return redirect('/blog_view?id={0}'.format(new_entry.id))
    else:
        blog_id = request.args.get('id')
        #blog_id = request.form('post.id')

        blog=Blog.query.filter_by(id=blog_id).first()
        return render_template("/blog_view.html",blog=blog)

    # else:
    #     return render_template("blog_view2.html", blog=blog)



#WILL NEED ID - USE ID, INCRIMENT BY 1 AT END OF PRINTING OUT MAIN FORM,
#AND MAKE LINKS USE A GET FEATURE TO OPEN CORRECT PAGE/BLOG

@app.route('/new_post', methods =  ["GET","POST"])
def entry():
    return render_template("/entry_form.html")

if __name__ == '__main__':
    app.run()