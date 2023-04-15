FROM python:3.9

WORKDIR /usr/src/lifemr-backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --upgrade pip

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]