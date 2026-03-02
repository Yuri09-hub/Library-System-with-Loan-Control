from models import User, Loan, Fine, Book, session
from sqlalchemy.exc import IntegrityError
d
import data_verification as verification


class Library:

    @staticmethod
    def creat_user(name, email, password, phone, id_card):
        try:
            user = User(name=name, email=email, password=password, phone=phone, id_card=id_card)
            session.add(user)
            session.commit()
            session.close()
        except IntegrityError as e:
            print(e)
