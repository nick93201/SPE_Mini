FROM python:3.9-slim

# Copy calculator.py and the test file to the /app directory
WORKDIR /app
COPY cal.py .
COPY test.py .
CMD ["python3","cal.py"]
