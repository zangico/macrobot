# DEVELOPMENTMENT README

This README provides instructions for setting up the development environment for the project. Follow the steps below to get started.

## Prerequisites
- Poetry installed on your system. You can install it with the following command:
  ```bash
   curl -sSL https://install.python-poetry.org | python3 -
  ```
  If you want to create .venv inside the project directory, run:
  ```bash
  poetry config virtualenvs.in-project true
  ```
- Python 3.12 installed on your system. You can download, compile, and install it with:
  ```bash
  sudo apt update
  sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
  wget https://www.python.org/ftp/python/3.12.12/Python-3.12.12.tgz
  tar -xf Python-3.12.12.tgz
  cd Python-3.12.12
  ./configure --enable-optimizations
  make -j $(nproc)
  sudo make altinstall
  ```

## Development Setup
1. Clone the repository
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Copy and edit the .env.dist file to create a .env file with your configuration.
5. Run the development server:
   ```bash
   ./main.sh
   ```

## Deployment
To deploy the application using Docker, follow these steps:
1. Create requirements.txt file:
   ```bash
   poetry export -f requirements.txt --output requirements.txt --without-hashes
   ```
2. Copy and edit the .env.dist file to create a .env file with your configuration.
3. Build the Docker image:
   ```bash
   docker compose build
    ```
4. Run the Docker container:
    ```bash
    docker compose up -d
    ```
