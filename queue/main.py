from azure.storage.queue import QueueClient

queue_client = QueueClient.from_connection_string("your_connection_string", "taskQueue") #write later
queue_client.send_message("start_vm_task")