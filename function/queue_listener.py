# queue_listener.py

def listen_for_messages():
    from azure.storage.queue import QueueClient
    from send_http_request import send_request
    from dotenv import load_dotenv
    import os
    import json
    import azure.functions as func
    from function.get_file import file_get


    load_dotenv('.env')

    subscription_id = os.getenv("SUBSCRIPTION_ID")
    resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
    vm_name = os.getenv("VM_NAME")
    public_ip = os.getenv("PUBLIC_IP")  

    #quequeメッセージからfilepathの受け取り
    import azure.functions as func
    get_file_result = file_get(func.QueueMessage)
    file_path = get_file_result[0]
    message  =  get_file_result[1]


    # Azure Storage Queueの接続文字列とキュー名
    queue_name = os.getenv("QUEUE_NAME")
    connection_string = os.getenv("CONNECTION_STRING")

    # キューのクライアントを作成
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)

    # メッセージ内容に基づいて VM を起動,VM上のfastapiアプリケーションへHTTPリクエストを送る
    if message.content == "start_vm_task":
        send_request(public_ip,file_path)  
