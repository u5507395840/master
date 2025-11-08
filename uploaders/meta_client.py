"""Meta/Facebook uploader stub"""

class MetaClient:
    def __init__(self):
        print("MetaClient: inicializado")

    def create_ad(self, config: dict):
        print("MetaClient.create_ad: config recibida")
        return {"status": "created"}
