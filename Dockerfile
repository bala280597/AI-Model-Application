FROM python:3.6-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential
#ENTRYPOINT ["python", "main.py"]
EXPOSE 7000
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]

