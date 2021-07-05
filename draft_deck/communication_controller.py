import requests


class CommunicationController:
    def __init__(self, drafter):
        self.drafter = drafter
        self.url = ""