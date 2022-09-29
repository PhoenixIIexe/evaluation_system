from __init__ import db
from __init__ import app
import models

db.create_all(app=app)
