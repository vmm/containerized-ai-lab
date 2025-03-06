#!/bin/bash

# Script to help manage the Containerized AI Lab

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo -e "${GREEN}Containerized AI Lab Management Script${NC}"
    echo ""
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start all containers"
    echo "  start-gpu   - Start containers with GPU support (Ubuntu/NVIDIA)"
    echo "  start-amd   - Start containers with GPU support (Ubuntu/AMD)"
    echo "  stop        - Stop all containers"
    echo "  status      - Check container status"
    echo "  logs        - Show logs from containers"
    echo "  model [name]- Download a model (default: llama2)"
    echo "  restart     - Restart all containers"
    echo "  shell       - Open a shell in the AI lab container"
    echo "  ollama-shell- Open a shell in the Ollama container"
    echo "  chat [model]- Chat directly with an Ollama model (default: llama2)"
    echo "  help        - Show this help message"
    echo ""
}

# Function to start containers
start() {
    echo -e "${YELLOW}Starting containers...${NC}"
    docker compose up -d
    echo -e "${GREEN}Containers started successfully!${NC}"
    echo -e "Access the web interface at ${GREEN}http://localhost:8000${NC}"
}

# Function to start containers with NVIDIA GPU support
start_gpu() {
    echo -e "${YELLOW}Starting containers with NVIDIA GPU support...${NC}"
    docker compose -f docker-compose.gpu.yml up -d
    echo -e "${GREEN}NVIDIA GPU-enabled containers started successfully!${NC}"
    echo -e "Access the web interface at ${GREEN}http://localhost:8000${NC}"
}

# Function to start containers with AMD GPU support
start_amd() {
    echo -e "${YELLOW}Starting containers with AMD GPU support...${NC}"
    docker compose -f docker-compose.amd.yml up -d
    echo -e "${GREEN}AMD GPU-enabled containers started successfully!${NC}"
    echo -e "Access the web interface at ${GREEN}http://localhost:8000${NC}"
}

# Function to stop containers
stop() {
    echo -e "${YELLOW}Stopping containers...${NC}"
    docker compose down
    echo -e "${GREEN}Containers stopped successfully!${NC}"
}

# Function to check container status
status() {
    echo -e "${YELLOW}Container status:${NC}"
    docker compose ps
}

# Function to show logs
logs() {
    echo -e "${YELLOW}Container logs:${NC}"
    docker compose logs -f
}

# Function to download a model
download_model() {
    model_name=${1:-llama2}
    echo -e "${YELLOW}Downloading model: ${model_name}${NC}"
    docker compose exec ai-lab python models/download.py $model_name
}

# Function to restart containers
restart() {
    echo -e "${YELLOW}Restarting containers...${NC}"
    
    # Stop and remove containers
    docker compose down
    
    # Start containers again
    docker compose up -d
    
    echo -e "${GREEN}Containers restarted successfully!${NC}"
    echo -e "Access the web interface at ${GREEN}http://localhost:8000${NC}"
}

# Function to open a shell in the AI lab container
shell() {
    echo -e "${YELLOW}Opening shell in AI lab container...${NC}"
    docker compose exec ai-lab /bin/bash
}

# Function to open a shell in the Ollama container
ollama_shell() {
    echo -e "${YELLOW}Opening shell in Ollama container...${NC}"
    docker compose exec ollama /bin/bash
}

# Function to chat directly with an Ollama model
chat() {
    model_name=${1:-llama2}
    echo -e "${YELLOW}Starting chat with model: ${model_name}${NC}"
    docker compose exec ollama ollama run $model_name
}

# Main script logic
case "$1" in
    start)
        start
        ;;
    start-gpu)
        start_gpu
        ;;
    start-amd)
        start_amd
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    model)
        download_model "$2"
        ;;
    restart)
        restart
        ;;
    shell)
        shell
        ;;
    ollama-shell)
        ollama_shell
        ;;
    chat)
        chat "$2"
        ;;
    help|*)
        show_help
        ;;
esac

exit 0