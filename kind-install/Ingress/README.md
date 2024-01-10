### Step 1: Cluster Configuration(On macOS/ Windows/Linux)
  Create a file named `kind-ingress-config.yaml` and copy the contents below into it. This configuration sets up a cluster with one control-plane node and two worker nodes. However this config also sets up the cluster to have the capabilities to enable Ingress. We still have to install the ingress and the Ingress controller, which will be revealed later.

- **Create Config File:**
  ```sh
  kind: Cluster
  apiVersion: kind.x-k8s.io/v1alpha4
  nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
  - role: worker
  - role: worker 
  ```
### Step 2: Create Our Cluster
  Use the following command to create your cluster with the specified configuration:
- **Create Cluster:**
  ```sh
  kind create cluster --name my-ingress-cluster --config kind-ingress-config.yaml
  ```
- **Verify the Cluster:**
  ```sh
  kubectl get nodes
  ```
  You should see the three nodes specified in the kind-ingress-config.yaml file.

### Step 3: Create Our NGINX Ingress Controller
  Use the following command to create your cluster with the specified configuration:
- **Create NGINX Ingress Controller:**
  ```sh
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
  ```
  The manifests contains kind specific patches to forward the hostPorts to the ingress controller, set taint tolerations and schedule it to the custom labelled node.

Now the Ingress Controller is all setup. Wait until is ready to process requests running:
  ```sh
  kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
  ```


