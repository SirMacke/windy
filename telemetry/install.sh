#!/bin/bash

# Default options
SYSTEM_WIDE=false
COMPONENT="all"  # all, collector, api

# Process command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --system)
            SYSTEM_WIDE=true
            shift
            ;;
        --user)
            SYSTEM_WIDE=false
            shift
            ;;
        --all)
            COMPONENT="all"
            shift
            ;;
        --collector)
            COMPONENT="collector"
            shift
            ;;
        --api)
            COMPONENT="api"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--system|--user] [--all|--collector|--api]"
            exit 1
            ;;
    esac
done

# Create the virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    
    echo "Installing dependencies..."
    .venv/bin/pip install -r requirements.txt
fi

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir -p data
fi

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    
    # Generate a random API key
    if command -v openssl &> /dev/null; then
        API_KEY=$(openssl rand -hex 16)
        sed -i "s/your_secret_api_key_here/$API_KEY/g" .env
    fi
fi

# Install service files
install_service() {
    local service_file=$1
    local service_name=$(basename $service_file)
    
    if $SYSTEM_WIDE; then
        echo "Installing $service_name system-wide..."
        sudo cp $service_file /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable $service_name
        sudo systemctl start $service_name
    else
        echo "Installing $service_name for current user..."
        mkdir -p ~/.config/systemd/user/
        cp $service_file ~/.config/systemd/user/
        systemctl --user daemon-reload
        systemctl --user enable $service_name
        systemctl --user start $service_name
    fi
}

# Install selected component(s)
case $COMPONENT in
    all)
        install_service systemd/windy-telemetry.service
        ;;
    collector)
        install_service systemd/windy-collector.service
        ;;
    api)
        install_service systemd/windy-api.service
        ;;
esac

echo "Installation complete!"
echo ""
if $SYSTEM_WIDE; then
    echo "To view service status: sudo systemctl status windy-telemetry.service"
    echo "To view logs: sudo journalctl -u windy-telemetry.service -f"
else
    echo "To view service status: systemctl --user status windy-telemetry.service"
    echo "To view logs: journalctl --user -u windy-telemetry.service -f"
fi
echo ""
echo "Your system is now collecting weather data!"