FROM python:3.10.12

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
# intends from the current directory to the container start building
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Espone la porta su cui l'applicazione sarà disponibile
EXPOSE 5000


# Run app.py when the container launches
CMD ["python", "server.py"]




