cd backend
echo "===========requirements.txt install start==========="
pip install -r requirements.txt
echo "===========requirements.txt install finish==========="

echo "===========makemigrations start==========="
python manage.py makemigrations
echo "===========makemigrations finish==========="

echo "===========migrate start==========="
python manage.py migrate
echo "===========migrate finish==========="

python manage.py runserver
