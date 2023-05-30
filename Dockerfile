FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add metadata to the image
LABEL maintainer="aitorman@outlook.com"
LABEL version="1.0"
LABEL description="Buscar contenido en Twitter y almacenarlo en una archivo excel con opción a cla"

# Install Git and build-essential (which includes gcc)
RUN apt-get update && \
    apt-get install -y git python3-dev build-essential

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
