FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt gutenber.txt hunger_game.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
