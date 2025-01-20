def send_request(public_ip,file_path):
    import requests
    url = f"http://{public_ip}:8000"

    # ファイルを開く
    with open(file_path, "rb") as f:
        # ファイルを 'files' パラメータとして送信
        files = {"file": (file_path, f, "application/octet-stream")}
        response = requests.post(url, files=files)
        print(response.status_code)  # レスポンスのステータスコードを表示
        print(response.text)  # レスポンスの内容を表示
