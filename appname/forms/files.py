from appname.forms import BaseForm
from wtforms import validators, TextAreaField, FileField

class FileForm(BaseForm):
    description = TextAreaField('Description')
    attachment = FileField('Attachment', validators=[validators.InputRequired()])
class WatermarkForm(BaseForm):
    watermark = TextAreaField('Watermark Text', validators=[validators.InputRequired()])
    attachment = FileField('Attachment', validators=[validators.InputRequired()])
