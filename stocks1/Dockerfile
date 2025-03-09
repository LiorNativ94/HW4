# Step 1: Use an official Python runtime as the base image
FROM python:alpine

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file to the working directory
COPY requirements.txt /app/

# Step 4: Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire application to the container
COPY . .

# Step 6: Set the environment variable for Flask to run in production mode (optional)
ENV FLASK_RUN_PORT=8000
ENV FLASK_APP=main.py

# Step 7: Expose the port Flask is running on (default is 5001)
EXPOSE 8000

# Step 8: Specify the command to run the application
CMD ["flask","run","--host=0.0.0.0", "--port=8000"]

