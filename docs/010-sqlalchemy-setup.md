# sqlalchemy getting started


## setup python3 venv and install sqlalchemy psycopg2-binary
```
~  $ python3 -m venv path/to/venv
~  $ source path/to/venv/bin/activate
(venv) ~  $ python3 -m pip install sqlalchemy psycopg2-binary
Collecting sqlalchemy
  Downloading SQLAlchemy-2.0.32-cp312-cp312-macosx_11_0_arm64.whl.metadata (9.6 kB)
Collecting psycopg2-binary
  Downloading psycopg2_binary-2.9.9-cp312-cp312-macosx_11_0_arm64.whl.metadata (4.4 kB)
Collecting typing-extensions>=4.6.0 (from sqlalchemy)
  Downloading typing_extensions-4.12.2-py3-none-any.whl.metadata (3.0 kB)
Downloading SQLAlchemy-2.0.32-cp312-cp312-macosx_11_0_arm64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 47.0 MB/s eta 0:00:00
Downloading psycopg2_binary-2.9.9-cp312-cp312-macosx_11_0_arm64.whl (2.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.6/2.6 MB 88.1 MB/s eta 0:00:00
Downloading typing_extensions-4.12.2-py3-none-any.whl (37 kB)
...
```

## setup pgvector database 


```
CREATE DATABASE pgvector;
CREATE USER pgvector WITH PASSWORD '...';
GRANT ALL PRIVILEGES ON DATABASE pgvector TO pgvector;
```

to prevent 

```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.InsufficientPrivilege) permission denied for schema public
```

I also ran

```
GRANT ALL PRIVILEGES ON SCHEMA public TO pgvector;
```


## Building first table


```
(venv) ~/projects/learning-pgVector/bin main $ cat sqlalchemy_setup.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://pgvector:...@localhost/pgvector')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
```

Running this generates a `deprecated` warning
```
(venv) ~/projects/learning-pgVector/bin main $ python3 sqlalchemy_setup.py
/Users/davidpitts/projects/learning-pgVector/bin/sqlalchemy_setup.py:7: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  Base = declarative_base()
```
But we have our table
```
(venv) ~/projects/learning-pgVector/bin main $ psql -d pgvector -c "\d users"
                                 Table "public.users"
 Column |       Type        | Collation | Nullable |              Default
--------+-------------------+-----------+----------+-----------------------------------
 id     | integer           |           | not null | nextval('users_id_seq'::regclass)
 name   | character varying |           |          |
 age    | integer           |           |          |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
```


