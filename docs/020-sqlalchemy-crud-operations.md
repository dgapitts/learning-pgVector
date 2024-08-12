### sqlalchemy CRUD code

## Create and Read 
```
(venv) ~/projects/learning-pgVector/bin main $ cat sqlalchemy_step2-crud.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://pgvector:pgvector@localhost/pgvector')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Session = sessionmaker(bind=engine)
session = Session()


new_user = User(name='John Doe', age=30)
session.add(new_user)
session.commit()

users = session.query(User).all()
for user in users:
    print(user.name, user.age)
```
and output 
```
(venv) ~/projects/learning-pgVector/bin main $ python3 sqlalchemy_step2-crud.py
/Users/davidpitts/projects/learning-pgVector/bin/sqlalchemy_step2-crud.py:6: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  Base = declarative_base()
John Doe 30
```
