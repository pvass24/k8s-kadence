# Use an official Prometheus image as the base image
FROM prom/prometheus:v2.28.0

# Copy Prometheus configuration file
COPY prometheus-cfg.yaml /etc/prometheus/

# Expose Prometheus and Grafana ports
EXPOSE 9090
EXPOSE 3000

# Switch to root temporarily to create the user
USER root

# Create a user named "prometheus" with a specific UID
RUN adduser --uid 1000 --disabled-password prometheus

# Change ownership of the Prometheus data directory to the non-root user
RUN chown -R prometheus:prometheus /prometheus

# Set the user to run Prometheus (optional)
USER prometheus

# Start Prometheus
CMD [ "prometheus" ]
