import requests
BASE_URL = "http://localhost:5000"

def test_tva_valid():
    response = requests.get(f"{BASE_URL}/tva", params={"ht": 100, "taux": 10})
    assert response.status_code == 200
    assert '{"ht":100.0,"taux":10.0,"ttc":110.0}\n' == response.text

def test_tva_missing_ht():
    response = requests.get(f"{BASE_URL}/tva", params={"taux": 10})
    assert response.status_code == 400
    assert '{"error":"Missing ht Parameters"}\n' == response.text

def test_tva_invalid_types():
    response = requests.get(f"{BASE_URL}/tva", params={"ht": "abc", "taux": 10})
    assert response.status_code == 400
    assert '{"error":"ht et taux doivent etre des nombres"}\n' == response.text

def test_tva_bounds():
    assert requests.get(f"{BASE_URL}/tva", params={"ht": 0, "taux": 10}).status_code == 200
    assert requests.get(f"{BASE_URL}/tva", params={"ht": 100, "taux": 0}).status_code == 200
    assert requests.get(f"{BASE_URL}/tva", params={"ht": 100, "taux": 100}).status_code == 200
    assert requests.get(f"{BASE_URL}/tva", params={"ht": 100, "taux": -1}).status_code == 400
    assert requests.get(f"{BASE_URL}/tva", params={"ht": -1, "taux": 100}).status_code == 400
