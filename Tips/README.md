# Best Tips for Acing CKA, CKAD, and CKS Exams

## 1. Master Basic `vim` for File Editing

The exam environment uses `vim` as the default editor. While you don't need to be an expert, these essential commands will help you work efficiently.

---

### Key Commands

#### Basic Operations
- **Open a File**: `vim file.yaml`
- **Enter Insert Mode**: Press `i`
- **Exit Insert Mode**: Press `Esc`
- **Save and Exit**: `:wq`
- **Undo Changes**: Press `u`

#### Navigation
- **Search for Text**: Type `/string` and press Enter
  - Use `n` for next match
  - Use `N` for previous match
- **Jump to Line**: 
  - Inside file: `:41` (jumps to line 41)
  - Opening file: `vim +41 deployment.yaml`

#### YAML Formatting
- **Indent**: Highlight lines (`Shift + V`) → Press `>`
- **Unindent**: Highlight lines (`Shift + V`) → Press `<`

---

### Example: Debugging a Kubernetes Deployment with an Error

Suppose you are working on a deployment YAML file and encounter an error when applying it:

#### Deployment YAML (`deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: nginx:1.21.1
        ports:
        - containerPort: 80
      - name: another-container
        image: busybox:latest
         ports:            # Intentional Error: Indentation mismatch
        - containerPort: 8080

## How to Debug Using `vim`

### Step 1: Apply the YAML File
Run the following command to apply the deployment YAML file:
```bash
kubectl apply -f deployment.yaml

### Error Message Example
If there's an error in the file, you might see a message like this:
```plaintext
error: error validating "deployment.yaml": error converting YAML to JSON: yaml: line 20: did not find expected key

### Step 2: Open the File in `vim` and Jump to Line 20

1. Open the file in `vim`:
   ```bash
   vim deployment.yaml

Once the file is open, jump directly to line 20 by typing:
```plaintext
:20

Fix your error(s) and save file with

```plaintext
:x\
```

`### Handling Immutable Resources When `vim` Creates a Temporary File

When editing an immutable resource (e.g., PersistentVolumeClaim), Kubernetes might reject the changes, and `kubectl` saves the changes to a temporary file instead. You can use the temporary file to forcefully replace the resource.

#### Example: Editing a PersistentVolumeClaim (PVC)

1. Attempt to edit the PVC:
   ```bash
   kubectl edit pvc alpha-pvc -n alpha
   ```

1.  If the PVC is immutable, you might see an error like this:
   
    ```bash
    error: persistentvolumeclaims "alpha-pvc" is invalid
    spec: Forbidden: spec is immutable after creation except resources.requests and volumeAttributes for bound claims
    A copy of your changes has been stored to "/tmp/kubectl-edit-3898228328.yaml"
    error: Edit cancelled, no valid changes were saved.
    ```

3.  Locate the temporary file that `kubectl` created:
    ```bash
    /tmp/kubectl-edit-3898228328.yaml
    ```

4.  Forcefully replace the PVC using the temporary file:
    ```bash
    kubectl replace -f /tmp/kubectl-edit-3898228328.yaml --force --grace-period=0
    ```

* * * * *

#### Explanation

-   Immutable Resources: Certain Kubernetes resources, like PersistentVolumeClaims (PVCs), have immutable fields that cannot be updated directly.
-   Temporary File: When you use `kubectl edit` on an immutable resource, `kubectl` saves the changes to a temporary file and aborts the edit.
-   `kubectl replace`: Replaces the resource with the updated manifest.
-   `--force`: Deletes the existing resource and recreates it.
-   `--grace-period=0`: Ensures the resource is terminated immediately without waiting for the default grace period.

* * * * *

#### Best Practice

If replacing a resource, ensure you understand the implications, as it will delete and recreate the resource. For PVCs, this might temporarily disconnect Pods relying on the PVC.


### Recommended `.vimrc` Configuration
```vim
set expandtab
set shiftwidth=2
set softtabstop=2
```



## 2. Leverage Kubernetes DNS Patterns

Understanding DNS patterns is crucial for service communication across your cluster.

### DNS Hierarchy
1. Same Namespace: `service-name`
2. Cross Namespace: `service-name.namespace`
3. FQDN: `service-name.namespace.svc.cluster.local`

> 💡 **Pro Tip**: Start with the simplest pattern and expand as needed.

## 3. Master Pod and Service Communication

Understanding how Pods communicate with each other and with external clients is crucial in Kubernetes. Services provide the abstraction needed to route traffic to the appropriate Pods seamlessly.

### Service Types

- **ClusterIP** (Default):
  - **Purpose:** Internal cluster communication.
  - **Access Pattern:** `service-name:port`.
  - **Use Case:** Facilitates communication between microservices within the cluster.
  - **Example:** A frontend service accessing a backend service via its `ClusterIP`.

- **NodePort**:
  - **Purpose:** Expose a service on the node's IP at a static port.
  - **Port Range:** 30000-32767.
  - **Access Pattern:** `node-ip:node-port`.
  - **Use Case:** Useful for simple external access to applications during development or testing.

- **LoadBalancer**:
  - **Purpose:** Provides an external IP via a cloud provider's load balancer.
  - **Access Pattern:** `external-ip:port`.
  - **Use Case:** Best for production deployments needing external traffic routing to the cluster.

- **ExternalName**:
  - **Purpose:** Maps a service to an external DNS record (e.g., external databases or APIs).
  - **Access Pattern:** Uses a CNAME record to redirect traffic.
  - **Example:** `db.example.com` as the external database endpoint.

---

### Common Service Patterns

#### ClusterIP Example
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - name: http         # Optional name for the port
      port: 80           # Service port (used for communication)
      targetPort: 8080   # Internal Pod container port
### Key Details
- **name**: A unique identifier for the port (useful when multiple ports are defined in a service).
- **port**: The port the service exposes to other services or Pods in the cluster.
- **targetPort**: The internal container port where the application listens. If omitted, it defaults to the value of `port`.

---

### NodePort Example
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - name: http
      port: 80           # Service port
      targetPort: 8080   # Internal Pod container port
      nodePort: 30080    # Fixed external port on the node

### Key Details
- **nodePort**: Maps the service to a specific port on each node, making it accessible externally using the node's IP.
- Naming the port with `name` is useful for distinguishing between multiple ports (e.g., `http` vs. `https`).

---

### Quick Service Creation

You can easily create services for existing workloads using the `kubectl expose` command.

```bash
# Expose a Deployment with a ClusterIP service
kubectl expose deployment nginx --name=nginx-svc --port=80 --target-port=8080 

# Expose a Pod with a NodePort service
kubectl expose pod mypod --name=mypod-svc --port=80 --type=NodePort

### Key Notes
- If `type` is not specified, `ClusterIP` is used by default.
- The `targetPort` represents the internal port the container is listening on. If omitted, it defaults to the value of `port`.
- Use the `--port` flag to define the service's exposed port.

---

### Naming Ports in Services

Kubernetes allows naming ports with the `name` field.

#### Benefits of Naming Ports
- Useful when multiple ports are defined in the service.
- Helps identify ports easily in configuration files.
- Required when using protocols like HTTP/2 or gRPC, as some controllers (e.g., Ingress) rely on port names to route traffic.

#### Example with Named Ports
```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: https
      port: 443
      targetPort: 8443


## 4. Master `jsonpath` for Kubernetes Queries

Extract specific information from Kubernetes objects efficiently:

```bash
# Get Pod image name
kubectl get pod my-pod -o jsonpath='{.spec.containers[0].image}'

# List all Pod names
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
```

## 5. Learn `awk` for Text Processing

`awk` is a powerful tool for extracting and formatting text, making it highly useful when working with Kubernetes, Docker, or CI/CD pipelines.

---

### Common Examples

#### Extract Image and Tag
Use `awk` to combine the image repository and tag for a cleaner output:

```bash
crictl images

Output:

IMAGE                                     TAG                 IMAGE ID            SIZE
docker.io/bitnami/nginx                   latest              d42eb6c65d81d       67.1MB
docker.io/kodekloud/webapp-color          latest              32a1ce4c22f21       31.8MB
docker.io/library/busybox                 <none>              27a71e19c9562       2.17MB
docker.io/library/busybox                 latest              517b897a6a831       2.17MB
docker.io/library/nginx                   1.13                ae513a47849c8       44.6MB
docker.io/library/nginx                   1.14                295c7be079025       44.7MB
docker.io/library/nginx                   1.16                dfcfd8e9a5d38       51MB
docker.io/library/nginx                   1.17                9beeba249f3ee       51MB
docker.io/library/nginx                   alpine              a5967740120f9       22.8MB
docker.io/library/nginx                   latest              3b25b682ea82b       73MB
docker.io/library/ubuntu                  latest              59ab366372d56       29.8MB

```bash
crictl images | awk '{print $1 ":" $2}'

Output:

IMAGE:TAG
docker.io/bitnami/nginx:latest
docker.io/kodekloud/webapp-color:latest
docker.io/library/busybox:<none>
docker.io/library/busybox:latest
docker.io/library/nginx:1.13
docker.io/library/nginx:1.14
docker.io/library/nginx:1.16
docker.io/library/nginx:1.17
docker.io/library/nginx:alpine
docker.io/library/nginx:latest


### Explanation:
- **`$1`**: Refers to the first column (image repository).
- **`$2`**: Refers to the second column (image tag).
- Combines both with `:` to output `repository:tag`.

Even further, you can add tail -n +2 to remove the IMAGE:TAG header

```bash
crictl images | tail -n +2 | awk '{print $1 ":" $2}'

Output:

docker.io/bitnami/nginx:latest
docker.io/kodekloud/webapp-color:latest
...

---

### Filter and Format Output

Remove entries with `<none>` tags from the output:
```bash
crictl images | awk '$2 != "<none>" {print $1 ":" $2}'
```

### Scanning Filtered Images for CRITICAL Vulnerabilities Using `trivy`

This command filters images with names containing `nginx`, scans them for CRITICAL vulnerabilities using `trivy`, and prints only the "Total" line from the scan output.

#### Command:
```bash
for i in $(crictl images | awk '/nginx/ {print $1 ":" $2}'); do
  echo "Scanning $i for CRITICAL vulnerabilities...";
  trivy image $i --severity CRITICAL --quiet | grep Total;
done
```

* * * * *

### Explanation:

1.  Filter Images by Name:

    -   The `awk '/nginx/ {print $1 ":" $2}'` portion filters the images whose name contains the word `nginx` in the output of `crictl images`.
    -   It combines the first column (image repository) and the second column (image tag) into `repository:tag` format.
2.  Loop Through Filtered Images:

    -   The `for i in $(...)` loop iterates over each filtered image name and assigns it to the variable `$i`.
3.  Scan Each Image:

    -   The `trivy image $i --severity CRITICAL --quiet` command runs a vulnerability scan for the current image:
        -   `--severity CRITICAL`: Limits the scan to CRITICAL vulnerabilities.
        -   `--quiet`: Suppresses non-essential output, such as logs and informational messages.
4.  Filter Scan Results:

    -   The `grep Total` command filters the output to include only the line containing the word `Total`, which summarizes vulnerability counts.

* * * * *

### Example Output:

For images like `nginx:latest` and `nginx:alpine`, the command might produce output like this:

```bash
`Scanning docker.io/nginx:latest for CRITICAL vulnerabilities...
Total: 3 (CRITICAL: 1, HIGH: 2)

Scanning docker.io/nginx:alpine for CRITICAL vulnerabilities...
Total: 0 (CRITICAL: 0, HIGH: 0)`
```
* * * * *

### Key Notes:

-   Filtering by Image Name:

    -   The `/nginx/` filter in `awk` ensures that only images with "nginx" in their name are included in the loop.
    -   You can replace `nginx` with any other keyword to filter specific images.
-   Focused Output:

    -   By using `--quiet` and `grep Total`, the command ensures that only relevant results are displayed.
-   Custom Filters:

    -   Modify the `awk` filter to match different image patterns or exclude specific tags (e.g., `<none>`).

This approach combines flexibility and simplicity, making it efficient for scanning targeted images in your environment.


## 6. Network Diagnostics with `netcat`

### Testing Connectivity
```bash
# Test service in same namespace
kubectl exec -it my-pod -- sh
nc -zv service-name port

# Test cross-namespace service
nc -zv service-name.namespace.svc.cluster.local port

# Test Pod-to-Pod
kubectl exec -it source-pod -- sh
nc -zv target-pod-name port
```

## 7. Navigate Kubernetes Documentation

### Quick Tips
- Use `Ctrl + F` to find resource definitions with `kind: {resource}`
- Copy and modify sample manifests
- Bookmark frequently used pages

### Example: Creating a ServiceAccount
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-serviceaccount
```

## 8. Use `kubectl explain` for Quick Reference

```bash
# View Pod spec details
kubectl explain pod.spec

# Deep dive into container configuration
kubectl explain pod.spec.containers
```

## 9. Validate with `--dry-run`
```bash
kubectl run infinite-logger \
  --image=busybox \
  --dry-run=client -o yaml \
  -- /bin/sh -c 'while true; do echo "Current time: $(date)" >> /data/logs/output.log; sleep 5; done' > infinite-logger-pod.yaml
```

Then you'll need to add the volume configuration separately by editing the YAML file using vim. The final YAML should look like:
```bash
apiVersion: v1
kind: Pod
metadata:
  name: infinite-logger
spec:
  containers:
    - name: infinite-logger
      image: busybox
      command: ["/bin/sh", "-c"]
      args:
        - while true; do echo "Current time: $(date)" >> /data/logs/output.log; sleep 5; done
      volumeMounts:
        - name: my-vol
          mountPath: /data
  volumes:
    - name: my-vol
      emptyDir: {}
```

# Validate the YAML
```bash
kubectl apply -f infinite-logger-pod.yaml --dry-run=client
```

# Generate deployment with loop
```bash
kubectl create deployment loop-deployment \
  --image=busybox \
  --replicas=2 \
  --dry-run=client -o yaml \
  -- /bin/sh -c 'while true; do echo "Pod $HOSTNAME running"; sleep 10; done' > loop-deployment.yaml
```

## 10. File Organization Best Practices

- Use descriptive names: `question1-deployment.yaml`
- Keep backups: `cp file.yaml file-backup.yaml`
- Organize by resource type or question number

## 11. Debug YAML Efficiently

1. Validate syntax with `--dry-run`
2. Use vim to jump to error lines
3. Reapply after fixes

## 12. Time-Saving Aliases

```bash
alias k=kubectl
alias kgp='kubectl get pods'
alias kaf='kubectl apply -f'
```

## 13. Exam Strategy

### Time Management
- Start with easier questions
- Mark difficult questions for review
- Leave time for double-checking work

### Environment Setup
- Adjust terminal font size
- Set comfortable color scheme
- Test aliases before starting

## Practice Tips

- Set up a local cluster using `minikube` or `kind`
- Practice real-world scenarios
- Time yourself on practice questions
- Review and learn from mistakes

> 🎯 **Remember**: Regular practice with these tools and techniques is key to exam success!
