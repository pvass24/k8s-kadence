# K8's Kadence Flask App

## Introducing Helm

What is Helm?

Helm is a package manager for Kubernetes, which is an open-source container orchestration platform. Helm is used to simplify the deployment and management of applications on Kubernetes clusters. It allows users to define, install, and upgrade even complex Kubernetes applications with ease.

So What? 

In essence, Helm transforms the concept of "applications" into tangible, manageable entities. It eliminates the cumbersome process of individually creating Kubernetes resources such as deployments, services, ingress, and more. Instead, Helm packages these resources as "Charts," simplifying the creation and removal of applications.

Next Steps: So now we are going to create our own custom helm chart that will create everything for our Flask App! Excited? Yup I know!

## Getting Started



### Install Helm

From Homebrew (macOS)
1. **Clone the Repository:**
    ```sh
    brew install helm    
    ```

From Apt (Debian/Ubuntu)
   **Clone the Repository:**
    ```sh
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
    ```

From Apt (Debian/Ubuntu)
   **Clone the Repository:**
    ```sh
    choco install kubernetes-helm    
    ```

2. **Create your Helm Chart:**
    ```sh
    helm create flask-app-chart
    ```

3. **Comment out appVersion in Chart.yaml file:**
    Example --> #appVersion: "1.16.0"
    ```sh
    vi Chart.yaml
    ```

4. **Add your Docker image to the values.yaml file:**
    a. Example: Replace "repository: nginx" with --> repository: "yourdockerhubprofile/myflaskapp"
    b. Also, replace tag to your desired tag of the docker image. It will default to the latest image.
    c. Change service type to `NodePort` & port to `5000`
    d-1. Update ingress to true classname to `nginx`
    d-2. Uncomment this annotation `nginx.ingress.kubernetes.io/rewrite-target: /`
    d-3. Make host value empty
    d-4. Update pathType to `Prefix` 
    ```sh
    vi values.yaml
    ```
5. **Modify the templates/deployment.yaml file**
    a. below readinessProbe add this:
    
    ```sh
    env:
      - name: POD_NAME
        valueFrom:
          fieldRef:
            fieldPath: metadata.name
    ```
6. **Install your helm release:**
   ##Important Note: 
   You must be outside of the flask-app-chart directory
    ```sh
    helm install nameofyourrelease flask-app-chart
    ```
7. **Access your App!**
   Visit `http://localhost` and you should be able to access your application!


### Installing ArgoCD



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


