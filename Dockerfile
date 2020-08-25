FROM python:3.8
LABEL Name=yemekkalmasin Version=0.0.1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip virtualenv
RUN virtualenv -p python env
RUN . env/bin/activate
RUN pip install -r requirements.txt
RUN cp -rf Sample.env .env
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]