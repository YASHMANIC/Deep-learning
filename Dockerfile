# Use smaller base image
FROM python:3.10-slim-buster

# Set work directory
WORKDIR /app

# Copy only essential files first
COPY requirements.txt .
COPY setup.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Clean up after install (if necessary)
RUN rm -rf /root/.cache

# Run the app
CMD ["python", "app.py"]
