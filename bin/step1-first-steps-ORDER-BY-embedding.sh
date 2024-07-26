# as per https://github.com/pgvector/pgvector
# still working through basic demos
psql -c "DROP TABLE IF EXISTS items;"
psql -c "CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3)); INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'); SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5; "


# BEGIN sample output
: <<'END'
~/projects/learning-pgVector  $ psql -c "CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3)); INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'); SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5; "
CREATE TABLE
INSERT 0 2
 id | embedding
----+-----------
  1 | [1,2,3]
  2 | [4,5,6]
(2 rows)
END
# END sample output
