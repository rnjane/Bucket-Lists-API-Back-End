from flask import Flask, render_template, redirect, url_for
from flask import flash, session, request, current_app
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import forms
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    buckets = db.relationship('Bucket', backref='user', lazy='dynamic')


class Bucket(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    bucketname = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='bucket', lazy='dynamic', cascade="all, delete-orphan")


class Item(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(15), server_default='Not Done')
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))


class Users():
    '''This class defines actions related to the users of the app'''
    __username = ''
    __password = ''
    def create_user(self, username, password):
        '''Method to register users'''
        if type(username) is list or type(username) is dict:
            return 'wrong data format'
        if User.query.filter_by(username=username).first() is not None:
            return 'username in use. use a different one.'
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return 'account created'


    def login_user(self, username, password):
        '''Method to log users in'''
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return 'login succesful'
            return 'Wrong password'
        return 'Invalid username or password'

    def logout(self):
        '''log out method'''
        logout_user()
        return 'logout succesful'


class BucketLists():
    '''Class definition for the bucketlists classs'''
    __name = ''
    __username = ''

    def create_bucket(self, bucketname):
        '''add a bucket method'''
        new_bucket = Bucket(bucketname=bucketname, user=current_user)
        db.session.add(new_bucket)
        db.session.commit()
        return 'bucket added.'

    def view_buckets(self):
        '''view all buckets method'''
        user = User.query.filter_by(username=current_user.username).first()
        buckets = user.buckets.all()
        return buckets

    def delete_bucket(self, bucketname):
        '''delete a bucket method'''
        bucket = Bucket.query.filter_by(bucketname=bucketname).first()
        db.session.delete(bucket)
        db.session.commit()
        return 'delete succesful'

    def edit_bucket(self, oldname, newname):
        '''edit a bucket method'''
        bucket = Bucket.query.filter_by(bucketname=oldname).first()
        bucket.bucketname = newname
        db.session.commit()
        return 'edit succesful'


class Items():
    '''Class definition for the items classs'''
    __itemname = ''
    __itemlist = ''

    def create_item(self, itemname):
        '''create item method'''
        name = session['currentbucket']
        current_bucket = Bucket.query.filter_by(bucketname=name).first()
        new_item = Item(itemname=itemname, bucket=current_bucket)
        db.session.add(new_item)
        db.session.commit()
        return 'item added.'

    def view_items(self):
        '''view all items method'''
        bucket = Bucket.query.filter_by(bucketname=session['currentbucket']).first()
        items = bucket.items.all()
        return items

    def delete_item(self, itemname):
        '''delete an item method'''
        item = Item.query.filter_by(itemname=itemname).first()
        db.session.delete(item)
        db.session.commit()
        return 'delete succesful'

    def edit_item(self, oldname, newname, status):
        '''edit item method'''
        item = Item.query.filter_by(itemname=oldname).first()
        item.itemname = newname
        item.status = status
        db.session.commit()
        return 'edit succesful'

user = Users()
bucket = BucketLists()
item = Items()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    '''Home page'''
    return redirect(url_for('bucketlists'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''method to log in users'''
    form = forms.LoginForm()
    if user.login_user(form.username.data, form.password.data) == 'login succesful':
        flash('login succeful')
        return redirect(url_for('bucketlists'))
    elif user.login_user(form.username.data, form.password.data) == 'Wrong password':
        flash('Wrong password')
        return render_template('login.html', form=form)
    elif user.login_user(form.username.data, form.password.data) == 'Invalid username or password':
        flash('Invalid username or password')
        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''method to register new users'''
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data != form.confirmpassword.data:
                flash('passwords dont match')
                return render_template('register.html', form=form)
            elif user.create_user(form.username.data, form.password.data) == 'account created':
                flash('account created')
                return redirect(url_for('login'))
            elif user.create_user(form.username.data, form.password.data) == 'wrong data format':
                flash('wrong data format')
                return render_template('register.html', form=form)
            elif user.create_user(form.username.data, form.password.data) == 'username in use. use a different one.':
                flash('username in use. use a different one.')
                return render_template('register.html', form=form)
        flash('error in form')
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    '''method to log users out'''
    if user.logout() == 'logout succesful':
        return redirect(url_for('login'))
    flash('error logging out')
    return redirect(url_for('bucketlists'))


@app.route('/bucketlists')
@login_required
def bucketlists():
    '''View all bucket lists'''
    af = forms.NewBucketList()
    ef = forms.EditBucket()
    df = forms.DeleteBucket()
    buckets = bucket.view_buckets()
    return render_template('bucketlists.html', buckets=buckets, name=current_user.username, addform=af, editform=ef, deleteform=df)


@app.route('/bucketlists/addbucket', methods=['POST', 'GET'])
@login_required
def addbucket():
    '''Add Bucket lists function'''
    form = forms.NewBucketList()
    if bucket.create_bucket(form.bucketname.data) == 'bucket added.':
        flash('Bucket added.')
        return redirect(url_for('bucketlists'))
    return redirect(url_for('bucketlists'))


@app.route('/bucketlist/delete', methods=['POST', 'GET'])
@login_required
def deletebuket():
    '''delete bucket'''
    if bucket.delete_bucket(request.form['bucketname']) == 'delete succesful':
        flash('delete succesful')
        return redirect(url_for('bucketlists'))
    flash('error deleting bucket')
    return redirect(url_for('bucketlists'))


@app.route('/bucketlist/edit', methods=['POST', 'GET'])
@login_required
def editbuket():
    '''edit bucket'''
    if bucket.edit_bucket(request.form['bucketname'], request.form['newname']) == 'edit succesful':
        flash('Edit succesful')
        return redirect(url_for('bucketlists'))
    flash('error editing bucket')
    return redirect(url_for('bucketlists'))


@app.route('/bucketlists/<b_key>/items', methods=['POST', 'GET'])
@login_required
def viewitems(b_key):
    '''View items in a bucket list'''
    session['currentbucket'] = b_key
    af = forms.NewItem()
    ef = forms.EditItem()
    df = forms.DeleteItem()
    items = item.view_items()
    return render_template('tasks.html', items=items, addform=af, editform=ef, deleteform=df, blist=b_key)


@app.route('/items/additem', methods=['POST', 'GET'])
@login_required
def additem():
    '''Add item function'''
    if item.create_item(request.form['itemname']) == 'item added.':
        flash('Item added.')
        return redirect(url_for('viewitems', b_key=session['currentbucket']))
    flash('Illegal item name.')
    return redirect(url_for('viewitems', b_key=session['currentbucket']))


@app.route('/items/edititem', methods=['POST', 'GET'])
@login_required
def edititem():
    '''Edit item function'''
    form = forms.EditItem()
    if item.edit_item(request.form['bucketname'], request.form['newname'], request.form['status']) == 'edit succesful':
        flash('edit succesful')
        return redirect(url_for('viewitems', b_key=session['currentbucket']))
    flash('error in edit form')
    return redirect(url_for('viewitems', b_key=session['currentbucket']))


@app.route('/items/removeitem', methods=['POST', 'GET'])
@login_required
def removeitem():
    '''Remove item function'''
    if item.delete_item(request.form['itemname']) == 'delete succesful':
        flash('delete successful')
        return redirect(url_for('viewitems', b_key=session['currentbucket']))
    flash('error deleting item')
    return redirect(url_for('viewitems', b_key=session['currentbucket']))
