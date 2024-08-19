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
