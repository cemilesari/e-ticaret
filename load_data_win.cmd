set ENVIROO=python

set MANAGER=manage.py

del /F db.sqlite3
%ENVIROO% %MANAGER% reseter
%ENVIROO% %MANAGER% makemigrations core
%ENVIROO% %MANAGER% makemigrations users
%ENVIROO% %MANAGER% makemigrations notify
%ENVIROO% %MANAGER% makemigrations
%ENVIROO% %MANAGER% migrate

%ENVIROO% %MANAGER% load_new

set RUN_PROJECT=%ENVIROO% %MANAGER% runserver 0.0.0.0:8000
%RUN_PROJECT%