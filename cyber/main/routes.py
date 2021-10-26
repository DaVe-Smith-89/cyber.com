from flask import Blueprint, render_template, jsonify, request, url_for, send_file, session, redirect, abort, flash, make_response
from flask_login import current_user, login_required
from cyber.models import User, Post, Tool, Lesson, Ehi, adminModelView, SpecialFile, userModelView, fileModelView, HomePagePosts, EmailSystem
from cyber import db, admin, admins, bcrypt, app
from cyber.main.forms import EmailSystemRegisterForm
from io import BytesIO
from requests import get
from random import choices
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

admin.add_view(userModelView(User, db.session))
admin.add_view(adminModelView(Post, db.session))
admin.add_view(adminModelView(EmailSystem, db.session))
admin.add_view(adminModelView(Lesson, db.session))
admin.add_view(adminModelView(Tool, db.session))
admin.add_view(fileModelView(Ehi, db.session, category='Uploads'))
admin.add_view(fileModelView(SpecialFile, db.session, category='Uploads'))

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    while True:
        lessons = choices(Lesson.query.all(), k=3)
        if len(lessons) == len(set(lessons)):
            break
    techcrunch = choices(eval(HomePagePosts.query.filter_by(source='techcrunch').first().data)['articles'], k=3)
    form = EmailSystemRegisterForm()
    if form.validate_on_submit():
        email = EmailSystem(email=form.email.data)
        db.session.add(email)
        db.session.commit()
    return render_template('main/home.html', techcrunch=techcrunch, lessons=lessons, form=form)

@main.route('/3xf8z81HUddaTkyqZBXJm9PG/refreshposts')
def refresh_posts():
    if current_user.is_authenticated:
        if current_user.email in admins:
            if 'admin_token' in session:
                if bcrypt.check_password_hash(session['admin_token'], 'kariponnaya'):
                    techcrunch = HomePagePosts.query.filter_by(source='techcrunch').first()
                    techcrunchdata = get('https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=e4158e76f9b04f0293995be6328537fa').json()
                    if techcrunch:
                        techcrunch.data = str(techcrunchdata)
                        techcrunch.date = datetime.utcnow()
                        db.session.commit()
                        flash('Record Updated Successfully.', 'success')
                    else:
                        techcrunch = HomePagePosts(source='techcrunch', data=str(techcrunchdata))
                        db.session.add(techcrunch)
                        db.session.commit()
            return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
        else:
            abort(403)
    else:
        abort(403)

@main.route('/about')
def about():
    return render_template('main/about.html', title='About')

@main.route('/services')
def services():
    return render_template('main/services.html', title='Services')

@main.route('/lessons', methods=['GET', 'POST'])
@login_required
def lessons():
    if request.method == 'POST':
        try:
            data = request.form['aim']
            post = Lesson.query.filter(Lesson.title.like('%'+data+'%')).first()
            data = { 'id': post.id, 'title': post.title}
            return jsonify(data)
        except:
            pass
    lessons = reversed(Lesson.query.all())
    return render_template('main/lessons.html', lessons=lessons, title='Lessons')

@main.route('/lessons/<int:lesson_id>')
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    social = {'decsription': lesson.description[:200], 'image': None}
    return render_template('main/lesson.html', lesson=lesson, social=social, title=lesson.title)

@main.route('/tools', methods=['GET', 'POST'])
@login_required
def tools():
    if request.method == 'POST':
        try:
            data = request.form['aim']
            tool = Tool.query.filter(Tool.title.like('%'+data+'%')).first()
            data = { 'id': tool.id, 'title': tool.title}
            return jsonify(data)
        except:
            pass
    tools = reversed(Tool.query.all())
    return render_template('main/tools.html', tools=tools, title='Tools')

@main.route('/tools/<int:tool_id>')
def tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    social = {'decsription': tool.description, 'image': str(tool.tool_img)}
    return render_template('main/tool.html', tool=tool, title=str(tool.title), description=tool.description, social=social)

@main.route('/file/upload', methods=['POST'])
@login_required
def file_upload():
    if current_user.is_authenticated:
        if current_user.email in admins:
            if 'admin_token' in session:
                if bcrypt.check_password_hash(session['admin_token'], 'kariponnaya'):
                    if request.method == 'POST':
                        ehifile = request.files['ehi']
                        newehi = SpecialFile(name=ehifile.filename, data=ehifile.read())
                        db.session.add(newehi)
                        db.session.commit()
            return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
        else:
            abort(404)
    else:
        abort(404)

@main.route('/specialfile/download/<int:file_id>')
@login_required
def file_download(file_id):
    file_data = SpecialFile.query.get_or_404(file_id)
    return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True)

@main.route('/3xf8z81HUddaTkyqZBXJm9PG/log', methods=['POST'])
def log_admin():
    if request.form['email'] in admins:
        if  request.form['password'] == 'kariponnaya':
            user = request.form['email']
            session['admin_token'] = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            flash(f'Successfully logged as {user}', 'success')
            return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
        return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
    return redirect('/3xf8z81HUddaTkyqZBXJm9PG')

@main.route('/3xf8z81HUddaTkyqZBXJm9PG/logout')
def logout_admin():
    session.clear()
    flash('loged out Successfully.', 'success')
    return redirect('/3xf8z81HUddaTkyqZBXJm9PG')

@main.route('/sitemap.xml', methods=['GET'])
def sitemap():
    try:
        """Generate sitemap.xml. Makes a list of urls and date modified."""
        pages=[]
        ten_days_ago=(datetime.now() - timedelta(days=7)).date().isoformat()
        # static pages
        for rule in app.url_map.iter_rules():
            if not ('/3xf8z81HUddaTkyqZBXJm9PG' in str(rule.rule)) and ("GET" in rule.methods and len(rule.arguments)==0):
                pages.append(
                            ["https://slcyberwarriors.com"+str(rule.rule),ten_days_ago]
                            )

        sitemap_xml = render_template('sitemap_template.xml', pages=pages)
        response= make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"    

        return response
    except Exception as e:
        return(str(e))
