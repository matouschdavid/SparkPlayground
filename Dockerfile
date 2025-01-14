# Use an official Python base image
FROM python:3.10-slim

# Set environment variables
ENV SPARK_VERSION=3.4.1
ENV HADOOP_VERSION=3
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk wget curl ca-certificates procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Find and set the correct JAVA_HOME dynamically
RUN update-alternatives --set java $(update-alternatives --list java | grep java-17) && \
    echo "JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))" >> /etc/environment

ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Download and install Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a working directory
WORKDIR /app

# Copy application files into the container
COPY app /app

# Set Spark environment variables for the runtime
ENV _JAVA_OPTIONS="-Djava.io.tmpdir=/tmp"
ENV PYSPARK_SUBMIT_ARGS="--driver-java-options='-Djava.io.tmpdir=/tmp' pyspark-shell"

# Default command
CMD ["python", "main.py"]
