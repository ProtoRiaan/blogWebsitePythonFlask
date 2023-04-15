FROM python:3.10.11-slim-bullseye

MAINTAINER Riaan Schuld 

CMD ["ufw allow 5000"]

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


#copy project
COPY . .


#run app.py
ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]