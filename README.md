# 42musaev


### Running the Application
To start the application, run the following command:

```shell
docker-compose up
```

### Applying Linters and Formatters
To apply all linters and formatters, run the following command:

```shell
pre-commit run --all-files
```

### Creating a New Service
To create a new service, use the following command:

```shell
make create-service service=<service_name>
```

### Adding .env file for service
to add environment variables add the file to /envs
```shell
touch env/<filename>
```
