FROM python:3.9.1

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod 777 /usr/src/app/entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
