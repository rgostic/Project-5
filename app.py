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
@app.route('/')
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

@app.route('/edit/<int:entry_id>', methods=["GET", "POST"])
@app.route('/entries/edit/<int:entry_id>', methods=["GET", "POST"])
@app.route('/entry/<int:entry_id>', methods=["GET", "POST"])
def edit(entry_id):
	if request.method == "POST":
		#update and save entry
		entry = models.Entry.select().where(models.Entry.id == entry_id).get()
		entry.title = request.form["title"]
		entry.date = request.form["date"]
		entry.time_spent = request.form["timeSpent"]
		entry.learned = request.form["whatILearned"]
		entry.resources = request.form["ResourcesToRemember"]

		entry.save()
		return redirect(url_for('entries', entry_id=entry_id))
	entry = models.Entry.select().where(models.Entry.id == entry_id).get()
	return render_template('edit.html', entry=entry)

@app.route('/entries/<int:entry_id>')
@app.route('/details/<int:entry_id>')
def details(entry_id):
	entry = models.Entry.select().where(models.Entry.id == entry_id).get()
	return render_template('detail.html', entry=entry)



if __name__ == "__main__":
	models.initialize()
	app.run(debug=True)