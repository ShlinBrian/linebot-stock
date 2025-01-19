FROM python:3.8.12-slim

# Set working directory
WORKDIR /api/

# Copy requirements and install dependencies
COPY requirements.txt /api/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY ./api /api/

# Run the application
CMD ["uvicorn", "--port", "8001", "--host", "0.0.0.0", "--log-level", "error", "app:APP"]
