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

