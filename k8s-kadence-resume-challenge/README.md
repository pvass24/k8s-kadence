# K8's Kadence Resume Challenge

##Intro

This is a remix to the Cloud Resume Challenge.
A key prerequisite is that you must have a Cloud Provider to participate in the official challenge. So I took it upon my self to make this challenge more available to all who may not have the funds to do this on AWS or any Cloud Provider. Obviuosly, we wont have the ability to expose our service through a Loadbalancer thats handled by a cloud Provider, but If you have access to your home network modem, we can still expose our local application over the internet.

**Setting the Stage**

Imagine you are going to deploy an e-commerce website. It’s crucial to consider the challenges of modern web application deployment and how containerization and Kubernetes (K8s) offer compelling solutions:

Scalability: How can your application automatically adjust to fluctuating traffic?
Consistency: How do you ensure your application runs the same across all environments?
Availability: How can you update your application with zero downtime?
Containerization, using Docker, encapsulates your application and its environment, ensuring it runs consistently everywhere. Kubernetes, a container orchestration platform, automates deployment, scaling, and management, offering:

Dynamic Scaling: Adjusts application resources based on demand.
Self-healing: Restarts failed containers and reschedules them on healthy nodes.
Seamless Updates & Rollbacks: Enables zero-downtime updates and easy rollbacks.
By leveraging Kubernetes and containerization for your challenge, you embrace a scalable, consistent, and resilient deployment strategy. This not only demonstrates your technical acumen but aligns with modern DevOps practices.


## Challenge Guide

**Prerequisites**

Before you embark on this journey, ensure you are equipped with:

- Docker and Kubernetes CLI Tools: Essential for building, pushing Docker images, and managing Kubernetes resources.

- GitHub Account: For version control and implementing CI/CD pipelines.

- E-commerce Application Source Code and DB Scripts: Available at in this repo. Familiarize yourself with the application structure and database scripts provided.

**Lets Get Started**

1. **Containerize Your E-Commerce Website and Database:** 
A. Web Application Containerization
    Create a Dockerfile: Navigate to the root of the e-commerce application and create a Dockerfile. This file should instruct Docker to:
```sh
Use php:7.4-apache as the base image.
Install mysqli extension for PHP.
Copy the application source code to /var/www/html/.
Update database connection strings to point to a Kubernetes service named mysql-service.
Expose port 80 to allow traffic to the web server.
Build and Push the Docker Image:
Execute docker build -t yourdockerhubusername/ecom-web:v1 . to build your image.
Push it to Docker Hub with docker push yourdockerhubusername/ecom-web:v1.
Outcome: Your web application Docker image is now available on Docker Hub.
```

In order to do this navigate to the folder named `website`. 

```sh
cd website
```

Once you are in there you will see plenty of files. These files make up the website we are about to containerize. Lets open up the Dockerfile and read its contents.

```sh
cat Dockerfile
```

 It starts with `From` which, is specifying what the Base Image we will be using. In our requirements it specifies use `php:7.4-apache` and to install mysqli extension for PHP by using the RUN command. And then expose port 80 to allow ingress traffic to the webserver. The `website-deployment.yaml` file will take care of the db connection string in env section.

 Lets containerize the website and push it to our docker repo(Make sure to sign in to your docker account) 

```sh
docker build -t {yourdockerusername}/ecom-web:v1 .
docker push {yourdockerusername}/ecom-web:v1
```





B. Database Containerization
    Database Preparation: Instead of containerizing the database yourself, you’ll use the official MariaDB image. Prepare the database initialization script (`db-load-script.sql`) to be used with Kubernetes ConfigMaps or as an entrypoint script.
    

    
Now create a configmap using the `db-load-script.sql` file.

```sh
cd ..
kubectl create configmap db-init-script --from-file=db-load-script.sql
```


 

2. **Deploy Your Website to Kubernetes:**
Kubernetes Deployment: Create a website-deployment.yaml defining a Deployment that uses the Docker image created in Step 1A. Ensure the Deployment specifies the necessary environment variables and mounts for the database connection.
Outcome: The e-commerce web application is running on Kubernetes, with pods managed by the Deployment.

- Take a look at the `website-deployment.yaml` file. You need to modify the image to your image name(ex. image: pvass24/ecom-web:v1)

```sh
vi website-deployment.yaml
```
You will also notice that there are environment variables for our database. Since its a best practice to not hard code passwords in plain text were now going to create a secret that has the password to securely connect to our db.

```sh
kubectl create secret generic db-secret --from-literal=db-password=ecompassword
```

Create the deployment

```sh
kubectl create -f website-deployment.yaml
```

3. **Expose Your Website:**
Service Creation: Define a `website-service.yaml` to create a Service of type NodePort. This Service exposes your Deployment from your node's IP along with its random port range of 30000-32767.
Outcome: An accessible IP address for your web application from outside the cluster.

```sh
kubectl create -f website-service.yaml
```
Create the db and expose the db with a ClusterIP Service:

```sh
kubectl create -f db-deployment.yaml
kubectl create -f db-service.yaml
```


4. **Open up NodePort in your Modem to allow this port to be accessed from outside of your  local network:**
Accessing Modem Settings:
Run the command to get the nodePort 

```sh
kubectl get service ecom-web-service -o jsonpath={'.spec.ports[0].nodePort'}
```

 Make note of the NodePort. If you're using a cloud provider like EKS, you'd typically use LoadBalancer, but in our case, NodePort will be our alternative route. 
 
 To access your modem's settings:

Find your Gateway/Router IP address in your network settings.
Enter this IP address into your web browser.
Log in using the default credentials (usually found on your router. Do not confuse this with your Wifi Password).
Configuring Port Forwarding:
Once logged in, look for the port forwarding section. Here, we'll expose the NodePort and your computer's IP address. If you're not sure about your computer's IP address:

On Windows: Open Command Prompt and type ipconfig. Look for "IPv4 Address."
On Mac: Go to System Preferences > Network > Wi-Fi or Ethernet (depending on your connection) > Advanced > TCP/IP.
On Linux: Open Terminal and type ip addr.
Testing Access:
After configuring port forwarding, try accessing your website from outside your network using your IP address along with the NodePort. Test this by disconnecting from Wi-Fi on your phone and trying to access the site.

Remember, if you encounter any issues or are unsure about any steps, don't hesitate to reach out to your ISP for assistance or do a quick online search using your modem's model for guidance.


5. **Implement Configuration Management:**
Task: Add a feature toggle to the web application to enable a “dark mode” for the website.

Modify the Web Application: Add a simple feature toggle in the application code (e.g., an environment variable FEATURE_DARK_MODE that enables a CSS dark theme).
Use ConfigMaps: Create a ConfigMap named feature-toggle-config with the data FEATURE_DARK_MODE=true.
Deploy ConfigMap: Apply the ConfigMap to your Kubernetes cluster.
Update Deployment: Modify the website-deployment.yaml to include the environment variable from the ConfigMap.
Outcome: Your website should now render in dark mode, demonstrating how ConfigMaps manage application features.


6. **Scale Your Application:**
Task: Prepare for a marketing campaign expected to triple traffic.

Evaluate Current Load: Use command below to assess the current number of running pods.

```sh
kubectl get pods 
```

Scale Up: Increase replicas in your deployment or use this command below:

```sh
kubectl scale deployment/ecom-web --replicas=6
```
to handle the increased load.
Monitor Scaling: Observe the deployment scaling up with kubectl get pods.
Outcome: The application scales up to handle increased traffic, showcasing Kubernetes’ ability to manage application scalability dynamically.


7. **Perform a Rolling Update:**
Task: Update the website to include a new promotional banner for the marketing campaign.

Update Application: Modify the web application’s code to include the promotional banner.
Build and Push New Image: Build the updated Docker image as yourdockerhubusername/ecom-web:v2 and push it to Docker Hub.
Rolling Update: Update website-deployment.yaml with the new image version and apply the changes.
Monitor Update: Use kubectl rollout status deployment/ecom-web to watch the rolling update process.
Outcome: The website updates with zero downtime, demonstrating rolling updates’ effectiveness in maintaining service availability.


8. **Roll Back a Deployment:**
Task: Suppose the new banner introduced a bug. Roll back to the previous version.

Identify Issue: After deployment, monitoring tools indicate a problem affecting user experience.
Roll Back: Execute kubectl rollout undo deployment/ecom-web to revert to the previous deployment state.
Verify Rollback: Ensure the website returns to its pre-update state without the promotional banner.
Outcome: The application’s stability is quickly restored, highlighting the importance of rollbacks in deployment strategies.


9. **Autoscale Your Application:**
Task: Automate scaling based on CPU usage to handle unpredictable traffic spikes.

Implement HPA: Create a Horizontal Pod Autoscaler targeting 50% CPU utilization, with a minimum of 2 and a maximum of 10 pods.
Apply HPA: Execute kubectl autoscale deployment ecom-web --cpu-percent=50 --min=2 --max=10.
Simulate Load: Use a tool like Apache Bench to generate traffic and increase CPU load.
Monitor Autoscaling: Observe the HPA in action with kubectl get hpa.
Outcome: The deployment automatically adjusts the number of pods based on CPU load, showcasing Kubernetes’ capability to maintain performance under varying loads.


10. **Implement Liveness and Readiness Probes:**
Task: Ensure the web application is restarted if it becomes unresponsive and doesn’t receive traffic until ready.

Define Probes: Add liveness and readiness probes to website-deployment.yaml, targeting an endpoint in your application that confirms its operational status.
Apply Changes: Update your deployment with the new configuration.
Test Probes: Simulate failure scenarios (e.g., manually stopping the application) and observe Kubernetes’ response.
Outcome: Kubernetes automatically restarts unresponsive pods and delays traffic to newly started pods until they’re ready, enhancing the application’s reliability and availability.


11. **Utilize ConfigMaps and Secrets:**
Task: Securely manage the database connection string and feature toggles without hardcoding them in the application.

Create Secret and ConfigMap: For sensitive data like DB credentials, use a Secret. For non-sensitive data like feature toggles, use a ConfigMap.
Update Deployment: Reference the Secret and ConfigMap in the deployment to inject these values into the application environment.
Outcome: Application configuration is externalized and securely managed, demonstrating best practices in configuration and secret management.


12. **Document Your Process:**
Finalize Your Project Code: Ensure your project is complete and functioning as expected. Test all features locally and document all dependencies clearly.
Create a Git Repository: Create a new repository on your preferred git hosting service (e.g., GitHub, GitLab, Bitbucket).
Push Your Code to the Remote Repository
Write Documentation: Create a README.md or a blog post detailing each step, decisions made, and how challenges were overcome.
Extra credit
Package Everything in Helm
Task: Utilize Helm to package your application, making deployment and management on Kubernetes clusters more efficient and scalable.

Create Helm Chart: Start by creating a Helm chart for your application. This involves setting up a chart directory with the necessary templates for your Kubernetes resources.
Define Values: Customize your application deployment by defining variables in the values.yaml file. This allows for flexibility and reusability of your Helm chart across different environments or configurations.
Package and Deploy: Use Helm commands to package your application into a chart and deploy it to your Kubernetes cluster. Ensure to test your chart to verify that all components are correctly configured and working as expected.
Outcome: Your application is now packaged as a Helm chart, simplifying deployment processes and enabling easy versioning and rollback capabilities.
For more details, follow KodeKloud Helm Course.

Implement Persistent Storage
Task: Ensure data persistence for the MariaDB database across pod restarts and redeployments.

Create a PVC: Define a PersistentVolumeClaim for MariaDB storage needs.
Update MariaDB Deployment: Modify the deployment to use the PVC for storing database data.
Outcome: Database data persists beyond the lifecycle of MariaDB pods, ensuring data durability.
Implement Basic CI/CD Pipeline
Task: Automate the build and deployment process using GitHub Actions.

GitHub Actions Workflow: Create a .github/workflows/deploy.yml file to build the Docker image, push it to Docker Hub, and update the Kubernetes deployment upon push to the main branch.
Outcome: Changes to the application are automatically built and deployed, showcasing an efficient CI/CD pipeline.
