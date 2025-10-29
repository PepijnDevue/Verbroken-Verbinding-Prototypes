FROM pytorch/pytorch:2.2.0-cuda11.8-cudnn8-runtime

# Keep layers small and simple
RUN apt-get update && apt-get install -y --no-install-recommends \
	git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy only requirements first to leverage docker cache
COPY requirements.txt /app/requirements.txt

# Install Python dependencies (use pip from the base image)
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project files
COPY . /app

# Environment defaults
ENV STREAMLIT_SERVER_HEADLESS=true \
	STREAMLIT_SERVER_ENABLECORS=false \
	PORT=8501 \
	NVIDIA_VISIBLE_DEVICES=all \
	PYTHONUNBUFFERED=1

EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]

