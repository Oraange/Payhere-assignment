#./Dockerfile
FROM python:3.9

# Working Directory
WORKDIR /usr/src/app

# Copy Packages
COPY requirements.txt ./

# Install Packages
RUN pip install -r requirements.txt

COPY . .

# Run the application on the port 8000
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "payhere.wsgi:application"]
