# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for audio processing and builds
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy your project files into the container
COPY . .

# Install Cython first (required for some packages)
RUN pip install Cython

# ✅ Increase pip timeout to 5 minutes for reliability with large wheels
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Command to run your FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
