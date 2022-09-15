import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.38"
}
requests.post("https://rieltor.ua/api/users/register-sms/", json={"phone": "66660313591", "retry": 0}, headers=headers)