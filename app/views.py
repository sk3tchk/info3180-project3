"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
from app import db, app
from .forms import myform 
from random import randint
from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory, g, session
from werkzeug import secure_filename
from sqlalchemy.sql import functions
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from functools import wraps
from bs4 import BeautifulSoup
from app.forms import LoginForm, myform, WishForm
from app.models import user_profile, user_wishlist

import os
import random
import json
import requests
import smtplib


###
# Routing for your application.
###
app.secret_key = 'Who is that pokemon?'
app.config.from_object(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    try:
        return user_profile.query.get(int(id))
    except user_profile.DoesNotExist:
        return None
    

@app.before_request
def before_request():
    g.user = current_user
    
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/api/user/login', methods=['POST','GET'])
def login():
    error=None
    form = LoginForm(request.form)
    if request.method == 'POST':
        attempted_email = request.form['email']
        attempted_password = request.form['password']
        db_creds = user_profile.query.filter_by(email=attempted_email).first()
        db_email = db_creds.email
        db_password = db_creds.password
        db_id = db_creds.userid
        if attempted_email == db_email and attempted_password == db_password:
            session['logged_in'] = True
            login_user(db_creds)
            return redirect('/api/user/'+str(db_id))
        else:
            error = 'Incorrect username or password. Please try again'
            return render_template("login.html",error=error,form=form)
    form = LoginForm()
    return render_template("login.html",error=error,form=form)


@app.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect('/')


@app.route('/api/user/register', methods = ['POST','GET'])
def newprofile():
    if request.method == 'POST':
        form = myform()
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        sex = request.form['sex']
        age = int(request.form['age'])
        email = request.form['email']
        password = request.form['password']
        newProfile =user_profile(firstname=firstname, lastname=lastname, email=email, password=password, sex=sex, age=age)
        db.session.add(newProfile)
        db.session.commit()
        profilefilter = user_profile.query.filter_by(email=newProfile.email).first()
        return redirect('/api/user/'+str(profilefilter.userid))
    form = myform()
    return render_template('register.html',form=form)


@app.route('/api/user/<userid>')
@login_required
def profile_view(userid):
    if g.user.is_authenticated:
        profile_vars = {'id':g.user.userid, 'email':g.user.email, 'age':g.user.age, 'firstname':g.user.firstname, 'lastname':g.user.lastname, 'sex':g.user.sex}
        return render_template('user_profile.html',profile=profile_vars)
    

@app.route('/api/user/<id>/wishlist', methods = ['POST','GET'])
@login_required
def wishlist(id):
    profile = user_profile.query.filter_by(userid=id).first()
    profile_vars = {'id':profile.userid, 'email':profile.email, 'age':profile.age, 'firstname':profile.firstname, 'lastname':profile.lastname, 'sex':profile.sex}
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']
        image_url = ""
        newWish = user_wishlist(userid=id, title=title, description=description, description_url=url, image_url = image_url)
        db.session.add(newWish)
        db.session.commit()
        profilefilter = user_wishlist.query.filter_by(wishid=newWish.wishid).first()
        return redirect(url_for('image_get',wishid=profilefilter.wishid))
    form = WishForm()
    return render_template('wish_add.html',form=form,profile=profile_vars)

@app.route('/api/user/<id>/wishlists', methods=('GET', 'POST'))
def wishlists(id):
    wishlists = user_wishlist.query.filter_by(userid=id).all()
    storage = []
    for users_wishlist in wishlists:
        storage.append({'title':users_wishlist.title, 'description':users_wishlist.description, 'url':users_wishlist.description_url, 'image_url':users_wishlist.image_url})
    
    wishes = {'user_wishlist': storage}
    print wishes
    if request.method == 'POST':
      return jsonify(wishes)
    else:
      print storage
      return render_template('view_wish.html',wishlist=storage)  

#@app.route('/api/user/<id>/wishlist/share', method=('POST'))
#def wishshare(id):
#    return render_template(''):
    
@app.route('/api/thumbnail/process/<wishid>')
@login_required
def image_get(wishid):
    profilefilter =user_wishlist.query.filter_by(wishid=wishid).first()
    url = profilefilter.description_url
    result = requests.get(url)
    data = result.text
    images = []
    soup = BeautifulSoup(data, 'html.parser')
    og_image = (soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
        images.append(og_image['content'])
    for img in soup.find_all("img", class_="a-dynamic-image"):
        print img['src']
        images.append(img['src'])
    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        images.append(thumbnail_spec['href'])
    for img in soup.find_all("img", class_="a-dynamic-image"):
        if "sprite" not in img["src"]:
            images.append(img['src'])
    return render_template('get_image.html',images=images)
    
@app.route('/api/imageurl/addimage', methods=['POST'])
def add_imageurl():
    image_url = request.json['image_url']
    id = request.json["item_id"]
    
    
    item_wishlist = user_wishlist.query.filter_by(wishid=id).first()
    item_wishlist.image_url = image_url
    db.session.commit()
    return jsonify(message="success")

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/../picture/',
                               filename)

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
    
@app.route('/profile/', methods =('GET','POST'))
def profile():
    form =  myform()
    userid = random.randint(62000000, 620099999)
    print 'test'
    if request.method == 'POST': #and form.validate_on_submit():
        print 'validate'
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        sex = request.form['sex']
        file = request.files['image']
        image = secure_filename(file.filename)
        file.save(os.path.join("picture", image))
        user = user_profile(userid, image, firstname, lastname, age, sex)
        db.session.add(user)
        db.session.commit()
        flash('File Upload Complete!!!')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@app.route('/profiles/', methods =['GET','POST'])
def profiles():
    profiles = user_profile.query.all()
    storage = []
    if request.method == 'POST': #or request.headers['Content-Type'] == 'application/json':
        for users in profiles:
            storage.append({'userid':users.userid, 'image':users.image, 'first name':users.firstname,'last name':users.lastname,'age':users.age,'sex':users.sex})
        users ={'users':storage}
        return jsonify(users)
    else:
        return render_template('profiles.html',profiles=profiles)
        
@app.route('/profile/<userid>/', methods=['GET'])
def query(userid):
    queryid = User.query.filter_by(userid=userid).first_or_404()
    return render_template('profiles.html',profiles=profiles)
    
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
