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

Base.metadata.create_all(engine)

new_user = User(name='John Doe', age=30)
session.add(new_user)
session.commit()

users = session.query(User).all()
for user in users:
    print(user.name, user.age)

user = session.query(User).filter_by(name='John Doe').first()
user.age = 31
session.commit()

user = session.query(User).filter_by(name='John Doe').first()
session.delete(user)
session.commit()


try:
    session.add(new_user)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()


