"""YouTube uploader stub"""

class YouTubeUploader:
    def __init__(self):
        print("YouTubeUploader: inicializado")

    def upload(self, file_path: str, title: str):
        print(f"YouTubeUploader.upload: {file_path} -> {title}")
        return {"status": "queued"}
