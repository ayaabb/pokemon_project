FROM python:3.9

# Set the working directory inside the container
WORKDIR /code

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the configuration file
#COPY config.env /code/config.env

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["uvicorn", "server:server", "--host", "0.0.0.0", "--port", "8001", "--reload"]
