Sure! Here's an overview of your project:

### Project Overview
This project involves creating a logging system that includes a client-server architecture for collecting, storing, and managing log data. The project is structured to ensure modularity, reusability, and maintainability.

### Key Components

1. **default_variables.py**:
   - Contains default configuration values and paths used across the project.
   - Provides a `get_default` function to retrieve default values.

2. **client.py**:
   - Implements a `LogClient` class that reads configuration, sends logs to a server, and handles retries and backups.
   - Uses the `SessionLogger` class for logging and the `get_default` function for default values.

3. **modules/**:
   - Contains utility modules and the server script.
   
   - **utils.py**:
     - Provides utility functions such as `read_config` and `save_to_database`.

   - **logger.py**:
     - Implements a `SessionLogger` class for managing logging sessions and saving logs.
     - Uses a `JsonFormatter` class to format log entries as JSON.
     - Integrates default log paths using the `get_default` function.

   - **flask_server.py**:
     - Implements a Flask server to receive and process log data.
     - Reads configuration and handles SSL encryption if enabled.
     - Uses the `get_default` function for default values.

   - **database.py**:
     - Implements a `DatabaseManager` class to manage SQLite database operations.
     - Initializes the database, saves logs, and fetches logs.

4. **Configuration and Certificates**:
   - **config.txt**: Configuration file used by the scripts.
   - **certificate_request.csr**: Certificate request file.
   - **certificate.pem**: Certificate file.
   - **private_key.pem**: Private key file.

5. **Backup and Logs**:
   - **backup_logs.json**: File to store backup logs.
   - **logs/**: Directory to store log files.

### How It Works

1. **Client Initialization**:
   - The `LogClient` class is initialized with configuration values, either provided or retrieved using `get_default`.
   - The client reads the configuration file and sets up logging and SSL context if encryption is enabled.

2. **Logging**:
   - The `SessionLogger` class manages logging sessions, formats log entries as JSON, and saves logs based on the specified method (file, stdout, custom).
   - Logs are saved to a file in the default logs path.

3. **Sending Logs**:
   - The client sends logs to the server using HTTP POST requests.
   - If sending fails, logs are backed up to a file and resent from the backup at regular intervals.

4. **Server**:
   - The Flask server receives log data and saves it to the database.
   - The server can handle SSL encryption if configured.

5. **Database Management**:
   - The `DatabaseManager` class initializes the database, saves log entries, and fetches logs.

### Example Usage

- **Client**:
  ```python
  config_file = get_default('DEFAULT_CONFIG_FILE')
  log_client = LogClient(config_file)
  log_client.send_logs_to_server()
  ```

- **Server**:
  ```python
  if __name__ == '__main__':
      config = read_config(get_default('DEFAULT_CONFIG_FILE'))
      port = int(config.get('server_config').get('port', get_default('DEFAULT_PORT')))
      use_encryption = config.get('server_config').get('certificate') and config.get('server_config').get('private_key')
      
      if use_encryption:
          ssl_context = (config['server_config']['certificate'], config['server_config']['private_key'])
          app.run(host='0.0.0.0', port=port, ssl_context=ssl_context)
      else:
          app.run(host='0.0.0.0', port=port)
  ```

This project provides a robust and flexible logging system that can be easily extended and customized. Let me know if you have any questions or need further details!