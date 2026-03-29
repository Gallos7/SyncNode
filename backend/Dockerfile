# -----------------------------------------------------------------------------
# STAGE: Base Image Configuration
# Using the official Python 3.11 image. The 'slim' variant strips out unnecessary 
# OS packages (like compilers) to keep the final image size minimal and secure.
# -----------------------------------------------------------------------------
FROM python:3.11-slim

# -----------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk.
# PYTHONUNBUFFERED: Ensures console output is piped directly to the terminal 
# without being buffered, allowing for real-time log monitoring.
# -----------------------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory within the container's filesystem.
WORKDIR /app

# -----------------------------------------------------------------------------
# LAYER OPTIMIZATION: Dependency Installation
# Docker caches layers to speed up builds. By copying ONLY the requirements file 
# first, Docker memorizes the installed packages. If source code changes later, 
# Docker skips the 'pip install' step and rebuilds almost instantly.
# -----------------------------------------------------------------------------
COPY requirements.txt .

# Install dependencies. The '--no-cache-dir' flag prevents pip from caching 
# the downloaded installation files (.whl), further reducing the final image size.
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# APPLICATION SOURCE CODE COPY
# Copy the entire backend source directory into the container.
# -----------------------------------------------------------------------------
COPY . .

# Inform Docker that the container intends to listen on port 8000 at runtime.
# Note: This is purely documentation. The actual port binding happens in docker-compose.
EXPOSE 8000

# -----------------------------------------------------------------------------
# CONTAINER EXECUTION COMMAND
# The exact command to spin up the FastAPI ASGI server using Uvicorn.
# Binding to 0.0.0.0 is required in Docker to allow external network access.
# -----------------------------------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]