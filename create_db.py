from app import create_app, db
from app.models import User, Task, Completion

app = create_app()
with app.app_context():
    db.create_all()
    print("Таблицы успешно созданы!")
