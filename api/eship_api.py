import requests

class EShipAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://eladecora.eship.com.br/v3/"
        self.headers = {
            "api": self.api_key,
            "Content-Type": "application/json"
        }

    def _post(self, funcao, payload=None):
        url = f"{self.base_url}?api&funcao={funcao}"
        if payload is None: payload = {}
        try:
            res = requests.post(url, json=payload, headers=self.headers)
            if res.status_code == 200:
                try: return res.json()
                except: return {"erro": False, "raw": res.text}
            return {"erro": True, "codigo": res.status_code, "msg": res.text}
        except Exception as e:
            return {"erro": True, "msg": str(e)}

    def consultar_ordens(self, payload):
        return self._post("webServiceGetOrdem", payload)

    def consultar_contato(self, payload):
        return self._post("webServiceGetContato", payload)
