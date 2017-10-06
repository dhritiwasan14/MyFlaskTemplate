from flask import Flask, render_template, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask import request
app = Flask(__name__)
class SearchForm(Form):
	search = StringField(" ", [validators.Length(min=4, max=30)], render_kw={'placeholder':'Search'})
@app.route('/', methods=['GET'])
def home():
	form = SearchForm(request.form)
	if request.method == 'POST' and form.validate():
		return redirect(url_for('search', q=form.search.data))
	return render_template('home.html', form=form)

if __name__ == "__main__":
	app.run(debug=True)