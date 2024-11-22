# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /tfg-AI_translator

# Copy the current directory contents into the container at /app
COPY . /tfg-AI_translator


# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "main.py"]
