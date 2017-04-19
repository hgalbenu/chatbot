# kirkwood

## generate migrations
python3 manage.py makemigrations

## run local migration
python3 manage.py migrate

## run tests
python3 manage.py test [--parallel]

## heroku: alembic run remote migration
heroku run 'python3 manage.py migrate'

## heroku: psql shell
heroku pg:psql

## heroku: run custom management command
heroku run 'python3 manage.py sync_heavenly'
heroku run 'python3 manage.py sync_intercom'
