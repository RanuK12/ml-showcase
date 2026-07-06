import os
import requests
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

class FinceptAPI:
    def __init__(self):
        self.base_url = os.getenv("FINCEPT_BASE_URL", "https://api.fincept.in")
        self.api_key = os.getenv("FINCEPT_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_balance_sheet(self, period="monthly", filters=None):
        """Obtener balance general."""
        endpoint = f"{self.base_url}/quantlib/instruments/balance"
        params = {"period": period}
        if filters:
            params.update(filters)
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_income_statement(self, period="monthly", filters=None):
        """Obtener estado de resultados."""
        endpoint = f"{self.base_url}/quantlib/instruments/income"
        params = {"period": period}
        if filters:
            params.update(filters)
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_cash_flow(self, period="monthly", filters=None):
        """Obtener flujo de efectivo."""
        endpoint = f"{self.base_url}/quantlib/instruments/cashflow"
        params = {"period": period}
        if filters:
            params.update(filters)
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Manejar respuestas de la API."""
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error en la API: {response.status_code} - {response.text}")