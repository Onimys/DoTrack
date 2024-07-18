task dev
alembic revision --autogenerate -m "add user table"

docker build . -t dotrack/projects:0.1.0
