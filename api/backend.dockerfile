FROM python:3.10-slim-buster

WORKDIR /usr
COPY . .

# Set the python path:
ENV PYTHONPATH="$PYTHONPATH:${PWD}"

RUN pip install --upgrade pip  && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]

EXPOSE 3000
