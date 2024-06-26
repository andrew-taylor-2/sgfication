# Start from a base image with Conda preinstalled
FROM continuumio/miniconda3

# Install system dependencies for opencv
RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in environment.yml
RUN conda env create -f environment.yml

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the Uvicorn server for the FastAPI app
CMD ["conda", "run", "--no-capture-output", "-n", "sgfenv", "uvicorn", "sgfication.main:app", "--host", "0.0.0.0", "--port", "8000"]
