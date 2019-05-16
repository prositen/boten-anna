FROM python:3.6
WORKDIR app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONPATH .
ENV SLACKBOT_API_TOKEN replace_me
CMD [ "python", "./annabot.py" ]
