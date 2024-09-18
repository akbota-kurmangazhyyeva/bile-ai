FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6

# Clone EDGE repository
RUN git clone https://github.com/Stanford-TML/EDGE.git /app/EDGE

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip install git+https://github.com/rodrigo-castellon/jukemirlib.git
RUN pip install 'git+https://github.com/facebookresearch/pytorch3d.git'

# Copy the application code
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]