#!/usr/bin/env python3
# auto_whatsapp_web_sender.py — Envía mensajes automáticos por WhatsApp Web usando Selenium.
# Requiere: selenium, webdriver-manager, Chrome instalado.

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def enviar_mensaje_whatsapp(numero, mensaje, espera=3):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://web.whatsapp.com/")
        input("👉 Escanea el código QR y presiona Enter...")

        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.send_keys(numero)
        time.sleep(espera)
        search_box.send_keys(Keys.ENTER)

        msg_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        msg_box.send_keys(mensaje)
        time.sleep(1)
        msg_box.send_keys(Keys.ENTER)
        print(f"✅ Mensaje enviado a {numero}")
        time.sleep(2)
        driver.quit()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Ejemplo de uso:
    # python3 auto_whatsapp_web_sender.py "+5493511234567" "Hola! Este es un mensaje automático."
    import sys
    if len(sys.argv) != 3:
        print("Uso: python3 auto_whatsapp_web_sender.py <número> <mensaje>")
    else:
        enviar_mensaje_whatsapp(sys.argv[1], sys.argv[2])