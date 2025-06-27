import requests
url = "http://localhost:5000/convert"

def test_devise():
    # Invalide from
    response = requests.get(url, params={"from":"JAMBON","to":"USD","amount": 100})
    assert response.status_code == 400
    assert '{"error":"Devise invalide"}\n' == response.text
    # Invalide TO
    response = requests.get(url, params={"from": "USD","to":"FROMAGE","amount": 100})
    assert response.status_code == 400
    assert '{"error":"Devise invalide"}\n' == response.text
    # Valide from et to mais mauvais duo EUR et GBP
    response = requests.get(url, params={"from": "GBP","to":"EUR","amount": 100})
    assert response.status_code == 400
    assert '{"error":"Devise invalide"}\n' == response.text

def test_param_manquant():
    response = requests.get(url, params={"to":"USD","amount": 100})
    assert response.status_code == 400
    assert '{"error":"Missing From Parameters"}\n' == response.text
    # Invalide TO
    response = requests.get(url, params={"from": "USD","amount": 100})
    assert response.status_code == 400
    assert '{"error":"Missing To Parameters"}\n' == response.text
    # Valide from et to mais mauvais duo EUR et GBP
    response = requests.get(url, params={"from": "GBP","to":"EUR"})
    assert response.status_code == 400
    assert '{"error":"Missing Amount Parameters"}\n' == response.text


def test_bon_appel():
    response = requests.get(url, params={"from": "USD","to":"EUR","amount": 100})
    assert response.status_code == 200
    assert '{"converted_amount":90.91,"from":"USD","original_amount":100.0,"to":"EUR"}\n' == response.text

def test_mauvais_type():
    # Invalide from
    response = requests.get(url, params={"from": 10,"to":"USD","amount": 100})
    assert response.status_code == 400
    assert '{"error":"Devise invalide"}\n' == response.text
    # Invalide TO
    response = requests.get(url, params={"from": "USD","to":10,"amount": 100})
    assert response.status_code == 400
    assert '{"error":"Devise invalide"}\n' == response.text
    # Valide from et to mais mauvais duo EUR et GBP
    response = requests.get(url, params={"from": "GBP","to":"EUR","amount": "Jour"})
    assert response.status_code == 400
    assert '{"error":"Amount doit etre un nombre"}\n' == response.text

def test_prix_invalide():
    # Prix négatif
    response = requests.get(url, params={"from": "GBP","to":"EUR","amount": -10})
    assert response.status_code == 400
    assert '{"error":"Amount doit etre superieur a 0"}\n' == response.text


