from library import Library
from models import session
from sqlalchemy.exc import IntegrityError

try:
    app = Library()
    app.register_user(name="Yuri", email="yuri@gmail.com", phone="934576680", id_card="00888LA039", session=session)
    session.commit()
except IntegrityError as e:
    print(e)
finally:
    session.close()
