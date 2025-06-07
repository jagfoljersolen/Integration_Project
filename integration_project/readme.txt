venv
https://stackoverflow.com/questions/42733542/how-to-use-the-same-python-virtualenv-on-both-windows-and-linux

pip freeze > requirements.txt

[linux]
python -m venv isenv
source isenv/bin/activate
pip install -r requirements.txt  # Install all the libs.


migracje
python manage.py makemigrations app
python manage.py migrate
[powershell] 
py manage.py makemigrations app
py manage.py migrate

import danych
python manage.py import_commodities data/commodity.csv
python manage.py import_commodity_with_units data/commodity_with_units.csv
python manage.py import_conflicts data/conflicts.csv --batch-size 1000
[powershell, cmd]
py manage.py import_commodity data/commodity.csv
py manage.py import_commodity_with_units data/commodity_with_units.csv
py manage.py import_conflicts data/conflicts.csv --batch-size 1000

logowanie
admin
admin@dmin.com
admin1234



https://getbootstrap.com/docs/4.1/content/tables/