FROM python:3.10.6-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app
EXPOSE 3000
CMD ["python", "app.py"]
