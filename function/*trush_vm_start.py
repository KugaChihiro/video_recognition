def start_vm(subscription_id: str, resource_group_name: str, vm_name: str):
    from azure.mgmt.compute import ComputeManagementClient
    from azure.identity import DefaultAzureCredential

    # Azureの認証情報を取得
    credential = DefaultAzureCredential()
    # ComputeManagementClientを作成
    compute_client = ComputeManagementClient(credential, subscription_id)

    
    # VMを起動（非同期ではなく同期で実行）
    print(f"Starting VM: {vm_name} in resource group: {resource_group_name}...")
    # VM 起動の同期的なメソッド
    compute_client.virtual_machines.start(resource_group_name, vm_name)
    print(f"VM {vm_name} has been started.")
