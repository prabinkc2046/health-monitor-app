FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

 
ENV DB_USER="flask"
ENV DB_PASSWORD="flask"
ENV DB_HOST="mysql-host"
ENV DB_NAME="usage_data"

EXPOSE 5000
CMD ["python","fetch_result.py"]
