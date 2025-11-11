# Dummy stub para evitar error de importación
class YouTubeUploader:
	def __init__(self):
		pass
	def upload(self, video_path, metadata):
		return {"status": "ok", "videoId": "dummy_video_id"}
