import  psycopg2
from models.models import Task

db = psycopg2.connect("user=postgres password=postgres dbname=qa_bot host=localhost port=5432")
cursor = db.cursor()

task = Task()
task.images = ""                                                                                                                    

task.text = "simple task text"

task.topic = "simple topic"

task.answer = "followed answer"

cursor.execute(task.insertThis())

db.commit()

db.close()
