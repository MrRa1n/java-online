from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

class CreateChallengeForm(FlaskForm):
    # title
    title = StringField('Title')
    # instructions
    instructions = TextAreaField('Instructions')
    # rel - code (model)
    code = HiddenField('Code', id='code_hidden')
    # rel - resource (model)
    resources = StringField('Resources')
    # rel - code (model)
    tests = HiddenField('Tests', id='tests_hidden')
    # submit
    submit = SubmitField('Create', id='create_challenge')