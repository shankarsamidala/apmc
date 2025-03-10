# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Start Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myapp.wsgi:application"]
