from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields import BooleanField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError
import re


app = Flask(__name__)
app.secret_key = 'SSHHHH!!!'


def edit_profile(request):
        user = request.current_user
        form = ProfileForm(request.POST, user)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        user.save()
        redirect('edit_profile')
    return render_template('edit_profile.html', form=form)


class MyForm(FlaskForm):
    name = StringField('Name', validators=InputRequired())


class RegistrationForm(FlaskForm):
    def validate_password(form, field):
        match_list = []

        digit_match = re.search('[0-9]', field.data)
        upper_match = re.search('[A-Z]', field.data)
        lower_match = re.search('[a-z]', field.data)
        symbol_match = re.search('[~`!@#$%^&*(),.?":{}|<>/*+]', field.data)

        if digit_match:
            print('digit case match: true')
            match_list.append(1)
        else:
            print('digit case match: false')
            match_list.append(0)

        if upper_match:
            print('upper case match: true')
            match_list.append(1)
        else:
            print('upper case match: false')
            match_list.append(0)

        if lower_match:
            print('lower case match: true')
            match_list.append(1)
        else:
            print('lower case match: false')
            match_list.append(0)

        if symbol_match:
            print('symbol case match: true')
            match_list.append(1)
        else:
            print('symbol case match: false')
            match_list.append(0)

        print(f"boolean list of match cases: {match_list}")
        if 0 in match_list:
            print('requirement missing - raising error')
            raise ValidationError('Password must contain at least 1: lower case letter, upper case letter, digit, special character')

    username = StringField('Username', [Length(min=4, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35),  Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=35)])
    accept_rules = BooleanField('I accept the site rules', [InputRequired()])


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = RegistrationForm()
    if form.validate_on_submit():
        return '<a href="/">Try Again</a>'
    print(form.errors)
    return render_template('base.html', form=form)


if __name__ == '__main__':
    app.run()