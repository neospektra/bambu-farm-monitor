#!/bin/bash
# Bambu Farm Monitor - macOS Automated Installation Script
# This script will install Docker Desktop (if needed) and set up Bambu Farm Monitor

set -e

# Color output functions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${MAGENTA}================================================================${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}================================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Check if running on macOS
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS only"
        exit 1
    fi
}

# Check if Homebrew is installed
check_homebrew() {
    if command -v brew &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Install Homebrew
install_homebrew() {
    print_header "Installing Homebrew"
    print_info "Homebrew is the package manager for macOS"
    echo ""

    if check_homebrew; then
        print_success "Homebrew is already installed"
        return 0
    fi

    print_info "Installing Homebrew..."
    print_warning "This may take several minutes and will prompt for your password"
    echo ""

    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Check if on Apple Silicon and add to PATH
    if [[ $(uname -m) == 'arm64' ]]; then
        if [[ -f /opt/homebrew/bin/brew ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
    fi

    if check_homebrew; then
        print_success "Homebrew installed successfully!"
        return 0
    else
        print_error "Failed to install Homebrew"
        return 1
    fi
}

# Check if Docker is installed and running
check_docker() {
    if command -v docker &> /dev/null; then
        if docker ps &> /dev/null; then
            return 0
        fi
    fi
    return 1
}

# Check if Podman is installed and running
check_podman() {
    if command -v podman &> /dev/null; then
        if podman ps &> /dev/null; then
            return 0
        fi
    fi
    return 1
}

# Install Docker Desktop
install_docker_desktop() {
    print_header "Installing Docker Desktop"

    if ! check_homebrew; then
        print_error "Homebrew is required but not installed"
        return 1
    fi

    print_info "Installing Docker Desktop via Homebrew..."
    print_warning "This may take several minutes..."
    echo ""

    # Install Docker Desktop
    if brew install --cask docker; then
        print_success "Docker Desktop installed successfully!"
        echo ""
        print_warning "Docker Desktop has been installed but needs to be started"
        print_info "Opening Docker Desktop..."

        # Open Docker Desktop
        open -a Docker

        echo ""
        print_info "Please wait for Docker Desktop to start (this may take 1-2 minutes)"
        print_info "You'll see a whale icon in your menu bar when it's ready"
        echo ""

        # Wait for user confirmation
        read -p "Press Enter when Docker Desktop is running..."

        # Wait for Docker to be ready
        print_info "Waiting for Docker to be ready..."
        local max_attempts=30
        local attempt=0

        while [ $attempt -lt $max_attempts ]; do
            if docker ps &> /dev/null; then
                print_success "Docker Desktop is ready!"
                return 0
            fi
            sleep 2
            attempt=$((attempt + 1))
        done

        print_error "Docker Desktop is not responding. Please ensure it's running and try again."
        return 1
    else
        print_error "Failed to install Docker Desktop"
        print_info "You can install manually from: https://www.docker.com/products/docker-desktop/"
        return 1
    fi
}

# Install Podman Desktop
install_podman_desktop() {
    print_header "Installing Podman Desktop"

    if ! check_homebrew; then
        print_error "Homebrew is required but not installed"
        return 1
    fi

    print_info "Installing Podman Desktop via Homebrew..."
    print_warning "This may take several minutes..."
    echo ""

    # Install Podman Desktop
    if brew install --cask podman-desktop; then
        print_success "Podman Desktop installed successfully!"
        echo ""
        print_warning "Podman Desktop has been installed but needs to be started"
        print_info "Please open Podman Desktop from Applications"
        print_info "Click 'Initialize and start' if prompted"
        echo ""

        read -p "Press Enter when Podman Desktop is running..."

        # Wait for Podman to be ready
        print_info "Waiting for Podman to be ready..."
        local max_attempts=30
        local attempt=0

        while [ $attempt -lt $max_attempts ]; do
            if podman ps &> /dev/null; then
                print_success "Podman Desktop is ready!"
                return 0
            fi
            sleep 2
            attempt=$((attempt + 1))
        done

        print_error "Podman Desktop is not responding. Please ensure it's running and try again."
        return 1
    else
        print_error "Failed to install Podman Desktop"
        print_info "You can install manually from: https://podman-desktop.io/downloads/macos"
        return 1
    fi
}

# Get printer information from user
get_printer_info() {
    local printer_num=$1

    echo ""
    echo -e "${CYAN}═══ Printer $printer_num Configuration ═══${NC}"

    read -p "Printer IP Address (e.g., 192.168.1.100): " ip
    if [[ -z "$ip" ]]; then
        return 1
    fi

    read -p "8-digit Access Code (from MQTT settings): " code
    if [[ -z "$code" ]] || [[ ${#code} -ne 8 ]]; then
        print_warning "Access code must be exactly 8 digits"
        return 1
    fi

    read -p "Printer Name (optional, press Enter to skip): " name
    read -p "Serial Number (optional, press Enter to skip): " serial

    echo "$printer_num|$ip|$code|$name|$serial"
    return 0
}

# Create docker-compose.yml
create_docker_compose() {
    local install_dir="$1"
    shift
    local printers=("$@")

    cat > "$install_dir/docker-compose.yml" <<EOF
version: '3.8'
services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"   # Web UI
      - "1984:1984"   # go2rtc WebRTC
      - "5000:5000"   # Config API
      - "5001:5001"   # Status API
EOF

    if [[ ${#printers[@]} -gt 0 ]]; then
        echo "    environment:" >> "$install_dir/docker-compose.yml"

        for printer_data in "${printers[@]}"; do
            IFS='|' read -r num ip code name serial <<< "$printer_data"

            echo "      - PRINTER${num}_IP=$ip" >> "$install_dir/docker-compose.yml"
            echo "      - PRINTER${num}_CODE=$code" >> "$install_dir/docker-compose.yml"

            if [[ -n "$name" ]]; then
                echo "      - PRINTER${num}_NAME=$name" >> "$install_dir/docker-compose.yml"
            fi

            if [[ -n "$serial" ]]; then
                echo "      - PRINTER${num}_SERIAL=$serial" >> "$install_dir/docker-compose.yml"
            fi
        done
    fi

    cat >> "$install_dir/docker-compose.yml" <<EOF

    volumes:
      - bambu-config:/app/config
    restart: unless-stopped

volumes:
  bambu-config:
EOF

    print_success "Created docker-compose.yml"
}

# Main installation process
main() {
    print_header "Bambu Farm Monitor - macOS Installation"
    echo -e "${CYAN}Version 3.3.9${NC}"
    echo ""
    print_info "This script will help you install and configure Bambu Farm Monitor"
    echo ""

    # Check if running on macOS
    check_macos

    # Variables
    local use_docker=false
    local use_podman=false
    local container_cmd=""

    print_header "Checking System Requirements"

    # Check for existing Docker installation
    if check_docker; then
        print_success "Docker is installed and running"
        use_docker=true
        container_cmd="docker"
    # Check for existing Podman installation
    elif check_podman; then
        print_success "Podman is installed and running"
        use_podman=true
        container_cmd="podman"
    # Neither installed - need to install one
    else
        print_warning "Neither Docker nor Podman is installed"
        echo ""
        echo -e "${YELLOW}Choose your container runtime:${NC}"
        echo "1. Docker Desktop (recommended, free for personal use)"
        echo "2. Podman Desktop (free alternative)"
        echo ""

        read -p "Enter your choice (1 or 2): " choice

        case $choice in
            1)
                # Ensure Homebrew is installed
                if ! check_homebrew; then
                    if ! install_homebrew; then
                        print_error "Failed to install Homebrew. Exiting."
                        exit 1
                    fi
                fi

                # Install Docker Desktop
                if install_docker_desktop; then
                    if check_docker; then
                        print_success "Docker Desktop is ready!"
                        use_docker=true
                        container_cmd="docker"
                    else
                        print_error "Docker Desktop is not running. Please start it and run this script again."
                        exit 1
                    fi
                else
                    print_error "Failed to install Docker Desktop"
                    exit 1
                fi
                ;;
            2)
                # Ensure Homebrew is installed
                if ! check_homebrew; then
                    if ! install_homebrew; then
                        print_error "Failed to install Homebrew. Exiting."
                        exit 1
                    fi
                fi

                # Install Podman Desktop
                if install_podman_desktop; then
                    if check_podman; then
                        print_success "Podman Desktop is ready!"
                        use_podman=true
                        container_cmd="podman"
                    else
                        print_error "Podman Desktop is not running. Please start it and run this script again."
                        exit 1
                    fi
                else
                    print_error "Failed to install Podman Desktop"
                    exit 1
                fi
                ;;
            *)
                print_error "Invalid choice"
                exit 1
                ;;
        esac
    fi

    # Pull the latest image
    print_header "Downloading Bambu Farm Monitor"
    print_info "Pulling latest image from Docker Hub..."

    if $container_cmd pull neospektra/bambu-farm-monitor:latest; then
        print_success "Image downloaded successfully"
    else
        print_error "Failed to pull image"
        exit 1
    fi

    # Configure printers
    print_header "Printer Configuration"
    print_info "You can configure up to 4 printers now (or add them later via web UI)"
    echo ""

    read -p "Configure printers now? (y/n): " configure_printers
    printers=()

    if [[ "$configure_printers" =~ ^[Yy]$ ]]; then
        for i in {1..4}; do
            echo ""
            read -p "Add Printer $i? (y/n): " add_printer

            if [[ "$add_printer" =~ ^[Yy]$ ]]; then
                if printer_data=$(get_printer_info $i); then
                    printers+=("$printer_data")
                    print_success "Printer $i configured"
                else
                    print_warning "Printer $i skipped"
                fi
            else
                break
            fi
        done
    fi

    # Choose deployment method
    print_header "Deployment Configuration"
    echo ""
    echo -e "${YELLOW}Choose deployment method:${NC}"
    echo "1. Docker Compose (recommended - easier to manage)"
    echo "2. Docker Run (simple - single command)"
    echo ""

    read -p "Enter your choice (1 or 2): " deploy_choice

    case $deploy_choice in
        1)
            # Docker Compose method
            install_dir="$HOME/bambu-farm-monitor"

            # Create directory
            if [[ ! -d "$install_dir" ]]; then
                mkdir -p "$install_dir"
                print_success "Created directory: $install_dir"
            fi

            # Create docker-compose.yml
            create_docker_compose "$install_dir" "${printers[@]}"

            # Start container
            print_header "Starting Bambu Farm Monitor"
            print_info "Starting container..."

            cd "$install_dir"
            if $container_cmd compose up -d; then
                print_success "Container started successfully!"
            else
                print_error "Failed to start container"
                exit 1
            fi
            ;;
        2)
            # Docker Run method
            print_header "Starting Bambu Farm Monitor"
            print_info "Starting container..."

            run_cmd="$container_cmd run -d --name bambu-farm-monitor -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001"

            # Add environment variables for printers
            for printer_data in "${printers[@]}"; do
                IFS='|' read -r num ip code name serial <<< "$printer_data"

                run_cmd+=" -e PRINTER${num}_IP=$ip"
                run_cmd+=" -e PRINTER${num}_CODE=$code"

                if [[ -n "$name" ]]; then
                    run_cmd+=" -e PRINTER${num}_NAME='$name'"
                fi

                if [[ -n "$serial" ]]; then
                    run_cmd+=" -e PRINTER${num}_SERIAL=$serial"
                fi
            done

            run_cmd+=" -v bambu-config:/app/config neospektra/bambu-farm-monitor:latest"

            if eval $run_cmd; then
                print_success "Container started successfully!"
            else
                print_error "Failed to start container"
                exit 1
            fi
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac

    # Wait for container to be ready
    print_info "Waiting for services to initialize..."
    sleep 5

    # Check if container is running
    if $container_cmd ps | grep -q bambu-farm-monitor; then
        print_success "Bambu Farm Monitor is running!"
    else
        print_warning "Container may not be running properly"
        print_info "Check logs with: $container_cmd logs bambu-farm-monitor"
    fi

    # Show completion message
    print_header "Installation Complete!"
    echo ""
    print_success "Bambu Farm Monitor is now running!"
    echo ""
    echo -e "${GREEN}Access your dashboard at:${NC}"
    echo -e "${CYAN}  http://localhost:8080${NC}"
    echo ""

    if [[ ${#printers[@]} -eq 0 ]]; then
        print_info "Since you didn't configure printers, you'll need to add them via the web UI"
        print_info "Click 'Add Printer' button and follow the setup wizard"
    fi

    echo ""
    echo -e "${YELLOW}Useful commands:${NC}"
    echo "  View logs:       $container_cmd logs bambu-farm-monitor"
    echo "  Stop container:  $container_cmd stop bambu-farm-monitor"
    echo "  Start container: $container_cmd start bambu-farm-monitor"
    echo "  Restart:         $container_cmd restart bambu-farm-monitor"
    echo ""
    print_info "For more information, visit: https://github.com/neospektra/bambu-farm-monitor"
    echo ""

    # Open browser
    read -p "Open dashboard in browser now? (y/n): " open_browser
    if [[ "$open_browser" =~ ^[Yy]$ ]]; then
        open "http://localhost:8080"
    fi

    echo ""
    echo "Press Enter to exit..."
    read
}

# Run the installation
main "$@"
