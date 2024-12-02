FROM python:3.11-slim

# Copy the current directory contents into the container at /app
RUN mkdir /app
COPY . /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the application listens on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.routes:app", "--host", "0.0.0.0", "--port", "8000"]