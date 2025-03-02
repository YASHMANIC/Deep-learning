import multiprocessing
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Binding
bind = "0.0.0.0:8080"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Process naming
proc_name = "deepbot"