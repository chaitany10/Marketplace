
### Setting up Virtual Environment and Install Requirements
```bash
sudo pip install virtualenv
python3 -m venv myvenv
source myvenv/bin/activate
pip install Django==3.0.4
```

### Running the website locally
```bash
cd ~/auction
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
