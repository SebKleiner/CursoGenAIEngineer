
import re

text_response = """
Hola, puedes contactarme en mi correo personal: usuario@example.com. 
También puedes usar mi correo de trabajo: u.ejemplo@empresa.co.
"""

def extract_emails(text):
    # Simple regex pattern to capture emails (may be simplified for demonstration)
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
    emails = re.findall(pattern, text)
    return emails

if __name__ == "__main__":
    emails_found = extract_emails(text_response)
    print("Correos encontrados:", emails_found)
