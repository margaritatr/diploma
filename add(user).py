from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from DAL import ORM, User

app = Flask(__name__)
bcrypt = Bcrypt(app)

orm = ORM()
orm.start_session()

Session = sessionmaker(bind=orm._engine)
session = Session()

# ---------- Данные пользователей ----------
users_data = [
    ('admin', 'Иванов', 'Иван', 'Иванович', 'password1', 1, 1, None, '2023-01-01'),
    ('social1', 'Петров', 'Петр', 'Петрович', 'password2', 2, 2, 1, '2024-01-01'),
    ('social2', 'Сидоров', 'Сидор', 'Сидорович', 'password3', 2, 3, 1, '2023-01-01'),
    ('inspector1', 'Алексеева', 'Анна', 'Алексеевна', 'password4', 3, 4, 1, '2024-01-01')
]

# ---------- Вставка пользователей ----------
for username, surname, first_name, patronymic, password, role_id, territorial_center_id, department_id, start_date in users_data:
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(
        username=username,
        surname=surname,
        first_name=first_name,
        patronymic=patronymic,
        password=hashed_password,
        role_id=role_id,
        territorial_center_id=territorial_center_id,
        department_id=department_id,
        start_date=start_date
    )

    session.add(user)

session.commit()
session.close()
