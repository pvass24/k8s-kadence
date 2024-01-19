# K8's Kadence Flask App

## Overview

This repository contains a simple Flask application designed to demonstrate the basics of containerization using Docker and orchestration using Kubernetes. The application greets users with a personalized message, "Hello {username} welcome to K8’s Kadence!", where the `{username}`, `{bg-color}`, & `{font-color}` is dynamically set through an environment variable. The goal of this project is to provide a hands-on experience for students learning about Docker, Kubernetes, and the principles of deploying applications in a containerized environment. The key difference with V3 vs V2 is we have added a way to gather metrics. We will be counting page visits as well as the duration of the requests. 
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
    cd k8s-kadence/flask-app-v3/
    ```

2. **Build the Docker Image:**
    ```sh
    docker build -t myflaskapp:v3
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

5. **Stop the Container:**
    Enter `Control + C` to stop the container.

### Adding the Image to Docker Hub

1. **Log in to Docker Hub from Your Command Line:**
    ```sh
    docker login
    ```

2. **Tag Your Docker Image:**
    Replace `yourdockerhubusername` with your Docker Hub username and `tagname` with your desired tag.
    ```sh
    docker tag myflaskapp:v3 <yourdockerhubusername>/myflaskapp:v3
    ```

3. **Push the Image to Docker Hub:**
    ```sh
    docker push yourdockerhubusername/myflaskapp:v3
    ```

4. **Verify the Image on Docker Hub:**
    Check your Docker Hub account to see if the image is uploaded.

### Deploying on Kubernetes

1. **Create or Update the Kubernetes Deployment YAML:**
   Edit the `deployment.yaml` file to point to the image on your Docker Hub account (`yourdockerhubusername/myflaskapp:v3`).

2. **Apply the Deployment:**
   Apply the deployment to your Kubernetes cluster using the command:
   ```sh
   kubectl apply -f deployment.yaml

## Important Note
   You can skip the next step if you have already created the service from the V1 section.

3. **View and Create the Service:**
   Since were using KinD, to access the deployment we need to create a service. I have created the service yaml file for you. Check it out. Its called myflaskapp-svc.yaml
   ```sh
   cat myflaskapp-svc.yaml
   ```
   You can see the service is exposing the flask app with a blank nodePort figure. When the nodePort is empty, there will be a random nodePort provided upon creation of the service. You can check out the assigned port number by running `k get svc myflaskapp-svc`. Also the pods in the deployment are "selected" by the service due to the matching labels "app: myflaskapp". I always recommend to run `kubectl get svc,ep` so we can see both the services and the endpoints(pods) connected to the services. 
   
   Lets create the service.
   ```sh
   kubectl create -f myflaskapp-svc.yaml
   ```
  
   We also can port-forward to access the app locally however lets use an ingress instead.
   Ingress is used to expose HTTP and HTTPS routes from outside the cluster to services within the cluster. It allows you to define rules for inbound connections and route them to different services based on the request's host or URL path. This is particularly useful for managing access to multiple services through a single external endpoint. Lets examine the `ingress.yaml` file.
   ```sh
   cat ingress.yaml
   ```
   apiVersion: networking.k8s.io/v1: This specifies the API version of the resource. In this case, it's using version 1 of the networking API group.

   kind: Ingress: This indicates that the resource type you are defining is an Ingress. An Ingress is used for managing external access to services in a Kubernetes cluster, typically HTTP.

   metadata: This section contains metadata about the Ingress resource:

   name: my-first-ingress: The name of the Ingress resource is set to "my-first-ingress".
   annotations:
   nginx.ingress.kubernetes.io/rewrite-target: /: This is an annotation specific to Nginx Ingress Controller. It modifies the path of the request before forwarding it to the backend service. Here, it rewrites the path to /.
   spec: This section specifies the desired state of the Ingress:

   ingressClassName: nginx: Specifies the Ingress Class to be used. In this case, it’s pointing to an Ingress Class named “nginx”, which indicates that an Nginx Ingress Controller should manage this Ingress.
rules: This defines the rules through which the incoming traffic is routed:

   http:
   paths:
   - path: /: This specifies the URL path to match for incoming requests. Here, it matches the root path (/).
   pathType: Prefix: This indicates how the path should be matched and routed. Prefix means that any path that starts with the specified path (/) will match.
     backend: Defines where the traffic should be routed once a rule is matched:
   service:
   name: myflaskapp-svc: The name of the Service to which traffic should be sent. In this case, traffic is routed to a Service named "myflaskapp-svc".
   port:
   number: 5000: The port number of the Service on which it is listening. Here, it indicates that traffic should be sent to port 5000 of "myflaskapp-svc".

4. **Now lets create the ingress
    ```sh
    k create -f ingress.yaml
    ```
   To access the app simply enter localhost in your browser and it should redirect you straight to the app like before. Because we have added the annotation `nginx.ingress.kubernetes.io/rewrite-target: /` this will redirect the request to the backend service `myflaskapp-svc` which is listening on port 5000.
   
4. **View the metrics:**

   Enter http://localhost/metrics to view your apps metrics.
   You should try reloading the http://localhost page a few times to simulate users connecting to your application and the `myflaskapp_requests_total` counter should increase with every visit.

Congrats!!!! You have created a flask app that started in your local machine and now you have created a cluster to host your application and exposed it via an ingress!


