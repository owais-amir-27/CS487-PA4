import azure.functions as func
import azure.durable_functions as df
import os, json, time, requests

app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="orchestrators/my_orchestrator", methods=["POST"])
@app.durable_client_input(client_name="client")
async def http_starter(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    order = req.get_json()
    instance_id = await client.start_new("my_orchestrator", client_input=order)
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext):
    order = context.get_input()
    # Step 1: Call Validation
    validation = yield context.call_activity("validate_activity", order)
    
    if not validation.get("valid"):
        return {"status": "rejected", "reason": validation.get("reason", "unknown")}
    
    # Step 2: Call Report Generation
    report_url = yield context.call_activity("report_activity", order)
    return {"status": "completed", "report_url": report_url}

@app.activity_trigger(input_name="order")
def validate_activity(order: dict) -> dict:
    validate_url = os.environ["VALIDATE_URL"]
    response = requests.post(validate_url, json=order)
    return response.json()

@app.activity_trigger(input_name="order")
def report_activity(order: dict) -> str:
    from azure.mgmt.containerinstance import ContainerInstanceManagementClient
    from azure.mgmt.containerinstance.models import (
        ContainerGroup, Container, ResourceRequirements, ResourceRequests,
        ImageRegistryCredential, EnvironmentVariable, ContainerGroupIdentity
    )
    from azure.identity import DefaultAzureCredential
    import os, time, json

    # 1. Fetch all variables from the OS environment
    sub_id       = os.environ["SUBSCRIPTION_ID"]
    rg           = os.environ["REPORT_RG"]
    loc          = os.environ["REPORT_LOCATION"]
    image        = os.environ["REPORT_IMAGE"]
    storage_url  = os.environ["STORAGE_ACCOUNT_URL"]
    acr_server   = os.environ["ACR_SERVER"]
    acr_username = os.environ["ACR_USERNAME"]
    acr_password = os.environ["ACR_PASSWORD"]
    client_id    = os.environ["AZURE_CLIENT_ID"]

    order_id = order["order_id"]
    name     = f"ci-report-{order_id.lower()}"

    # 2. Setup Clients and Identity
    credential = DefaultAzureCredential()
    client = ContainerInstanceManagementClient(credential, sub_id)
    
    rollnum = rg.split("-")[-1]
    mi_id = f"/subscriptions/{sub_id}/resourcegroups/{rg}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mi-pa4-{rollnum}"

    # 3. Define the Container
    container = Container(
        name=name,
        image=image,
        resources=ResourceRequirements(requests=ResourceRequests(cpu=1.0, memory_in_gb=1.5)),
        environment_variables=[
            EnvironmentVariable(name="ORDER_ID", value=order_id),
            EnvironmentVariable(name="ORDER_JSON", value=json.dumps(order)),
            EnvironmentVariable(name="STORAGE_ACCOUNT_URL", value=storage_url),
            EnvironmentVariable(name="AZURE_CLIENT_ID", value=client_id)
        ]
    )

    # 4. Create the ACI Group
    container_group = ContainerGroup(
        location=loc,
        containers=[container],
        os_type="Linux",
        restart_policy="Never",
        image_registry_credentials=[ImageRegistryCredential(
            server=acr_server, username=acr_username, password=acr_password
        )],
        identity=ContainerGroupIdentity(
            type="UserAssigned",
            user_assigned_identities={mi_id: {}}
        )
    )

    client.container_groups.begin_create_or_update(rg, name, container_group).result()

    # 5. Wait for it to finish (Polling)
    for _ in range(30):
        group = client.container_groups.get(rg, name)
        if group.instance_view.state == "Succeeded":
            break
        time.sleep(10)

    # 6. Cleanup & Return the URL
    client.container_groups.begin_delete(rg, name)
    return f"{storage_url}/reports/{order_id}.pdf"