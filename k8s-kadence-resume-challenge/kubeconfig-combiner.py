import os
import subprocess

def merge_kubeconfigs(kubeconfig_files):
    kubeconfig_paths = ':'.join(kubeconfig_files)
    subprocess.run(f'kubectl config view --flatten --kubeconfig={kubeconfig_paths} > all-in-one-kubeconfig.yaml', shell=True, check=True)
    print("Merged kubeconfig files successfully.")

def main():
    kubeconfig_files = []
    while True:
        kubeconfig_file = input("Enter the path to a kubeconfig file (leave blank to finish): ").strip()
        if not kubeconfig_file:
            break
        kubeconfig_file = os.path.abspath(os.path.expanduser(kubeconfig_file))  # Expand ~ to user's home directory and get absolute path
        if not os.path.isfile(kubeconfig_file):
            print("File not found. Please enter a valid file path.")
            continue
        kubeconfig_files.append(kubeconfig_file)

    if not kubeconfig_files:
        print("No kubeconfig files provided. Exiting.")
        return

    # Set KUBECONFIG environment variable
    kubeconfig_paths = ':'.join(kubeconfig_files)
    os.environ['KUBECONFIG'] = kubeconfig_paths
    print("KUBECONFIG environment variable set to:", kubeconfig_paths)

    try:
        merge_kubeconfigs(kubeconfig_files)
    except Exception as e:
        print("An error occurred:", str(e))
        print("Merging kubeconfig files failed.")

    # Rename merged kubeconfig file to ~/.kube/config
    try:
        subprocess.run(['mv', 'all-in-one-kubeconfig.yaml', os.path.expanduser('~/.kube/config')], check=True)
        print("Merged kubeconfig file renamed to ~/.kube/config")
    except Exception as e:
        print("An error occurred while renaming the merged kubeconfig file:", str(e))

if __name__ == "__main__":
    main()

