"""Campaign manager stub"""

class CampaignManager:
    def __init__(self):
        print("CampaignManager: inicializado")

    def create_campaign(self, payload: dict):
        print("CampaignManager.create_campaign: recibida payload")
        return {"status": "ok"}
