# Start from a base image with Conda preinstalled
FROM continuumio/miniconda3

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
CMD ["conda", "run", "-n", "myenv", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
