# -*- coding = utf-8 -*-
#from flask.ext.mysql import MySQL
import os
from flask import Flask, session, request, redirect, g, url_for, abort, render_template, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import schema, Column, DateTime, String, Integer, Float, create_engine
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.sql.functions import now
import pdb

SECRET_KEY = 'rest api'
USERNAME='lxy'
PASSWORD='123'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

Base = declarative_base()
engine = create_engine("mysql://root:@localhost/mysql", encoding='latin1')


class blogs(Base):
    __tablename__ = 'blogs'
    title = Column(String(60), primary_key=True)
    author = Column(String(40))
    content = Column(String(120))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

DBsession = sessionmaker(bind=engine)
#DBsession.configure(bind=engine)
Base.metadata.create_all(engine)
#b2 = blog(author='a', title='t',content='c')
#session.add(b2)
#session.commit()
DSession = DBsession()

@app.before_request
def before_request():
  pass


@app.teardown_request
def teardown_request(exception):
  DSession.close()

@app.route('/blog',methods=['GET', 'POST'])
def s_blog():
  error = None
  if request.method == 'POST':
    if session.get('logged_in'):
      session.pop('logged_in', None)
      flash('You were logged out')
      return redirect(url_for('s_blog'))
    else:
      if request.form['username'] != app.config['USERNAME']:
        error = 'Invalid username'
      elif request.form['password'] != app.config['PASSWORD']:
        error = 'Invalid password'
      else:
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('s_blog'))
  return render_template("s_blog.html", error=error)

#def login():


#@app.route('/authors', methods=['GET', 'POST'])
#def s_authors():
 # blogs = DSession.query(blog).order_by(blog.title)
  #return render_template('s_authors.html', blogs=blogs)


@app.route('/blog/articles', methods=['GET', 'POST', 'DELETE'])
def s_titles():
  if request.method == 'POST':
    ablog=blogs(title=request.form['title'], author=app.config['USERNAME'], \
      content=request.form['content'], \
      created_at=now(), updated_at=now())
    DSession.add(ablog)
    DSession.commit()
  blog = DSession.query(blogs).order_by(blogs.title)
  return render_template('s_titles.html', blogs=blog)



@app.route('/blog/articles/<title>', methods=['GET', 'POST' 'PUT', 'DELETE'])
def s_info(title):
  for blog in DSession.query(blogs).filter(blogs.title==title):
    pass
  if (request.method == 'PUT') or (request.args.get('_method') == 'PUT'):
    blog.updated_at=now()
    DSession.commit()
  if request.method == 'DELETE':
    DSession.delete(blog)
    DSession.commit()
    return redirect(url_for('s_titles'))
  return render_template('s_info.html', blog=blog)



#@app.route('/blog_out')
#def exit():
 # session.pop('logged_in', None)
  #flash('You were logged out')
  #return redirect(url_for('s_blog'))


if __name__ == '__main__':
    app.run(debug=True)



