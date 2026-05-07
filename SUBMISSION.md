<div align="center">

# PA4 Submission: TaskFlow Pipeline

<img alt="GitHub only" src="https://img.shields.io/badge/Submit-GitHub%20URL%20Only-10b981?style=for-the-badge">
<img alt="Total points" src="https://img.shields.io/badge/Total-100%20points-7c3aed?style=for-the-badge">

</div>

## Student Information

| Field | Value |
|---|---|
| Name | Owais Amir |
| Roll Number | 27100429 |
| GitHub Repository | https://github.com/owais-amir-27/CS487-PA4 |
| Resource Group | `rg-sp26-27100429` |
| Assigned Region | `ukwest` |

## Evidence Rules

- Use relative image paths, for example: `![AKS nodes](docs/aks-nodes.png)`.
- Every image must have a 1-3 sentence description below it.
- Azure Portal screenshots must show the resource name and enough page context to identify the service.
- CLI screenshots must show the command and output.
- Mask secrets such as function keys, ACR passwords, and storage connection strings.


## Task 1: App Service Web App (15 points)

### Evidence 1.1: Forked Repository

![Forked Repo](docs/images/Screenshot%202026-05-06%20212649.png)

**Description:** This shows my forked CS487-PA4 repository under my GitHub account, containing the base starter code for the assignment.

### Evidence 1.2: App Service Overview

![App Service Overview](docs/images/Screenshot%202026-05-06%20212839.png)

**Description:** The Azure Portal overview page for my App Service `pa4-27100429`. It confirms the app is in the `rg-sp26-27100429` resource group and currently holds a "Running" status.

### Evidence 1.3: Deployment Center / GitHub Actions

![Deployment Center](docs/images/Screenshot%202026-05-06%20212933.png)

**Description:** This shows the Deployment Center logs with a "Succeeded" status, confirming the GitHub Actions workflow successfully built and deployed the Node.js code.

### Evidence 1.4: Live Web UI

![Live Web UI](docs/images/Screenshot%202026-05-06%20212951.png)

**Description:** The TaskFlow frontend interface successfully loading in my browser via the public `.azurewebsites.net` URL, proving the frontend Node app is being served correctly.

---

## Task 2: Azure Container Registry (15 points)

### Evidence 2.1: ACR Overview

![ACR Overview](docs/images/Screenshot%202026-05-07%20215019.png)

**Description:** The overview of my Azure Container Registry named `pa427100429` in the UK West region.

### Evidence 2.2: Docker Builds

![Docker Build 1](docs/images/Screenshot%202026-05-07%210747.png)
![Docker Build 2](docs/images/Screenshot%202026-05-07%20211222.png)
![Docker Build 3](docs/images/Screenshot%202026-05-07%20215045.png)

**Description:** My terminal showing the successful local execution of `docker build` commands for the `validate-api`, `report-job`, and `func-app` directories using the `linux/amd64` platform flag.

### Evidence 2.3: ACR Repositories

![ACR Repositories 1](docs/images/Screenshot%202026-05-07%20215145.png)
![ACR Repositories 2](docs/images/Screenshot%202026-05-07%20215056.png)

**Description:** CLI output confirming that all three images (`func-app`, `report-job`, and `validate-api`) were successfully tagged as `:v1` and pushed to my cloud registry.

---

## Task 3: Durable Function Implementation (12 points)

### Evidence 3.1: Completed Function Code

[function_app.py](function-app/function_app.py)

**Description:** My orchestrator function safely chains two activities together. It first yields the validation activity; if the order is valid, it proceeds to yield the report generation to spin up the ACI container.

### Evidence 3.2: Local Function Handler Listing

![Local Function Run](docs/images/Screenshot%202026-05-07%20220054.png)

**Description:** The terminal output showing the Azure Functions Core Tools successfully launching locally, having discovered and mapped my orchestrator and activity endpoints.

---

## Task 4: Function App Container Deployment (8 points)

### Evidence 4.1: Function App Container Configuration



**Description:** The Function App uses the `func-app:v1` Docker image directly from my ACR vault.

### Evidence 4.2: Orchestration Smoke Test

![Orchestration Smoke Test](docs/images/Screenshot%202026-05-07%20221655.png)

**Description:** A terminal `curl` POST request to my deployed Function App. The JSON response returns the unique instance `id` and the `statusQueryGetUri` required to poll the orchestration state.

### Evidence 4.3: Expected Failed Status Before Downstream Wiring

![Failed Status](docs/images/Screenshot%202026-05-07%20221712.png)

**Description:** Polling the `statusQueryGetUri` reveals a "Failed" status. This is expected because the downstream services were not yet wired, causing the initial activity to gracefully fail.

---

## Task 5: AKS Validator (15 points)

### Evidence 5.1: AKS Cluster


**Description:** Overview of the AKS cluster `pa4-27100429` running on a `Standard_B2s` VM size.

### Evidence 5.2: Kubernetes Nodes and Pods

![K8s Nodes](docs/images/Screenshot%202026-05-07%20223148.png)
![K8s Pods](docs/images/Screenshot%202026-05-07%20223140.png)

**Description:** Output of `kubectl get nodes` showing the node is Ready, and `kubectl get pods` showing the `validate-deployment` pod is successfully running my ACR image.

### Evidence 5.3: Kubernetes Service

![K8s Service](docs/images/Screenshot%202026-05-07%20223135.png)

**Description:** Output of `kubectl get service validate-service` showing the LoadBalancer has successfully acquired an external public IP on port 8080.

### Evidence 5.4: Validator API Tests

![API Test 1](docs/images/Screenshot%202026-05-07%20223405.png)
![API Test 2](docs/images/Screenshot%202026-05-07%20223054.png)
![API Test 3](docs/images/Screenshot%202026-05-07%20223113.png)

**Description:** `curl` tests against the AKS public IP confirming `/health` returns "ok", a valid `/validate` returns true, and an invalid `/validate` correctly returns false.

### Evidence 5.5: Function App `VALIDATE_URL`

![Function App Env Vars](docs/images/Screenshot%202026-05-07%20223240.png)

**Description:** The environment variables for my Function App showing `VALIDATE_URL` mapped strictly to the external IP address of my AKS LoadBalancer service.

### Evidence 5.6: AKS Idle Behavior



**Description:** The AKS node remains running continuously even when there are no orders to validate, showing the "always-on" nature of the service.

---

## Task 6: ACI Report Job (15 points)

### Evidence 6.1: Blob Container

![Blob Container](docs/images/Screenshot%202026-05-07%20224257.png)

**Description:** The `reports` container successfully created within my storage account to hold the dynamically generated PDFs.

### Evidence 6.2: Manual ACI Run

![Manual ACI Run](docs/images/Screenshot%202026-05-07%20224322.png)

**Description:** Output of `az container show` returning a Succeeded/Terminated state for the test container, proving the ephemeral job booted, executed, and exited.

### Evidence 6.3: ACI Logs

![ACI Logs](docs/images/Screenshot%202026-05-07%20224333.png)

**Description:** Output of `az container logs` showing the Python print statements confirming the container successfully generated and uploaded the PDF.

### Evidence 6.4: Generated PDF

![Generated PDF](docs/images/Screenshot%202026-05-07%20224358.png)

**Description:** Output proving that the `.pdf` was physically written into the blob storage container by the ACI process.

### Evidence 6.5: Function App Managed Identity and IAM

![Managed Identity](docs/images/Screenshot%202026-05-07%20224425.png)

**Description:** The Function App Identity blade showing the assigned managed identity, granting the function the necessary Azure RBAC permissions to dynamically spawn ACI containers.

### Evidence 6.6: Report App Settings

![App Settings](docs/images/Screenshot%202026-05-07%20224537.png)

**Description:** The Function App settings showing `REPORT_*` variables pointing to my registry image, `ACR_*` containing credentials, and the `STORAGE_ACCOUNT_URL`.

---

## Task 7: End-to-End Pipeline (15 points)

### Evidence 7.1: Web App Wiring

*(Skipped for time)*

**Description:** `FUNCTION_START_URL` and `FUNCTION_STATUS_URL` configured on the Web App.

### Evidence 7.2: Happy Path UI

![Happy Path UI 1](docs/images/Screenshot%202026-05-07%20230522.png)
![Happy Path UI 2](docs/images/Screenshot%202026-05-07%20230639.png)

**Description:** The TaskFlow dashboard showing a successful order traversing from form submission to "Completed", exposing the direct download link for the generated PDF.

### Evidence 7.3: Backend Participation

![Function Logs](docs/images/Screenshot%202026-05-07%20230832.png)
![AKS Logs](docs/images/Screenshot%202026-05-07%20231009.png)
![Blob List](docs/images/Screenshot%202026-05-07%20231005.png)
![Report Details](docs/images/Screenshot%202026-05-07%20230804.png)

**Description:** Logs showing `my_orchestrator` firing sequentially, with Kubernetes and Blob logs confirming the end-to-end traversal of the unique order ID.

### Evidence 7.4: Reject Path UI

![Reject Path UI](docs/images/Screenshot%202026-05-07%20231132.png)
![Reject Path Log](docs/images/Screenshot%202026-05-07%20231238.png)

**Description:** The dashboard catching a rejection for an order with 999 items. The Durable Function gracefully short-circuits and skips the ACI creation step.

---

## Task 8: Write-up and Architecture Diagram (5 points)

### Evidence 8.1: Architecture Diagram



**Description:** The complete logical flow showing the App Service frontend triggering the Durable Function backend, which polls AKS for validation, spawns ACI for reports, and writes to Blob Storage.

### Question 8.2: Service Selection

TaskFlow uses **App Service** for the frontend because it provides simple, managed web hosting with out-of-the-box CI/CD integration from GitHub. **Durable Functions** act as the central brain because they offer stateful orchestration, allowing the system to safely "sleep" while waiting for long-running downstream tasks to finish. **AKS** is used for the validation API because it acts as a highly available, always-on microservice capable of handling rapid, concurrent requests. Finally, **ACI** is chosen for report generation because it provides on-demand, serverless compute that executes a specific job and immediately tears down, saving money compared to running a dedicated worker VM.

### Question 8.3: ACI vs AKS

**AKS** requires provisioning a permanent virtual machine (node) that runs continuously, meaning we pay for 24/7 compute regardless of traffic, but the API responds instantly with no cold starts. **ACI**, on the other hand, operates on an on-demand billing model where we are only charged for the exact seconds the container is active. While ACI saves money for infrequent tasks, it suffers from cold starts, meaning it takes time to pull the image and boot the container before the job can even begin.

### Question 8.4: Durable Functions vs Plain HTTP

First, Durable Functions solve the "double-billing" and timeout problems; if we used a plain HTTP function, it would have to stay awake and actively wait for the ACI container to finish generating the report, charging us for idle time and risking an HTTP timeout. Durable Functions gracefully checkpoint their state and go to sleep while waiting for the ACI. Second, Durable Functions provide automatic state management; we don't need to build a separate database to track whether an order is "pending," "validating," or "completed" because the orchestrator exposes its current state natively via the status polling URL.

### Question 8.5: Cost Review



**Description:** The **Azure Kubernetes Service (Virtual Machine Scale Sets)** is the most expensive resource because it requires provisioning a dedicated `Standard_B2s` VM that runs continuously 24/7 to keep the validation API highly available, whereas the Functions and ACI only incur costs when actively executing code.

### Question 8.6: Challenges Faced

1. **GitHub Actions Folder Path Bug:** During Task 1, the automated deployment kept failing because the Azure generated YAML script assumed the Node code was in the root directory. I debugged this by checking the GitHub Actions runner logs, realizing it couldn't find `package.json`, and manually editing the `.yml` file to `cd webapp` before running `npm install` and updating the package path.
2. **Environment Variable Context in Python:** During Task 6/7, the ACI creation failed via the Durable Function with a `NameError: name 'SUBSCRIPTION_ID' is not defined`. By polling the Function status endpoint and reading the stack trace, I realized the Python script was trying to use the variable directly rather than fetching it from the OS. I fixed the code by explicitly mapping `os.environ["SUBSCRIPTION_ID"]` before passing it to the Azure SDK client.