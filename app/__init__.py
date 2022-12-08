from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kqfkongddcfkly:b37a795817fb01a08d5fadfb3b73755e8b44768cd0b1ba9b6973e67e36448800@ec2-35-175-19-96.compute-1.amazonaws.com:5432/de0a76nqc5naub"

db=SQLAlchemy(app)

class Requisicao(db.Model):
    __tablename__= "requisicao"

    id_req = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)

class UltimaRequisicao(db.Model):
    __tablename__ = "ultima_requisicao"

    id_last_req = db.Column(db.Integer, primary_key=True)
    last_req = db.Column(db.Integer)

class Total(db.Model):
    __tablename__ = "total"
    
    id_total = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)

class Clima(db.Model):
    __tablename__ = "clima"

    id_clima = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float)
    umidade = db.Column(db.Integer)

    def __init__(self, temperatura, umidade):
        self.temperatura = temperatura
        self.umidade = umidade

db.create_all()

@app.route('/req', methods=['GET', 'POST'])
def get():
    if request.method == "POST":
        try: 
            json = request.get_json()
            valor = Requisicao(valor=float(json['valor']))
            db.session.add(valor)
            db.session.commit()
            return jsonify({'message': 'Enviado com sucesso'})
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'message' : 'Falha ao enviar'})

    if request.method == "GET":
        obj = Requisicao.query.order_by(Requisicao.id_req.desc()).limit(1).first()
        resposta = jsonify({"id_valor": obj.id_req, "valor": obj.valor})
        return resposta

@app.route('/last-req', methods=['POST', 'GET'])
def req():
    if request.method == "POST":
        json = request.get_json()
        last_req = UltimaRequisicao(last_req=int(json['last_req']))
        db.session.add(last_req)
        db.session.commit()
        return jsonify({"last_req": last_req.last_req})
    
    if request.method == "GET":
        resposta = UltimaRequisicao.query.order_by(UltimaRequisicao.id_last_req.desc()).limit(1).first()
        return jsonify({"last_req": resposta.last_req})

@app.route('/total', methods=['POST'])
def total():
    if request.method == "POST":
        json = request.get_json()
        total = Total(total=float(json["total"]))
        if Total.query.first() is None:
            db.session.add(total)
            db.session.commit()
            return jsonify({'total': total.total})
        else:
            tot_atual = Total.query.order_by(Total.id_total.desc()).first()
            novo_total = total.total + tot_atual.total
            db_total = Total(total=float(novo_total))
            db.session.add(db_total)
            db.session.commit()
            return jsonify({'total': novo_total})

@app.route('/clima', methods=['POST', 'GET'])
def clima():
    if request.method == "POST":
        json = request.get_json()
        try:
            dados = Clima(json['temperatura'], json['umidade'])
            db.session.add(dados)
            db.session.commit()
            return jsonify({'message': 'Enviado com sucesso'})
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'message': 'Falha ao enviar'})

    if request.method == "GET":
        resposta = Clima.query.order_by(Clima.id_clima.desc()).limit(1).first()
        return jsonify({'temperatura': resposta.temperatura, 'umidade': resposta.umidade})


if __name__ == "main":
    app.run(debug=True)