# Best Tips for Acing CKA, CKAD, and CKS Exams

## 1. Master Basic `vim` for File Editing

The exam environment uses `vim` as the default editor. While you don't need to be an expert, these essential commands will help you work efficiently.

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

### Service Types
- **ClusterIP**: Internal cluster communication (default)
  - Access pattern: `service-name:port`
  - Use case: Internal microservices
- **NodePort**: External access through node IP
  - Port range: 30000-32767
  - Access pattern: `node-ip:node-port`
- **LoadBalancer**: Cloud provider load balancer
  - Automatically provisions external IP
  - Best for production external access
- **ExternalName**: CNAME record for external services
  - Maps to external DNS
  - Example: `db.example.com`

### Common Service Patterns
```yaml
# Basic ClusterIP Service
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080

# NodePort Example
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
```

### Quick Service Creation
```bash
# Create service for existing deployment
kubectl expose deployment nginx --port=80 --target-port=8080

# Create service with specific type
kubectl expose pod mypod --port=80 --type=NodePort
```

## 4. Master `jsonpath` for Kubernetes Queries

Extract specific information from Kubernetes objects efficiently:

```bash
# Get Pod image name
kubectl get pod my-pod -o jsonpath='{.spec.containers[0].image}'

# List all Pod names
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
```

## 5. Learn `awk` for Text Processing

```bash
# Extract image and tag
docker images | awk '{print $1 ":" $2}'

# Filter and format output
crictl images | awk '$2 != "<none>" {print $1 ":" $2}'
```

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

kubectl run infinite-logger \
  --image=busybox \
  --dry-run=client -o yaml \
  -- /bin/sh -c 'while true; do mkdir -p /data/logs && echo "Current time: $(date)" >> /data/logs/output.log; sleep 5; done' > infinite-logger-pod.yaml

Then you'll need to add the volume configuration separately by editing the YAML file using vim. The final YAML should look like:

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
        - while true; do mkdir -p /data/logs && echo "Current time: $(date)" >> /data/logs/output.log; sleep 5; done
      volumeMounts:
        - name: my-vol
          mountPath: /data
  volumes:
    - name: my-vol
      emptyDir: {}

# Validate the YAML
kubectl apply -f infinite-logger-pod.yaml --dry-run=client

# Generate deployment with loop
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
