import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
	title = CharField()
	date = DateTimeField(default=datetime.datetime.now)	
	time_spent = CharField()
	learned = TextField()
	resources = TextField()

	class Meta:
		database = DATABASE
		order_by = ('-date',)

	@classmethod
	def create_entry(cls, title, date, time_spent, learned, resources):
		try:
			
			cls.create(
				title=title,
				date=date,
				time_spent=time_spent,
				learned=learned,
				resources=resources
				)
		except IntegrityError:
			raise ValueError("User already exists")

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Entry], safe=True)
	DATABASE.close()