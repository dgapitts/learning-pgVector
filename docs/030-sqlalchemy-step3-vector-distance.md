## sqlalchemy-step3-vector-distance
Unfortunately this demo script - isn't working for me (yet)

```
(venv) ~/projects/learning-pgVector/bin main $ cat sqlalchemy_step3-vector-distance.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from sqlalchemy import func

engine = create_engine('postgresql://pgvector:pgvector@localhost/pgvector')
Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    embedding = Column(Vector(3))  # A 3-dimensional vector

# Create the table in the database
Base.metadata.create_all(engine)


# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Create a new item with a vector embedding
item = Item(
    name="example_item",
    embedding=[0.1, 0.2, 0.3]
)

# Add and commit the item to the database
session.add(item)
session.commit()

# Define a target vector for similarity search
target_vector = [0.1, 0.2, 0.25]

# Perform the similarity search using L2 distance (Euclidean)
similar_items = session.query(
    Item,
    func.vector_l2_distance(Item.embedding, target_vector).label('distance')
).order_by('distance').all()

for item, distance in similar_items:
    print(f'Item: {item.name}, Distance: {distance}')
```

the issue appears to be with 

> "function vector_l2_distance(vector, numeric[])" and "No function matches the given name and argument types"

i.e. 
```
(venv) ~/projects/learning-pgVector/bin main $  python3 sqlalchemy_step3-vector-distance.py
/Users/davidpitts/projects/learning-pgVector/bin/sqlalchemy_step3-vector-distance.py:8: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  Base = declarative_base()
Traceback (most recent call last):
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
psycopg2.errors.UndefinedFunction: function vector_l2_distance(vector, numeric[]) does not exist
LINE 1: ...S items_name, items.embedding AS items_embedding, vector_l2_...
                                                             ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/davidpitts/projects/learning-pgVector/bin/sqlalchemy_step3-vector-distance.py", line 43, in <module>
    ).order_by('distance').all()
                           ^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/orm/query.py", line 2673, in all
    return self._iter().all()  # type: ignore
           ^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/orm/query.py", line 2827, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2362, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2247, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1418, in execute
    return meth(
           ^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py", line 515, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1640, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2355, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "/Users/davidpitts/path/to/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedFunction) function vector_l2_distance(vector, numeric[]) does not exist
LINE 1: ...S items_name, items.embedding AS items_embedding, vector_l2_...
                                                             ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.

[SQL: SELECT items.id AS items_id, items.name AS items_name, items.embedding AS items_embedding, vector_l2_distance(items.embedding, %(vector_l2_distance_1)s) AS distance
FROM items ORDER BY distance]
[parameters: {'vector_l2_distance_1': [0.1, 0.2, 0.25]}]
(Background on this error at: https://sqlalche.me/e/20/f405)
```
