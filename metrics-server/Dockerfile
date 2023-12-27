# Use an official Prometheus image as the base image
FROM prom/prometheus:v2.28.0

# Copy Prometheus configuration file
COPY prometheus-cfg.yaml /etc/prometheus/

# Expose Prometheus and Grafana ports
EXPOSE 9090
EXPOSE 3000

# Create a user named "prometheus" with a specific UID and GID
RUN groupadd -g 1000 prometheus && useradd -u 1000 -g prometheus -M -s /bin/false prometheus


# Set the user to run Prometheus (optional)
USER promethues

