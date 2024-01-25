# K8's Kadence Flask App

## Introducing Helm

What is Helm?

Helm is a package manager for Kubernetes, which is an open-source container orchestration platform. Helm is used to simplify the deployment and management of applications on Kubernetes clusters. It allows users to define, install, and upgrade even complex Kubernetes applications with ease.

So What? 

In essence, Helm transforms the concept of "applications" into tangible, manageable entities. It eliminates the cumbersome process of individually creating Kubernetes resources such as deployments, services, ingress, and more. Instead, Helm packages these resources as "Charts," simplifying the creation and removal of applications.

Next Steps: So now we are going to create our own custom helm chart that will create everything for our Flask App! Excited? Yup I know!

### Getting Started



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
### Important Note: Create a new folder for your helm chart artifacts

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

    a. Example: Replace "repository: nginx" with --> repository: `yourdockerhubprofile/myflaskapp`

    b. Also, replace tag to your desired tag of the docker image. It will default to the latest image. In our example lets use `v3`.

    c. Change service type to `NodePort` & port to `5000`

    d-1. Update ingress enabled to `true` &  classname to `nginx`

    d-2. Remove the `{}` & Uncomment this annotation `kubernetes.io/ingress.class: nginx`
    and add this below: `nginx.ingress.kubernetes.io/rewrite-target: /`
    should look like this

    ```sh
    annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
    ```

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

### Important Note: You must be outside of the flask-app-chart directory

    ```sh
    helm install nameofyourrelease ./flask-app-chart
    ```
7. **Access your App!**
   Visit `http://localhost` and you should be able to access your application!



### Creating a multibuld Docker Image

1. **Create docker builder:**
    ```sh
    docker buildx create --name mybuilder --use
    ```
2. **Inspect the builder:**
    ```sh
    docker buildx inspect --bootstrap
    ```
3. **Build Docker image and push to docker registry:**
    ```sh
    docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t YOURDOCKERACCOUNT/myflaskapp:v4 --push .
    ```

### Upgrades and Rollbacks

To upgrade your application, make your changes is the `values.yaml` file and once complete run the command below:

1. **Upgrade Release:**
    ```sh
    helm upgrade [RELEASE_NAME ./flask-app-chart]
    ```
Rub command below and you will see there is a `REVISION` field, this lets you know what revision you are on.
2. **Check your release versions:**
    ```sh
    helm list
    ``` 

3. **Rollback Release:**
    ```sh
    helm rollback [RELEASE_NAME] <Release_number>
    ```


 


### GitOps and ArgoCD

GitOps is a modern approach to managing infrastructure and application deployments, emphasizing the use of version-controlled Git repositories as the single source of truth for defining and maintaining the desired state of your systems. In GitOps, configurations are declared in code (usually YAML or JSON), stored in Git repositories, and automatically applied to target environments, such as Kubernetes clusters, by specialized tools like ArgoCD. This approach promotes automation, consistency, and collaboration among teams, as changes are made through code updates, ensuring infrastructure and applications are always in the desired state. GitOps also provides observability and rollback capabilities, making it a robust methodology for maintaining and scaling complex systems while ensuring reliability and reproducibility.

ArgoCD is ArgoCD is an open-source, GitOps-based continuous delivery tool designed for Kubernetes environments. It automates the deployment and management of applications on Kubernetes clusters.

### Installing ArgoCD

1. **Download ArgoCD Helm Chart:**
    ```sh
    helm repo add argo https://argoproj.github.io/argo-helm
    helm repo update
    ```

2. **Confirm its been added:**
    ```sh
    helm repo list
    ```
3. **Clone the Repository:**
    ```sh
    helm install argocd argo/argo-cd \
    --namespace argocd \
    --set server.extraArgs="{--insecure}" \
    --set server.ingress.enabled=false
    ```
4. **Enable port-forwarding for ArgoCD server:**
    ```sh
    kubectl port-forward service/argocd-server -n argocd 8080:443
    ```
5. **Get Password for ArgoCD login:**
    ```sh
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
    ```

6. **Login to ArgoCD:**
    ```sh
    http://localhost:8080
    ```
