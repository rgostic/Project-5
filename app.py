from flask import Flask, g, render_template, request, redirect, url_for

import models

app = Flask(__name__)

@app.before_request
def before_request():
	'''connect to db before each request'''
	g.db = models.DATABASE
	g.db.connect()


@app.after_request
def after_request(response):
	''' close the db connection after each request'''
	g.db.close()
	return response

@app.route('/entries')
def entries():
	
	entries = models.Entry.select()
	return render_template('index.html', entries=entries)

@app.route('/entry', methods=["GET", "POST"])
def entry():
	if request.method == "POST":
		models.Entry.create_entry(
				title = request.form["title"],
				date = request.form["date"],
				time_spent = request.form["timeSpent"],
				learned = request.form["whatILearned"],
				resources = request.form["ResourcesToRemember"]
			)
		return redirect(url_for('entries'))
	return render_template('new.html')

@app.route('/details/<int:entry_id>')
@app.route('/entries/<int:entry_id>')
def details(entry_id):
	entry = models.Entry.select().where(Entry.id == entry_id).get()

	return render_template('detail', entry)


if __name__ == "__main__":
	models.initialize()
	app.run(debug=True)