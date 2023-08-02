FROM python:3.10

RUN apt-get update && apt-get install -y ncat

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY check_db.sh /app/check_db.sh
RUN chmod +x /app/check_db.sh

ENTRYPOINT ["/app/check_db.sh"]
