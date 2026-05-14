# Python runtime
FROM python:3.14-slim

# Working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy applicaiton code
COPY . /app

# Expose port for GUI
EXPOSE 8501

CMD ["streamlit", "run", "GUI.py", "--server.port=8501", "--server.address=0.0.0.0"]
