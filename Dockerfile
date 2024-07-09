FROM python:3.9

# Updates
RUN apt-get -q -y update 
RUN apt-get install -y gcc

#Env variables
ENV WORKING_DIR=/app

# Set the working directory
WORKDIR ${WORKING_DIR}

# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Copy the rest of the application code
COPY . .

# Install the dependencies
RUN pip install -r requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
