FROM python:3.10.6-slim-buster
# Install necessary packages for OpenCV
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libgtk2.0-dev \
    pkg-config
WORKDIR /app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app
RUN rm -r /app/requirements.txt /app/*/__pycache__/ /app/ImageSteganographyServer/storage/__pycache__/
ENV PYTHONPATH=/app
RUN echo {} > /app/ImageSteganographyServer/storage/user_images.json
VOLUME ["/app/ImageSteganographyServer/storage/user_images.json"]
EXPOSE 3000
CMD ["python", "app.py"]