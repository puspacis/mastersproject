import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required

import googleapiclient.discovery
from google.oauth2 import service_account


@app.route('/')
@app.route('/home')
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
	return render_template('home.html', posts=posts)

def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    GOOGLE_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDi3EQPyamRoh8Q\n1penpE6Z7ck+nTOdEjTANUfF9LiRuZ8mm4qxFf84RocdBXdiMOueeLwC5ZFrYlrI\ntgX7BLg378eU2K+FV6Q73qqhMDYdmmNUkzwOKOWQLeEv+5JEgC0+G1K8D+YznhPx\nU/AyjMKdRErhy5FjKW1X3ITvo0Ol7ULd5bByyMHNUB78ihBcUw6XXUgScl13/enO\nfNTh3ZrXjrwIfip/ZJXszx11ISRMRZRYcjyj+T+Xkot2buSCxDubMALSEaoXzCia\n59WovQXHbpGmfALuF9ub6E2r7mddfgFSvWGNMh2AN1SoQmu4yzjIg1ofiN0X99+S\ncnzdURyXAgMBAAECggEATanikxUSvAyoXfdZC8cwMXo6PvlKRieJb5PN8nMJDLpj\nRbBSFrXVHcrnToQkjrT4tNPYaZV15zFQqw3Fll3TQzMPPGHCFQAf9W8RMwVyQUgt\nYTLWiHJvxKAwS2DwfgrzciOge0lmIZ2obiGyRVvy9CwBBrPOHgh8qmuQBwn5ir+9\n2ZIVZ54L1BTBuGIE0kEesPUQkL9SDtsKrhUrnaAUdDAHWfDul8TBQzeYLtHnFrSj\n+oq9/vQ3JHHBHBfyG+G2DQSaAhO7+C/3OfM/GHXyXqnEUOk8TOucbe/R5PDL2tKH\nYZRs1QRRa58uSHQ0QHszCozThNeBYd+AM9kTNuanYQKBgQD6OdAkHl2YI3tytwgq\n5UOSzCb1F7ueof3uqx/Xx5iIb2eQ1GIK4m+Yx9AFL5kdYUuNUJY3n2uFO38g5BHB\nXIk2AjFt0geTO+4dD5rBe/1pnd6XHX/3dXLm+5q/XU59KIXkrmdXiVvqkeyEZPzx\nONtoP4bm4DFJuO9iAxuV8uETUwKBgQDoGGx1zzLwfyZZgvFt1kp8i8Yqv78/kG47\nY0Mi8+OmgjVeTIZHOLD42sZHWHLT7hVV9AUufG1YOWDlmT5ZpYZxvEpPu3eDTXfo\nSZh3OA43kBIFdVdbxlOESUNJ4ffyeOa+QVfWVT88j88DeeAOagkPOcz1wu+gOerB\nKVzv8/SNLQKBgDoJ6NZH2MuuBzcvbwyMCuVkxvB4ZcNAraaLOKKTIDUdKfd025zM\nsrfMONrLFIe1BpIri/ww1P6dMzqMy/V+ojDNx2tCmRE0iGFjOjEAsmGqBXQlmoXq\nTxF2cIlMeiUbnhrRvRSXvqMk36hByE2nM3T1rzOj8qq344ZnVCGuqTgTAoGBAJBv\nIo/t8XVYqzTpF/WSdagsE5Zm3U1hRDgQ/aayv+jO/wc/+BA6Z2d2Pg4ILO1WLFDh\nGphjNmjAzFwVkYeYSqJc2qHjt+wuOYCEzCzk5XQOZCihbUvfj/my3f0McpCiTHX5\nk//97OxzUhCHt7dApYKkJbiLJzQ+1qh+ZSeuWXHBAoGAdpdaxqipUx4sigPXu5Pm\nti4eoqTykyJnZh9RN9uXfFEHqC/PTjfMAYZdxq8PxFlT3unU2xHMxxPq6Ke0rim/\nIDznD8WeniBxwdXwKPLZIPy7xp3Up7h+CcX0+oB8+q00As8IM0hQWOkWBcnGF+cd\nWaA1elBSiA1hzfrAu8n71c8=\n-----END PRIVATE KEY-----\n"
    # The environment variable has escaped newlines, so remove the extra backslash
    GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')

    account_info = {
      "private_key": GOOGLE_PRIVATE_KEY,
      "client_email": "ashish@flask-278914.iam.gserviceaccount.com",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials

def get_service(service_name='sheets', api_version='v4'):
    credentials = get_credentials()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service

@app.route('/videos', methods=['GET'])
@login_required
def sheet():
    service = get_service()
    spreadsheet_id = "1P7SQEXHAaYlm4IszRkGmtu0sM7ABZYL3cwKBte2aB58"
    range_name = "XR-Hardware!A:Z"

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    return render_template('sheet.html', values=values, title="Sheet Datas")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'New Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('bad attempt', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	
	output_size = (256,256)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('account updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your comment has been posted.', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='Comment', form=form, legend='New Comment')


@app.route('/post/<int:pid>')
def post(pid):
	post = Post.query.get_or_404(pid)
	return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:pid>/update', methods=['GET', 'POST'])
@login_required
def update_post(pid):
	post = Post.query.get_or_404(pid)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your comment updated', 'success')
		return redirect(url_for('post', pid=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update', form=form, legend='Update Comment')


@app.route('/post/<int:pid>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(pid):
	post = Post.query.get_or_404(pid)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('your comment deleted.', 'success')
	return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=3)
	return render_template('user_posts.html', posts=posts, user=user)
