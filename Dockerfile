# Start from a base image with Conda preinstalled
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a conda environment
RUN conda create -n myenv python=3.12

# Activate the environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Get the one pesky package I can't get with pip
RUN conda install -c intel mkl_fft

# use conda for some other packages where it could possibly help
RUN conda install numpy opencv

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the Uvicorn server for the FastAPI app
CMD ["conda", "run", "-n", "myenv", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
