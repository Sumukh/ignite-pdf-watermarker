import tempfile

from flask import Blueprint, render_template, abort, redirect, url_for, flash, send_file
from flask_login import login_required, current_user

from appname.extensions import storage
from appname.models import db
from appname.models.teams import Team
from appname.models.team_file import TeamFile
from appname.forms.files import WatermarkForm
from appname.helpers.pdf import watermark_pdf

blueprint = Blueprint('dashboard_home', __name__)

@blueprint.route('/')
@login_required
def index():
    if current_user.active_memberships:
        return redirect(url_for('.home', team_id=current_user.active_memberships[0].team.id))
    else:
        flash("You are not part of any teams", 'warning')
        return redirect(url_for('user_settings.memberships'))

@blueprint.route('/<hashid:team_id>')
@login_required
def home(team_id):
    team = Team.query.get(team_id)
    if not team or not team.has_member(current_user):
        abort(404)
    watermark_form = WatermarkForm()

    return render_template('dashboard/home.html', team=team, watermark_form=watermark_form)

@blueprint.route('/<hashid:team_id>/submit_watermark', methods=["POST"])
@login_required
def handle_watermark(team_id):
    team = Team.query.get(team_id)
    if not team or not team.has_member(current_user):
        abort(404)

    form = WatermarkForm()

    if form.validate_on_submit():
        new_file = watermark_pdf(form.watermark.data, form.attachment.data)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as outfile:
            new_file.save(outfile)
            file_data = open(outfile.name, 'rb')
            attachment = storage.upload(file_data.name)

            team_file = TeamFile(team=team, user=current_user, description=form.watermark.data,
                                 file_name=attachment.info['name'],
                                 file_object_name=attachment.name)
            db.session.add(team_file)
            db.session.commit()
            file_data.seek(0)

            return send_file(file_data, download_name="Watermarked.pdf")

    return abort(404)
