# K8s Kadence - Setting Up Our First Cluster

Welcome to the exciting world of Kubernetes! In this guide, we'll walk through the steps of creating our own Kubernetes cluster using KinD (Kubernetes in Docker) for lab and learning purposes.

## Prerequisites

Before we begin, ensure you have Docker and `kubectl` installed on your device. Depending on your operating system, follow these instructions:

### For Mac Users
- **Install Docker:**
  ```sh
  brew install docker
  ```
- **Install kubectl:**
  ```sh
  brew install kubectl
  ```
### For Windows Users
- **Install WSL 2:**
1. Enable WSL:
  ```sh
  wsl --install
  ```
  ## :rotating_light: Be sure to restart your Machine once installed! :rotating_light:

## Important Note
If you want to install a different Linux distribution, you can specify it with the --distribution flag in the wsl --install command. For example, wsl --install -d Debian for Debian. Alternatively, you can install another distribution from the Microsoft Store after setting up WSL. 

### Using Chocolatey (Windows Package Manager):
- **Install Docker:**
  ```sh
  choco install docker
  ```
- **Install KinD:**
  ```sh
  choco install kind
  ```
- **Install `kubectl`:**
  ```sh
  choco install kubernetes-cli
  ```
- **Alternatively, Install KinD Manually in PowerShell:**
  ```sh
  curl.exe -Lo kind-windows-amd64.exe https://kind.sigs.k8s.io/dl/v0.20.0/kind-windows-amd64
  Move-Item .\kind-windows-amd64.exe c:\some-dir-in-your-PATH\kind.exe
  ```
  Replace c:\some-dir-in-your-PATH with a directory in your system's PATH.

### Step 1: Download KinD(MacOS and Linux)
  For macOS and Linux users, download and install KinD, which allows us to run Kubernetes clusters locally.
  
- **On macOS via Homebrew:**
  ```sh
  brew install kind
  ```
- **On Linux:**
  ```sh
  curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/
  ```

### Step 2: Cluster Configuration(On macOS/ Windows/Linux)
  Create a file named kind-config.yaml and copy the contents below into it. This configuration sets up a cluster with one control-plane node and two worker nodes.

- **Create Config File:**
  ```sh
  kind: Cluster
  apiVersion: kind.x-k8s.io/v1alpha4
  nodes:
  - role: control-plane
  - role: worker
  - role: worker
  ```
### Step 3: Create Our Cluster
  Use the following command to create your cluster with the specified configuration:
- **Create Cluster:**
  ```sh
  kind create cluster --name my-cluster --config kind-config.yaml
  ```
- **Verify th Cluster:**
  ```sh
  kubectl get nodes
  ```
  You should see the three nodes specified in the kind-config.yaml file.

### Step 4: Kubectl Autocomplete & Aliases
  To streamline your Kubernetes command-line experience, let's set up autocomplete and aliases for kubectl.
  For ZSH Users(Mac)
- **Set up autocomplete:**
  ```sh
  source <(kubectl completion zsh)
  echo '[[ $commands[kubectl] ]] && source <(kubectl completion zsh)' >> ~/.zshrc
  ```
   For BASH Users(Linux & WSL)
- **Set up autocomplete:**
  ```sh
  source <(kubectl completion bash)
  echo "source <(kubectl completion bash)" >> ~/.bashrc
  ```
- **For shorthand usage of kubectl:**
  ```sh
  alias k=kubectl
  complete -o default -F __start_kubectl k

  ```
  This command creates an alias k for kubectl. You can then use k instead of typing out kubectl each time.


