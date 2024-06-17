FROM python:3.9

# Set the working directory in the container
WORKDIR /images

# Copy requirements.txt to the container
COPY requirements.txt /images/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the entire pokemon directory to the container
COPY . /images

# Command to run the application
CMD ["uvicorn", "server:server", "--host", "0.0.0.0", "--port", "8002", "--reload"]
