echo "=========makemigrations========="
python manage.py makemigrations
echo "=========finish makemigrations========="
echo "=========migrate========="
python manage.py migrate
echo "=========finish migrate========="

python manage.py runserver