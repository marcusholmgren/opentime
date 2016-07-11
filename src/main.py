"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import DateField, DecimalField, StringField, SubmitField, validators
import datetime 
from google.appengine.ext import ndb
from config import SECRET_KEY

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app.config['SECRET_KEY'] = SECRET_KEY

class TimeEntry(ndb.Model):
    code = ndb.StringProperty()
    time = ndb.FloatProperty()

    def __repr__(self):
        return "[{0} {1}]".format(self._class_name, self.code)


class DayModule(ndb.Model):
    day = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    details = ndb.LocalStructuredProperty(TimeEntry, repeated=True)

    def __repr__(self):
        return "[{0} {1}]".format(self._class_name(), self.day)

    @staticmethod
    def create():
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        return DayModule(day=now)

    def add_time(self, code, time):
        te = None
        for entry in self.details:
            if entry.code == code:
                te = entry
        if te:
            te.time += time
        else:
            self.details.append(TimeEntry(code=code, time=time))


class TimeEntryForm(Form):
    day = DateField(u'Day', default=datetime.date.today(), validators=[validators.InputRequired(message="Please provide a day")])
    code = StringField(u'Time code', validators=[validators.InputRequired()])
    time = DecimalField(u'Worked hours:', validators=[validators.InputRequired()])
    submit = SubmitField(u'Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = TimeEntryForm()
    if form.validate_on_submit():
        old_code = session.get('code')
        if old_code is not None and old_code != form.code.data:
            flash('Looks like you have changed project code!')
        app.logger.debug("Form validate name %s" % form.code.data)
        session['code'] = form.code.data
        form.code.data = ''
        return redirect(url_for('index'))
    #app.logger.debug("Index method called. Name is %s" % session.get("name"))
    return render_template('register_time.html', form=form, name=session.get('code'))


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    app.logger.debug("Hello method called name: %s" % name)
    return render_template('index.html', name=name, form=TimeEntryForm())


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    app.logger.error('Unexpected error: {}'.format(e))
    return 'Sorry, unexpected error: {}'.format(e), 500
