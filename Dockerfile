FROM python:3.9-slim-buster
# Install necessary packages for OpenGL support
RUN apt-get update && apt-get install -y \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri
WORKDIR /app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app
EXPOSE 3000
CMD ["python", "app.py"]
