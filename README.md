# Containerized AI Lab

A containerized environment for experimenting with local LLMs and LangChain agents.

## Features

- Fully containerized setup that works on both macOS and Linux
- Integrated local LLM support via Ollama
- Modular tool library for extending agent capabilities
- Simple configuration for GPU acceleration when available
- Cross-platform compatibility with minimal setup requirements

## Prerequisites

- Docker and Docker Compose installed
- Minimum 12GB RAM for the default llama2 model (8GB+ for smaller models like phi or gemma)
- For GPU acceleration: NVIDIA GPU with appropriate drivers and CUDA support

### Memory Requirements

Different models have different memory requirements:
- llama2: ~8GB+ RAM
- mistral: ~7GB+ RAM
- phi: ~4GB+ RAM
- gemma: ~5GB+ RAM

If you have limited memory, you can specify a smaller model in the .env file or docker-compose.yml.

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd containerized-ai-lab
   ```

2. Create an environment file:
   ```bash
   cp .env.example .env
   ```

3. Make the management script executable:
   ```bash
   chmod +x manage.sh
   ```

4. Start the containers:
   ```bash
   ./manage.sh start
   ```

5. Download a model (optional, will download automatically on first use):
   ```bash
   ./manage.sh model llama2
   ```

The management script provides several useful commands:
- `./manage.sh start` - Start containers
- `./manage.sh start-gpu` - Start containers with GPU support (for Ubuntu/NVIDIA)
- `./manage.sh stop` - Stop containers
- `./manage.sh status` - Check container status
- `./manage.sh logs` - Show container logs
- `./manage.sh model [name]` - Download a specific model
- `./manage.sh restart` - Restart containers
- `./manage.sh shell` - Open a shell in the AI lab container

### MacOS Docker Memory Configuration

On MacOS, Docker Desktop runs in a VM with limited resources by default. To allocate more memory:

1. Open Docker Desktop
2. Click on the Settings/Preferences gear icon
3. Navigate to "Resources" tab
4. Adjust the Memory slider to at least 16GB
5. Click "Apply & Restart"

![Docker Desktop Memory Settings](https://docs.docker.com/desktop/images/mac-resources.png)

## Usage

Once the containers are running:

1. Web Interface: Open `http://localhost:8000` in your browser
2. API Documentation: Open `http://localhost:8000/docs` to view the API endpoints

### Available Endpoints

- `GET /`: Home page with links to different sections
- `POST /chat`: Send a message to the AI agent
- `GET /models`: List available models from Ollama

## Configuration

### Resource Limits

The Docker Compose file includes memory settings for both the AI application and Ollama:

```yaml
deploy:
  resources:
    reservations:
      memory: 4G
    limits:
      memory: 8G
```

Adjust these values based on your system's available resources and the size of the models you're using.

### GPU Acceleration

For high-performance machines with NVIDIA GPUs (like your Ubuntu machine with 24GB VRAM), we've included a special configuration:

```bash
./manage.sh start-gpu
```

This command uses the `docker-compose.gpu.yml` file which is preconfigured for:
- 16-24GB of system RAM allocation
- NVIDIA GPU access
- Higher memory limits for larger models

Prerequisites for GPU support:
1. NVIDIA GPU with appropriate drivers installed
2. NVIDIA Container Toolkit (nvidia-docker2) installed
3. Docker configured to use the NVIDIA runtime

On Ubuntu, install the NVIDIA Container Toolkit with:
```bash
# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install nvidia-docker2
sudo apt-get update
sudo apt-get install -y nvidia-docker2

# Restart Docker
sudo systemctl restart docker
```

### Changing Models

Change the model by modifying the `MODEL_NAME` environment variable in the `.env` file or in `docker-compose.yml`. Available models from Ollama include:

- llama2
- mistral
- phi
- gemma
- and more...

## Extending

### Adding New Tools

1. Create a new tool file in the `tools` directory
2. Inherit from the `BaseTool` class
3. Implement the `_run` method
4. Add the tool to the `__init__.py` file
5. Update the `get_tools` function in `app/main.py`

Example new tool:
```python
from typing import Any
from .base import BaseTool

class MyNewTool(BaseTool):
    name = "my_new_tool"
    description = "Description of what my tool does"
    
    def _run(self, input: str, **kwargs: Any) -> str:
        # Tool implementation
        return f"Result for: {input}"
```