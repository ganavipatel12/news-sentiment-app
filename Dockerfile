# Use an official Python runtime
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --no-deps

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Start the Flask app using gunicorn
CMD gunicorn -w 4 -b 0.0.0.0:7860 api:app
