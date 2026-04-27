from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Проверяем, есть ли уже колонка points
        result = db.session.execute(text("PRAGMA table_info(user)"))
        columns = [row[1] for row in result]
        if 'points' not in columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN points INTEGER DEFAULT 0"))
            db.session.commit()
            print("Колонка 'points' успешно добавлена.")
        else:
            print("Колонка 'points' уже существует.")
    except Exception as e:
        print(f"Ошибка: {e}")
