from __init__ import db
from __init__ import app
import models

db.drop_all(app=app)
db.create_all(app=app)
