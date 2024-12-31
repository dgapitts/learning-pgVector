# as per https://github.com/pgvector/pgvector
# refer to latest version of the README for current version (v0.8.0 and beyond) of pgVector

cd /tmp
git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo

cd ~/projects/learning-pgVector/
psql -U postgres -c "CREATE EXTENSION vector"

