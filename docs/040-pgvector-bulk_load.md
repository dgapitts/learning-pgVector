## pgvector bulk_load


Given my problems with sqlalchemy, I've switched to fllowing [pgvector-python](https://github.com/pgvector/pgvector-python/blob/master/examples/bulk_loading.py)
* I went with a 1/10 of the size - 100000 rows instead of 1000000
* I also need to install psycopg

```
(venv) ~/projects/learning-pgVector/bin main $ pip install psycopg
Collecting psycopg
  Downloading psycopg-3.2.1-py3-none-any.whl.metadata (4.2 kB)
Requirement already satisfied: typing-extensions>=4.4 in /Users/davidpitts/path/to/venv/lib/python3.12/site-packages (from psycopg) (4.12.2)
Downloading psycopg-3.2.1-py3-none-any.whl (197 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 197.7/197.7 kB 10.1 MB/s eta 0:00:00
Installing collected packages: psycopg
Successfully installed psycopg-3.2.1
```



this worked and is pretty fast

```
(venv) ~/projects/learning-pgVector/bin main $ time python3 bulk_loading.py;psql -d pgvector -c "\d+"
Loading 100000 rows
..........
Success!

real	0m1.313s
user	0m0.414s
sys	0m0.077s

                                          List of relations
 Schema |     Name     |   Type   |  Owner   | Persistence | Access method |    Size    | Description
--------+--------------+----------+----------+-------------+---------------+------------+-------------
 public | items        | table    | pgvector | permanent   | heap          | 56 MB      |
 public | items_id_seq | sequence | pgvector | permanent   |               | 8192 bytes |
```
