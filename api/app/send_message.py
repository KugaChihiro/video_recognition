def send_message_to_queue(file_path: str):
    from azure.storage.queue import QueueClient
    import json
    
    connection_string = "your_connection_string" #write later
    queue_name = "your_queue_name"  #write later
    
    # QueueClientのインスタンスを作成
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
    # メッセージを送信（ファイルパスを送る）
    queue_client.send_message(file_path)
    print(f"Sent message with file path: {file_path}")

   
    message = "start_vm_task"

    # メッセージとして送信するデータを作成
    message_data = {
        "file_path": file_path,
        "message": message
    }
    
    # JSON形式にシリアライズしてメッセージを送信
    queue_client.send_message(json.dumps(message_data))
    print(f"Sent message with file path and task id: {file_path}, {message}")