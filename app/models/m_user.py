from typing import Dict, List, Optional
from empiricus_tests.app.models import db


class UsersModel(db.Model):
    __tablename__ = 'users'

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)

    def __init__(self, username: str, avatar: str, email: str, city: str):
        self.username = username
        self.avatar = avatar
        self.email = email
        self.city = city

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_table_length(cls) -> int:
        return cls.query.count()

    @classmethod
    def get_table_chunck(cls, start, end) -> List['UsersModel']:
        row_number = db.func.row_number().over(order_by=cls.id_).label('row_number')
        q = db.session.query(cls).add_column(row_number)
        return [i[0] for i in q.from_self().filter(row_number >= start).filter(row_number <= end).all()]

    @classmethod
    def find_by(cls, option, **kwargs) -> Optional['UsersModel']:
        if option == 'username':
            return cls.query.filter_by(username=kwargs.get('username')).first()
        elif option == 'email':
            return cls.query.filter_by(email=kwargs.get('email')).first()
        return None

    def response(self) -> Dict[str, str]:
        return {'username': self.username, 'avatar': self.avatar,
                'email': self.email, 'city': self.city}
