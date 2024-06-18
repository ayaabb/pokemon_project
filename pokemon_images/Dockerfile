FROM python:3.9

WORKDIR /images_server

COPY requirements.txt /images_server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /images_server
# Command to run the application
CMD ["uvicorn", "server:server", "--host", "0.0.0.0", "--port", "8002", "--reload"]
