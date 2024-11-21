## Overview - Barcelona PUG Nov-2024 - Vectors Storage Challenges

I've added details for the pgbench euclidean_product with "full vactor (int32)"  tests which I presented at the Barcelona Postgres User Goup (PUG) in November 2024. 

I've also added the scripts to my `pyday-bcn-2024` (I seemed to mixed up Barcelona pyDay and PUG sqlalchemy as I working on both simultaneously - apologies)

To run the scripts, exactly as the instructions below (atleast for Mac and Linux)

```
mkdir ~/projects
cd ~/projects
git clone https://github.com/dgapitts/pyday-bcn-2024
```

There are two appendix
* Appendix A - my pgbench_euclid32 test results
* Appendix B - Getting started with docker ankane/pgvector

Finally the [slide-deck found here](slideshare-BCN-PUG-Nov-2024-vectors-storage-challenges.pdf) 


## Setup

### Base table

Note as per the docker details below, I'm mapping post 5432 within the container to localhost:5433 which I've hard-coded into my setup script.

The setup script is to be run directly from your laptop (i.e. not within the docker shell)

```
(venv) ~/projects/pyday-bcn-2024/py main $ cat setup_v2.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector

import numpy as np
size=2

table="v"+str(size)
print (table)

# Define the database URL
DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5433"

# Create the engine
engine = create_engine(DATABASE_URL)

# Define the base class for declarative models
Base = declarative_base()

# Define the SQLAlchemy model
class Item(Base):
    __tablename__ = table

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    embedding = Column(Vector(size))

# Create the table in the database
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

for i in range(0,10):
    for j in range(0,1000):
        # Generate the random numbers
        # print (str(i)+"-"+str(j))
        random_array = np.random.rand(size)

        item = Item(
            name="example_item",
            embedding=random_array
        )

        # Add and commit the item to the database
        session.add(item)
        session.commit()
session.commit()
```

to run this


```
cd ~/projects/pyday-bcn-2024/py
python3 setup_v2.py
python3 setup_v4.py
python3 setup_v8.py
python3 setup_v16.py
python3 setup_v32.py
python3 setup_v64.py
python3 setup_v128.py
python3 setup_v256.py
python3 setup_v512.py
python3 setup_v1024.py
```


### Add index

From psql i.e.
```
docker exec -it my_postgres psql -U postgres
```
NB (POSTGRES_PASSWORD=mysecretpassword)



run

```
CREATE INDEX IF NOT EXISTS v2_embedding_ivfflat_idx ON v2 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v4_embedding_ivfflat_idx ON v4 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v8_embedding_ivfflat_idx ON v8 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v16_embedding_ivfflat_idx ON v16 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v32_embedding_ivfflat_idx ON v32 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v64_embedding_ivfflat_idx ON v64 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v128_embedding_ivfflat_idx ON v128 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v256_embedding_ivfflat_idx ON v256 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v512_embedding_ivfflat_idx ON v512 USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS v1024_embedding_ivfflat_idx ON v1024 USING ivfflat (embedding) WITH (lists = 100);
```

## Upload pgbench_euclid32_tests.tar


```
docker cp  ~/projects/pyday-bcn-2024/sql/pgbench_euclid32.tar dc465c92a2a4:/tmp
```

## Run tests


# Appendix A - my pgbench_euclid32 test results

### summary of test results
```
test,tps
v2,7709
v4,8052
v8,8317
v16,8361
v32,8272
v64,7705
v128,7646
v256,6549
v512,2191
v1024,1373
```

### details for test results

```
postgres@dc465c92a2a4:~$ pgbench -f pgbench_v2.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v2.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.130 ms
initial connection time = 1.883 ms
tps = 7709.505821 (without initial connection time)

postgres@dc465c92a2a4:~$ pgbench -f pgbench_v4.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v4.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.124 ms
initial connection time = 1.905 ms
tps = 8052.048441 (without initial connection time)


postgres@dc465c92a2a4:~$ pgbench -f pgbench_v8.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v8.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.120 ms
initial connection time = 1.683 ms
tps = 8317.391666 (without initial connection time)


postgres@dc465c92a2a4:~$ pgbench -f pgbench_v16.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v16.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.120 ms
initial connection time = 1.707 ms
tps = 8361.343835 (without initial connection time)


postgres@dc465c92a2a4:~$ pgbench -f pgbench_v32.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v32.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.121 ms
initial connection time = 1.570 ms
tps = 8272.940865 (without initial connection time)


postgres@dc465c92a2a4:~$ pgbench -f pgbench_v64.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v64.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.130 ms
initial connection time = 1.603 ms
tps = 7705.228768 (without initial connection time)


postgres@dc465c92a2a4:~$ pgbench -f pgbench_v128.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v128.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.131 ms
initial connection time = 1.831 ms
tps = 7646.779941 (without initial connection time)


postgres@dc465c92a2a4:~$ pgbench -f pgbench_v256.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v256.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.153 ms
initial connection time = 1.782 ms
tps = 6549.560524 (without initial connection time)

postgres@dc465c92a2a4:~$ pgbench -f pgbench_v512.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v512.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.456 ms
initial connection time = 1.797 ms
tps = 2191.463810 (without initial connection time)

postgres@dc465c92a2a4:~$ pgbench -f pgbench_v1024.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v1024.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.728 ms
initial connection time = 1.716 ms
tps = 1373.645242 (without initial connection time)
```


# Apendix B - Getting started with docker ankane/pgvector

## Download docker pgvector

```
docker pull ankane/pgvector
docker images
```

## Running pgvector container
```
docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5433:5432 -d postgres ankane/pgvector
```

## Connecting via psql (POSTGRES_PASSWORD=mysecretpassword)
```
docker exec -it my_postgres psql -U postgres
```

## Connecting vie bash 


```
docker ps        # to get container-id e.g. dc465c92a2a4 for me 
docker exec -it dc465c92a2a4 bash
```

for example to run local pgbench tests

```
postgres@dc465c92a2a4:~$ pgbench -f pgbench_v8.sql -c 1 -t 500
pgbench (15.4 (Debian 15.4-2.pgdg120+1))
starting vacuum...end.
transaction type: pgbench_v8.sql
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
maximum number of tries: 1
number of transactions per client: 500
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 0.120 ms
initial connection time = 1.683 ms
tps = 8317.391666 (without initial connection time)
```




