# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files into the container
COPY app.py wsgi.py superkart_sales_model.joblib .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
