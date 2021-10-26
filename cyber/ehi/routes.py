from flask import Blueprint, render_template, send_file, abort, request, url_for, redirect
from flask_login import current_user, login_required
from io import BytesIO
from cyber.models import Ehi
from cyber import admins, db

EHI = Blueprint('EHi', __name__)

@EHI.route('/ehi')
@login_required
def ehi():
    ehifiles = Ehi.query.all()
    return render_template('main/ehi.html', ehifiles=ehifiles, title='ehi')

@EHI.route('/ehi/upload', methods=['POST'])
def upload_ehi():
    if current_user.is_authenticated:
        if current_user.email in admins:
            if request.method == 'POST':
                ehifile = request.files['ehi']
                newehi = Ehi(name=ehifile.filename, data=ehifile.read())
                db.session.add(newehi)
                db.session.commit()
            return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
        else:
            abort(404)
    else:
        abort(404)

@EHI.route('/file/download/<int:file_id>')
@login_required
def ehi_download(file_id):
    file_data = Ehi.query.get_or_404(file_id)
    return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True)

