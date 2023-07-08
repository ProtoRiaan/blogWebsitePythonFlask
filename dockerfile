FROM python:3.10.11-slim-bullseye

LABEL author='Riaan Schuld' 

RUN pip install --upgrade pip

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN groupadd -g "${GID}" flask \
&& useradd --create-home --no-log-init -u "${UID}" -g "${GID}" flask \
&& chown flask:flask -R /app 

USER flask

# set environment variables
ENV PYTHONDONTWRITEBYTECODE="true" \
PYTHONUNBUFFERED="true" \
FLASK_APP='flaskblog'

# install dependencies

COPY --chown=flask:flask ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt


#copy project
COPY --chown=flask:flask . .

EXPOSE 8000

#run app.py
ENTRYPOINT [ "/home/flask/.local/bin/gunicorn" ]

CMD [ "-w 4", "-b 0.0.0.0", "run:app" ]
