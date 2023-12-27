# K8's Kadence Flask App

## Overview

This repository contains a simple Flask application designed to demonstrate the basics of containerization using Docker and orchestration using Kubernetes. The application greets users with a personalized message, "Hello {username} welcome to K8’s Kadence!", where the `{username}`, `{bg-color}`, & `{font-color}` is dynamically set through an environment variable. The goal of this project is to provide a hands-on experience for students learning about Docker, Kubernetes, and the principles of deploying applications in a containerized environment.

## Features

- **Personalized Greeting:** The application uses an environment variable to personalize the greeting message.
- **Containerization:** The Flask app is containerized using Docker, allowing for easy deployment and scalability.
- **Kubernetes Ready:** The application is designed to be deployed on a Kubernetes cluster, demonstrating basic Kubernetes concepts.
- **Styling:** The application features a simple styling with white text on a light blue background.

## Getting Started

### Prerequisites

- Docker installed on your machine.
- Access to a Docker Hub account.
- Access to a Kubernetes cluster (for Kubernetes deployment).

### Local Development and Testing

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/pvass24/k8s-kadence.git
    ```

2. **Build the Docker Image:**
    ```sh
    docker build -t <yourdockerhubusername>/myflaskapp:v2 .
    ```

3. **Run the Docker Container:**
    Replace `<username>` with your desired username.
    Replace `<bg-color>` with your desired background color.
    Replace `<font-color>` with your desired font color.
    ```sh
    docker run -p 5000:5000 -e USERNAME=<username> -e BG_COLOR=<bg-color> -e FONT_COLOR=<font-color> myflaskapp 
    ```

4. **Access the Application:**
    Open a web browser and navigate to `http://localhost:5000`.

### Adding the Image to Docker Hub

1. **Log in to Docker Hub from Your Command Line:**
    ```sh
    docker login
    ```

2. **Tag Your Docker Image:**
    Replace `yourdockerhubusername` with your Docker Hub username and `tagname` with your desired tag.
    ```sh
    docker tag myflaskapp <yourdockerhubusername>/myflaskapp:v2
    ```

3. **Push the Image to Docker Hub:**
    ```sh
    docker push yourdockerhubusername/myflaskapp:v2
    ```

4. **Verify the Image on Docker Hub:**
    Check your Docker Hub account to see if the image is uploaded.

### Deploying on Kubernetes

1. **Create or Update the Kubernetes Deployment YAML:**
   Edit the `deployment.yaml` file to point to the image on your Docker Hub account (`yourdockerhubusername/myflaskapp:v2`).

2. **Apply the Deployment:**
   Apply the deployment to your Kubernetes cluster using the command:
   ```sh
   kubectl apply -f deployment.yaml
