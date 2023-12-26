# K8's Kadence Flask App

## Overview

This repository contains a simple Flask application designed to demonstrate the basics of containerization using Docker and orchestration using Kubernetes. The application greets users with a personalized message, "Hello {username} welcome to K8’s Kadence!", where the `{username}` is dynamically set through an environment variable. The goal of this project is to provide a hands-on experience for students learning about Docker, Kubernetes, and the principles of deploying applications in a containerized environment.

## Features

- **Personalized Greeting:** The application uses an environment variable to personalize the greeting message.
- **Containerization:** The Flask app is containerized using Docker, allowing for easy deployment and scalability.
- **Kubernetes Ready:** The application is designed to be deployed on a Kubernetes cluster, demonstrating basic Kubernetes concepts.
- **Styling:** The application features a simple styling with white text on a light blue background.

## Getting Started

### Prerequisites

- Docker installed on your machine.
- Access to a Kubernetes cluster (for Kubernetes deployment).

### Running the Application with Docker

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/pvass24/k8s-kadence.git
    ```

2. **Build the Docker Image:**
    ```sh
    docker build -t myflaskapp .
    ```

3. **Run the Docker Container:**
    Replace `<username>` with your desired username.
    ```sh
    docker run -p 5000:5000 -e USERNAME=<username> myflaskapp
    ```

4. **Access the Application:**
    Open a web browser and navigate to `http://localhost:5000`.

### Deploying on Kubernetes

1. **Create a Docker Image and Push to a Registry:**
    Follow the instructions specific to your container registry.

2. **Update the Kubernetes Deployment YAML:**
    Modify the image path in the provided Kubernetes deployment YAML file to point to your Docker image.

3. **Apply the Deployment:**
    ```sh
    kubectl apply -f deployment.yaml
    ```

4. **Access the Application:**
    The access method may vary based on your Kubernetes setup.

## Contribution

Feel free to fork this repository and contribute by submitting a pull request. We appreciate your input in making this project more robust and versatile.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
