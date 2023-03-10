FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app
EXPOSE 3000
CMD ["python", "app.py"]
