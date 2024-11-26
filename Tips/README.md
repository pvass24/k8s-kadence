Best Tips for Acing CKA, CKAD, and CKS Exams
============================================

This guide combines essential Kubernetes techniques with beginner-friendly explanations and examples. Let's dive into the skills you need to ace the exams.

* * * * *

1\. Master Basic `vim` for File Editing
---------------------------------------

The exam environment uses `vim` as the default editor. While you don't need to be an expert, knowing the basics will save you time and frustration.

### Key Commands

-   Open a File:

    bash

    Copy code

    `vim file.yaml`

-   Search for Text:

    bash

    Copy code

    `/string`

    -   Example: To search for `metadata`, type `/metadata` and press `Enter`.
    -   Use `n` to jump to the next match and `N` for the previous match.
-   Jump to a Specific Line:

    -   Inside a file:

        bash

        Copy code

        `:{line-number}`

        -   Example: Jump to line 41:

            bash

            Copy code

            `:41`

    -   Open a file directly at a specific line:

        bash

        Copy code

        `vim +{line-number} file.yaml`

        -   Example:

            bash

            Copy code

            `vim +41 deployment.yaml`

-   Make Edits and Save:

    -   Press `i` to enter insert mode.
    -   Make changes.
    -   Press `Esc` to exit insert mode.
    -   Save and exit with:

        bash

        Copy code

        `:wq`

-   Undo Changes:

    bash

    Copy code

    `u`

-   Indent or Unindent YAML:

    -   Indent: Highlight lines with `Shift + V` and press `>`.
    -   Unindent: Highlight lines with `Shift + V` and press `<`.

### Optional Configuration

Add these lines to your `~/.vimrc` for better YAML editing:

vim

Copy code

`set expandtab
set shiftwidth=2
set softtabstop=2`

* * * * *

2\. Leverage Kubernetes DNS Patterns
------------------------------------

Understanding DNS is critical for accessing services, especially across namespaces or clusters.

### DNS Patterns

1.  Within the Same Namespace:

    bash

    Copy code

    `service-name`

2.  Across Namespaces:

    bash

    Copy code

    `service-name.namespace`

3.  Fully Qualified Domain Name (FQDN):

    bash

    Copy code

    `service-name.namespace.svc.cluster.local`

### Tip to Remember

The DNS hierarchy is simple:\
`service-name` → `service-name.namespace` → `service-name.namespace.svc.cluster.local`

Use the simplest pattern first, and expand as needed.

* * * * *

3\. Use `jsonpath` for Kubernetes Queries
-----------------------------------------

`jsonpath` simplifies querying Kubernetes objects by extracting specific fields.

### Examples

-   Get the Pod Image Name:

    bash

    Copy code

    `kubectl get pod my-pod -o jsonpath='{.spec.containers[0].image}'`

    -   Output: The image name (e.g., `nginx:1.19`).
-   List All Pod Names:

    bash

    Copy code

    `kubectl get pods -o jsonpath='{.items[*].metadata.name}'`

* * * * *

4\. Learn `awk` for Text Processing
-----------------------------------

`awk` is an excellent tool for extracting and manipulating text from Kubernetes or Docker commands.

### Examples

-   Extract Image and Tag:

    bash

    Copy code

    `docker images | awk '{print $1 ":" $2}'`

    -   Combines the image repository and tag as `image:tag`.
-   Filter and Format Output:

    bash

    Copy code

    `crictl images | awk '$2 != "<none>" {print $1 ":" $2}'`

    -   Excludes images without tags.

* * * * *

5\. Use `netcat` (`nc`) for Network Diagnostics
-----------------------------------------------

`netcat` helps verify service and pod connectivity, especially when working with Network Policies.

### Examples

1.  Test Service Connectivity:

    -   From a Pod:

        bash

        Copy code

        `kubectl exec -it my-pod -- sh
        nc -zv service-name port`

    -   Across Namespaces:

        bash

        Copy code

        `nc -zv service-name.namespace.svc.cluster.local port`

2.  Test Pod-to-Pod Connectivity:

    -   From one Pod to another:

        bash

        Copy code

        `kubectl exec -it source-pod -- sh
        nc -zv target-pod-name port`

* * * * *

6\. Navigate Kubernetes Documentation Efficiently
-------------------------------------------------

The official Kubernetes documentation is a key resource during the exam. Learn to find what you need quickly.

### Tips

-   Use `Ctrl + F` to search for `kind: {resource}`.
-   Copy sample manifests and tweak them to meet exam requirements.

### Example: Create a ServiceAccount

1.  Search for "ServiceAccount" in the docs.
2.  Copy the sample YAML:

    yaml

    Copy code

    `apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: my-serviceaccount`

3.  Modify it as needed.

* * * * *

7\. Use `kubectl explain` for Syntax Help
-----------------------------------------

The `kubectl explain` command provides details about resource fields and structure.

### Examples

-   View Pod Spec Details:

    bash

    Copy code

    `kubectl explain pod.spec`

-   Dive Deeper into Fields:

    bash

    Copy code

    `kubectl explain pod.spec.containers`

* * * * *

8\. Practice with `--dry-run`
-----------------------------

Use the `--dry-run` flag to validate resources or generate YAML without making changes.

### Examples

-   Generate a Pod Manifest:

    bash

    Copy code

    `kubectl run my-pod --image=nginx --dry-run=client -o yaml > my-pod.yaml`

-   Validate YAML Syntax:

    bash

    Copy code

    `kubectl apply -f file.yaml --dry-run=client`

* * * * *

9\. Organize Files for Efficiency
---------------------------------

Use meaningful file names and keep backups to avoid losing progress.

### Tips

-   Save files with descriptive names:
    -   Example: `question1-deployment.yaml`
-   Create backups:

    bash

    Copy code

    `cp question1-deployment.yaml question1-deployment-backup.yaml`

* * * * *

10\. Debug YAML Errors Quickly
------------------------------

Errors in YAML are common. Use these steps to troubleshoot:

1.  Validate syntax:

    bash

    Copy code

    `kubectl apply -f file.yaml --dry-run=client`

2.  Navigate to the error line in `vim` and fix the issue.
3.  Reapply after corrections.

* * * * *

11\. Use Aliases to Save Time
-----------------------------

Create `kubectl` aliases to reduce typing:

bash

Copy code

`alias k=kubectl
alias kgp='kubectl get pods'
alias kaf='kubectl apply -f'`

* * * * *

12\. Time Management and Exam Setup
-----------------------------------

-   Tackle Easy Questions First: Focus on solving the easier tasks first to save time for harder ones.
-   Adjust Terminal Settings: Set a comfortable font size and colors to reduce eye strain.

* * * * *

Practice Regularly
------------------

Use tools like `minikube` or `kind` to set up a local cluster for practice. Focus on real-world tasks like debugging, deploying, and managing resources.

* * * * *

By following these detailed tips and examples, you'll build the skills and confidence to excel in the CKA, CKAD, and CKS exams!
