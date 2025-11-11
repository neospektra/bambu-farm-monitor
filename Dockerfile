FROM debian:12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    gcc \
    g++ \
    libcurl4-openssl-dev \
    libcjson-dev \
    nginx \
    supervisor \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and extract Bambu Studio plugins from local build assets
COPY build_assets/linux_01.04.00.15.zip /tmp/linux_01.04.00.15.zip
RUN unzip -q /tmp/linux_01.04.00.15.zip -d /app && rm /tmp/linux_01.04.00.15.zip

# Copy go2rtc binary from local build assets
COPY build_assets/go2rtc_linux_amd64 /usr/local/bin/go2rtc
RUN chmod +x /usr/local/bin/go2rtc

# Copy BambuSource2Raw source files from local build assets
COPY build_assets/bambusource2raw.cpp build_assets/BambuTunnel.h build_assets/cJSON.c build_assets/cJSON.h /tmp/bambu_src/
RUN cd /tmp/bambu_src && \
    gcc bambusource2raw.cpp cJSON.c -lcurl -o /app/BambuP1SCam && \
    chmod +x /app/BambuP1SCam && \
    rm -rf /tmp/bambu_src

# Install Python dependencies for API
COPY api/requirements.txt /app/api/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /app/api/requirements.txt

# Copy configuration files
COPY go2rtc.yaml /app/go2rtc.yaml
COPY www/ /var/www/html/
COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh /app/entrypoint.sh
COPY api/ /app/api/

RUN chmod +x /app/entrypoint.sh && \
    chmod +x /app/api/*.py

# Expose ports
# 8080: Web UI
# 1984: go2rtc API and WebRTC
# 5000: Configuration API
# 5001: Status API
EXPOSE 8080 1984 5000 5001

# Use supervisor to manage multiple processes
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
