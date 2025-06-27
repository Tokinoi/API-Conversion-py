import requests

BASE_URL = "http://localhost:5000"

def test_remise_valid():
    response = requests.get(f"{BASE_URL}/remise", params={"prix": 100, "pourcentage": 10})
    assert response.status_code == 200
    assert '{"pourcentage":10.0,"prixFinale":90.0,"prixInitial":100.0}\n' == response.text

def test_remise_missing_prix():
    response = requests.get(f"{BASE_URL}/remise", params={"pourcentage": 10})
    assert response.status_code == 400
    assert '{"error":"Missing Prix Parameters"}\n' == response.text

def test_remise_invalid_types():
    response = requests.get(f"{BASE_URL}/remise", params={"prix": "abc", "pourcentage": 10})
    assert response.status_code == 400
    assert '{"error":"Prix et pourcentage doivent etre des nombres"}\n' == response.text

def test_remise_bounds():
    assert requests.get(f"{BASE_URL}/remise", params={"prix": 0, "pourcentage": 10}).status_code == 200
    assert requests.get(f"{BASE_URL}/remise", params={"prix": 100, "pourcentage": 0}).status_code == 200
    assert requests.get(f"{BASE_URL}/remise", params={"prix": 100, "pourcentage": 100}).status_code == 200
    assert requests.get(f"{BASE_URL}/remise", params={"prix": 100, "pourcentage": -1}).status_code == 400
    assert requests.get(f"{BASE_URL}/remise", params={"prix": -1, "pourcentage": 100}).status_code == 400
