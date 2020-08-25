ENVIROO=./env/bin/python
MANAGER=manage.py
if [ "$1" == "--reset" ]; then
	rm -rf db.sqlite3
	$ENVIROO $MANAGER reseter
	$ENVIROO $MANAGER makemigrations
	$ENVIROO $MANAGER migrate
fi
$ENVIROO $MANAGER load_new

RUN_PROJECT="$ENVIROO $MANAGER runserver 0.0.0.0:8000"
echo $RUN_PROJECT
$RUN_PROJECT