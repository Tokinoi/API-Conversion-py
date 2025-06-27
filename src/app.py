from main import app
from flask import Flask, request, jsonify, make_response

# ===== Fonction de conversion entre devises =====
def api_Convertion(_from, _to):
    data = dict()

    data["EUR"] = {}
    data["EUR"]["USD"] = 1.1

    data["USD"] = {}
    data["USD"]["EUR"] = 1 / 1.1
    data["USD"]["GBD"] = 0.8

    data["GBD"] = {}
    data["GBD"]["USD"] = 1 / 0.8

    return data[_from][_to]


# ===== Route /convert =====
@app.route('/convert')
def convert():
    _from = request.args.get('from')
    _to = request.args.get('to')
    _amount = request.args.get('amount')

    if _from is None or _from.strip() == "":
        return make_response(jsonify({"error": "Missing From Parameters"}), 400)
    if _to is None or _to.strip() == "":
        return make_response(jsonify({"error": "Missing To Parameters"}), 400)
    if _amount is None or _amount.strip() == "":
        return make_response(jsonify({"error": "Missing Amount Parameters"}), 400)
    try:
        amount = float(_amount)
    except ValueError:
        return make_response(jsonify({"error": "Amount doit etre un nombre"}), 400)

    if amount <= 0:
        return make_response(jsonify({"error": "Amount doit etre superieur a 0"}), 400)

    try:
        converted_amount = amount * api_Convertion(_from, _to)
    except:
        return make_response(jsonify({"error": "Devise invalide"}), 400)

    output = {
        "from": _from,
        "to": _to,
        "original_amount": amount,
        "converted_amount": round(converted_amount, 2)
    }

    return jsonify(output), 200

# ===== Route /tva =====
@app.route('/tva')
def tva():
    _ht = request.args.get('ht')
    _taux = request.args.get('taux')

    if _ht is None or _ht.strip() == "":
        return make_response(jsonify({"error": "Missing ht Parameters"}), 400)
    if _taux is None or _taux.strip() == "":
        return make_response(jsonify({"error": "Missing taux Parameters"}), 400)

    try:
        ht = float(_ht)
        taux = float(_taux)
    except ValueError:
        return make_response(jsonify({"error": "ht et taux doivent etre des nombres"}), 400)

    if ht < 0:
        return make_response(jsonify({"error": "ht doit etre supérieur à 0"}), 400)
    if taux < 0:
        return make_response(jsonify({"error": "taux doit etre supérieur à 0"}), 400)
    if taux > 100:
        return make_response(jsonify({"error": "taux doit etre inférieur à 100"}), 400)


    output = {
        "ht": ht,
        "taux": taux,
        "ttc": round(ht * (1 + (taux / 100)), 2),
    }

    return jsonify(output), 200

# ===== Route /remise =====
@app.route('/remise')
def remise():
    _prix = request.args.get('prix')
    _pourcentage = request.args.get('pourcentage')

    if _prix is None or _prix.strip() == "":
        return make_response(jsonify({"error": "Missing Prix Parameters"}), 400)
    if _pourcentage is None or _pourcentage.strip() == "":
        return make_response(jsonify({"error": "Missing Pourcentage Parameters"}), 400)

    try:
        prix = float(_prix)
        pourcentage = float(_pourcentage)
    except ValueError:
        return make_response(jsonify({"error": "Prix et pourcentage doivent etre des nombres"}), 400)

    if prix < 0:
        return make_response(jsonify({"error": "Le prix doit etre supérieur à 0"}), 400)
    if pourcentage < 0:
        return make_response(jsonify({"error": "Le pourcentage doit etre supérieur à 0"}), 400)
    if pourcentage > 100:
        return make_response(jsonify({"error": "Le pourcentage doit etre inférieur à 100"}), 400)

    prix_final = round(prix * (1 - pourcentage / 100), 2)

    output = {
        "prixInitial": prix,
        "pourcentage": pourcentage,
        "prixFinale": prix_final,
    }

    return jsonify(output), 200
