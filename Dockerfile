FROM python:3.10-slim-buster

# Set work directory
WORKDIR /app

# Install system dependencies and upgrade SQLite
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    sqlite3 \
    libsqlite3-dev \
    wget \
    && wget https://www.sqlite.org/2024/sqlite-autoconf-3450000.tar.gz \
    && tar xvfz sqlite-autoconf-3450000.tar.gz \
    && cd sqlite-autoconf-3450000 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3450000* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set library path
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Copy only essential files first
COPY requirements.txt .
COPY setup.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clean up after install
RUN rm -rf /root/.cache

# Copy the rest of the application
COPY . .

# Run the app
CMD ["python", "app.py"]