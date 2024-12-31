

### Getting started

First question to ChatGPT was 

> How do I get started with pgVector and learning about AI.

and this lead to 

* [step 0 - base install](bin/step0-base-install.sh)
* [step 1 - first steps with ORDER-BY embedding](bin/step1-first-steps-ORDER-BY-embedding.sh)

### Background sqlalchemy

* [sqlalchemy-setup](docs/010-sqlalchemy-setup.md)
* [sqlalchemy-crud-operations](docs/020-sqlalchemy-crud-operations.md)


### Tests

* [Barcelona PUG Nov-2024 - Vectors Storage Challenges](docs/100-Barcelona_PUG_Nov-2024_Vectors-Storage-Challenges.md)


### Brew notes

* first the `bin/step0-base-install.sh` work on linux and macosx, including pg installed via brew
* brew service commands - note `info` instead of `status`

```
brew services info postgresql@16
brew services start postgresql@16
brew services restart postgresql@16
brew services stop postgresql@16
```

you can all use `pg_ctl`
```
/opt/homebrew/opt/postgresql@16/bin/pg_ctl stop -D /opt/homebrew/var/postgresql@16
```



