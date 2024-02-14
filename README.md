# HTTP-Socket Server with Docker

This Python script sets up an HTTP server and a socket server to handle GET and POST requests. It also demonstrates the use of Docker to containerize the application.

## Usage

1. Make sure you have Docker installed on your system.

2. Clone the repository:

    ```bash
    git clone https://github.com/Nikita-devel/http-socket-server.git
    ```

3. Navigate to the project directory:

    ```bash
    cd http-socket-server
    ```

4. Build the Docker image:

    ```bash
    docker build -t http-socket-server .
    ```

5. Run the Docker container:

    ```bash
    docker run -p 3000:3000 -p 5000:5000 http-socket-server
    ```

6. Access the server:

    Open a web browser and go to [http://localhost:3000](http://localhost:3000)

## Components

### `server.py`

This script contains the HTTP server and socket server components. It includes:

- `HttpHandler`: Handles HTTP GET and POST requests.
- `do_GET`: Handles GET requests and serves static files.
- `send_file`: Sends the requested file to the client.
- `do_POST`: Handles POST requests and sends data to the socket server.
- `save_data`: Saves POST data to a JSON file.
- `send_data_to_socket`: Sends data to the socket server.
- `run_socket_server`: Runs the socket server to receive data from the HTTP server.
- `run_http_server`: Runs the HTTP server.

## Dockerfile

The `Dockerfile` contains instructions to build a Docker image for the HTTP-Socket Server.

## Example

```bash
docker build -t http-socket-server .
docker run -p 3000:3000 -p 5000:5000 http-socket-server

 
