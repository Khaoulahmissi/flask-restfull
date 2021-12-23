from flask import Flask, request, jsonify, make_response
from models.db import create_db
from models.compte import *
from models.transaction import  *
####### IL FAUT CREER LA BASE DE DONNEES gestion_financiere
@app.route('/comptes', methods = ['GET'])
def comptes():
    get_comptes = Compte.query.all()
    compte_schema = CompteSchema(many=True)
    comptes = compte_schema.dump(get_comptes)
    return make_response(jsonify({"comptes": comptes}))

@app.route('/comptes/<id>', methods = ['GET'])
def get_compte_by_id(id):
    get_compte = Compte.query.get(id)
    compte_schema = CompteSchema()
    compte = compte_schema.dump(get_compte)
    return make_response(jsonify({"compte": compte}))

@app.route('/comptes', methods = ['POST'])
def create_compte():
    data = request.get_json()
    compte_schema = CompteSchema()
    compte = compte_schema.load(data)
    db.session.add(compte.data)
    db.session.commit()
    #result = compte_schema.dump(compte.create())
    return make_response(jsonify({"compte": compte_schema}),200)



@app.route('/transactions', methods = ['POST'])
def create_transaction():
    data = request.get_json()
    transaction_schema = TransactionSchema()
    transaction = transaction_schema.load(data)
    result = transaction_schema.dump(transaction.create())
    return make_response(jsonify({"transaction": result}),200)



@app.route('/transactions', methods = ['GET'])
def transactions():
    get_transactions = Transaction.query.all()
    transaction_schema = TransactionSchema(many=True)
    transactions = transaction_schema.dump(get_transactions)
    return make_response(jsonify({"transactions": transactions}))

@app.route('/transactions/<id>', methods = ['GET'])
def get_transaction_by_id(id):
    get_transaction = Transaction.query.get(id)
    transaction_schema = TransactionSchema()
    transaction = transaction_schema.dump(get_transaction)
    return make_response(jsonify({"transaction": transaction}))

@app.route('/transactions/<id>', methods = ['PUT'])
def update_transaction_by_id(id):
    data = request.get_json()
    get_transaction = Transaction.query.get(id)
    if get_transaction != None:
        if data.get('description'):
            get_transaction.description = data['description']
        if data.get('compte_deb'):
            get_transaction.compte_deb = data['compte_deb']
        if data.get('compte_cred'):
            get_transaction.compte_cred = data['compte_cred']
        if data.get('date'):
            get_transaction.date = data['date']
        db.session.add(get_transaction)
        db.session.commit()
        transaction_schema = TransactionSchema()
        transaction = transaction_schema.dump(get_transaction)
        return make_response(jsonify({"transaction": transaction}))
    else:
        return make_response(jsonify({"transaction": {}}))
        
@app.route('/comptes/<id>', methods = ['PUT'])
def update_compte_by_id(id):
    data = request.get_json()
    get_compte = Compte.query.get(id)
    if data.get('libelle'):
        get_compte.libelle = data['libelle']
    if data.get('informations'):
        get_compte.informations = data['informations']
    db.session.add(get_compte)
    db.session.commit()
    compte_schema = CompteSchema(only=['id', 'libelle', 'informations'])
    compte = compte_schema.dump(get_compte)
    return make_response(jsonify({"compte": compte}))

@app.route('/comptes/<id>', methods = ['DELETE'])
def delete_compte_by_id(id):
    get_compte = Compte.query.get(id)
    db.session.delete(get_compte)
    db.session.commit()
    return make_response("",204)
@app.route('/transactions/<id>', methods = ['DELETE'])
def delete_transaction_by_id(id):
    get_transaction = Transaction.query.get(id)
    db.session.delete(get_transaction)
    db.session.commit()
    return make_response("",204)
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)