import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database
from urllib.parse import quote
from flask_login import UserMixin

Base = declarative_base()
class FunctionalClass(Base):
    __tablename__ = 'functional_classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(length=150), unique=True, nullable=False)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(length=50), unique=True, nullable=False)

class TerritorialCenter(Base):
    __tablename__ = 'territorial_centers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    center_name = Column(String(length=255), unique=True, nullable=False)
    director_full_name = Column(String(length=255), nullable=False)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(length=255), unique=True, nullable=False)

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=150), unique=True, nullable=False)
    surname = Column(String(length=150), nullable=False)
    first_name = Column(String(length=150), nullable=False)
    patronymic = Column(String(length=150), nullable=False)
    password = Column(String(length=150), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    territorial_center_id = Column(Integer, ForeignKey('territorial_centers.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))
    start_date = Column(Date, nullable=True)

    role = relationship("Role")
    territorial_center = relationship("TerritorialCenter")
    department = relationship("Department")

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(length=150), nullable=False)
    first_name = Column(String(length=150), nullable=False)
    patronymic = Column(String(length=150), nullable=False)
    address = Column(String(length=250), nullable=False)
    func_class = Column(Integer, ForeignKey('functional_classes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    contract_number = Column(String(length=150), nullable=False)
    contract_date = Column(Date)
    birth_date = Column(Date)
    phone_number = Column(String(length=20))
    contract_end_date = Column(Date)
    visit_count = Column(Integer, default=0)
    status = Column(Enum('Активен', 'Не активен'))
    gender = Column(Enum('М', 'Ж'))

    functional_class = relationship("FunctionalClass")
    user = relationship("User")

class ServiceType(Base):
    __tablename__ = 'services_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(length=255), nullable=False)

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    service_type_id = Column(Integer, ForeignKey('services_types.id'), nullable=False)
    social_worker_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship("Client")
    social_worker = relationship("User")
    service_type = relationship("ServiceType")

class DepartmentTerritorialCenter(Base):
    __tablename__ = 'department_territorial_centers'
    department_id = Column(Integer, ForeignKey('departments.id'), primary_key=True)
    territorial_center_id = Column(Integer, ForeignKey('territorial_centers.id'), primary_key=True)

class FunctionalClassServiceType(Base):
    __tablename__ = 'functional_class_services_types'
    functional_class_id = Column(Integer, ForeignKey('functional_classes.id'), primary_key=True)
    service_type_id = Column(Integer, ForeignKey('services_types.id'), primary_key=True)


class ORM:
    def __init__(self):
        self._engine = None
        self._cur_session = None

    def start_session(self):
        password = quote("YOUR_PASSWORD") # ваш пароль
        connection_string = f"mysql+pymysql://root:{password}@localhost:3306/diplom"   # строка с вашими данными о подключении
        self._engine = create_engine(connection_string, connect_args={'charset': 'utf8'})

        if not database_exists(self._engine.url):
            create_database(self._engine.url)

        Base.metadata.create_all(self._engine)
        session = sessionmaker(bind=self._engine)
        self._cur_session = session()

    def close_session(self):
        self._cur_session.close()

    def add_inst(self, inst):
        self._cur_session.add(inst)
        self.commit()

    def commit(self):
        self._cur_session.commit()

    def get_data(self, entity):
        return self._cur_session.query(entity)

    def get_by_id(self, entity, id):
        return self._cur_session.query(entity).filter(entity.id == id).first()

    def delete_inst(self, inst):
        self._cur_session.delete(inst)
        self.commit()
