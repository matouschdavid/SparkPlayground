# Spark
## Usage
### Build the docker compose
Not necessary but nice for debugging.
```shell
docker-compose build
```

### Run batch processing
#### Windows
```shell
  $env:PROCESSING="batch"; docker-compose up
```
Exit with Crtl+C

#### MacOS
```shell
PROCESSING=batch docker-compose up
```
Exit with Control+C

### Run stream processing
#### Windows
```shell
  $env:PROCESSING="stream"; docker-compose up
```
Exit with Crtl+C

#### MacOS
```shell
PROCESSING=stream docker-compose up
```
Exit with Control+C

## What is it about?
In this demo project the openweather API is used in combination with apache spark.
Both batch and stream processing are used in an example program. The deployment is implemented as a docker-compose.

