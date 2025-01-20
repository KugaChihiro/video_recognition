def file_get(msg) -> None:
    import json

    # メッセージのボディからJSONをデコード
    message_data = json.loads(msg.get_body().decode('utf-8'))
    
    # JSONからファイルパスとメッセージを取得
    file_path = message_data["file_path"]
    message = message_data["message"]
    
    print(f"Received file path: {file_path}, message: {message}")
    
    return [file_path, message]