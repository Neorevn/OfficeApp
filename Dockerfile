# --- Stage 1: Build the frontend ---
FROM node:20-alpine as frontend-builder

WORKDIR /app/Frontend

# Copy frontend package files and install dependencies
# This copies only the package files to leverage Docker's layer caching.
# The 'npm install' step will only be re-run if these files change.
COPY Frontend/package.json Frontend/package-lock.json* ./
RUN npm install

# Copy the rest of the frontend code and build it
COPY Frontend/ .
RUN npm run build

# --- Stage 2: Build the backend ---
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main entrypoint and the Backend package
COPY main.py .
COPY Backend ./Backend

# Copy the built frontend from the builder stage
COPY --from=frontend-builder /app/dist ./dist

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]