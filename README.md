1.Clone the Git repository containing the application code:
    bash
    git clone https://github.com/nick93201/SPE_Mini.git

2.Update the cal.py and test.py files with your application code and test cases.
3.Update the deploy.yml Ansible playbook with your deployment tasks.
4.Create an inventory file inventory.ini with your target hosts for deployment.

Jenkins Pipeline Steps
1.Build Code:
    Makes cal.py executable and runs it with input values.
2.Test Code:
    Executes the test cases defined in test.py.
3.Build Docker Image:
    Builds a Docker image from the current directory.
4.Push Docker Image:
    Tags and pushes the Docker image to a Docker registry.
5.Run Ansible Playbook:
    Executes an Ansible playbook for deployment using the specified playbook and inventory files.

Usage
1.Create a new Jenkins job and configure it to use this pipeline script.
2.Trigger the job to start the automated build, test, dockerization, and deployment process.

Author
Nikhil NM
