# Use an official Prometheus image as the base image
FROM prom/prometheus:v2.28.0

# Copy Prometheus configuration file
COPY prometheus.yaml /etc/prometheus/

# Expose Prometheus and Grafana ports
EXPOSE 9090
EXPOSE 3000

# Set the user to run Prometheus (optional)
USER promethues
