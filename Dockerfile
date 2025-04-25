# Use Python 3.10 as the base image
FROM python:3.10-slim

# Install curl (needed to install uv package manager)
RUN apt-get update && apt-get install -y curl \
    && curl -Ls https://astral.sh/uv/install.sh | bash \
    && rm -rf /var/lib/apt/lists/*


# Add uv to the system PATH (default install location)
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory inside the container
WORKDIR /etl

# Copy the dependency file to the working directory
COPY pyproject.toml /etl/

# Install dependencies using uv (from pyproject.toml)
RUN uv pip install -r pyproject.toml --system

# Copy the rest of the project files to the container
COPY . /etl

