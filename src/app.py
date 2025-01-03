import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask_socketio import SocketIO
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_file, abort, render_template

from payments.pix import Pix
from repository.database import db
from db_models.payment import Payment

app = Flask(__name__)

instance_path = os.path.join(os.getcwd(), 'instance')

if not os.path.exists(instance_path):
  os.makedirs(instance_path)

app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  data = request.get_json()

  if 'value' not in data or not isinstance(data['value'], (int, float)):
    return jsonify({"message": "O campo 'value' é inválido ou ausente."}), 400

  if data['value'] <= 0:
    return jsonify({"message": "O campo 'value' deve ser maior que zero."}), 400

  expiration_date = datetime.now() + timedelta(minutes=30)

  new_payment = Payment(value=data['value'], expiration_date=expiration_date)

  pix_obj = Pix()
  data_payment_pix = pix_obj.create_payment()

  new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
  new_payment.qr_code = data_payment_pix['qr_code_path']

  db.session.add(new_payment)
  db.session.commit()

  return jsonify({
    "message": "O pagamento foi criado com sucesso.",
    "payment": new_payment.to_dict(),
    "qr_code_path": data_payment_pix['qr_code_path']
  })

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name):
  file_path = os.path.join(os.getcwd(), "src", "static", "img", f"{file_name}.png")
  
  if not os.path.exists(file_path):
    abort(404, description="Arquivo não encontrado")
  
  return send_file(file_path, mimetype='image/png')

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirmation_pix():
  data = request.get_json()

  if "bank_payment_id" not in data and "value" not in data:
    return jsonify({"message": "Dados do pagamento inválidos"}), 400

  payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

  if not payment or payment.paid:
    return jsonify({"message": "Pagamento não encontrado ou já confirmado"}), 404

  if data.get("value") != payment.value:
    return jsonify({"message": "Valor do pagamento inválido"}), 400

  payment.paid = True
  db.session.commit()
  socketio.emit('payment-confirmed', {"bank_payment_id": payment.bank_payment_id})

  return jsonify({"message": "O pagamento foi confirmado"})

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
  payment = Payment.query.get(payment_id)
    
  if payment is None:
    return render_template('404.html', payment=payment)
  
  if payment.qr_code is None:
    return jsonify({"message": "QR Code não gerado para este pagamento."}), 404

  if payment.paid:
    return render_template('confirmed_payment.html', payment=payment)
  
  host = "http://127.0.0.1:5000"
  qr_code_url = f"payments/pix/qr_code/{payment.qr_code}"

  return render_template('payment.html', payment=payment, host=host, 
                         url=qr_code_url, expiration_date=payment.expiration_date)

@socketio.on('connect')
def handle_connect():
  print("Client connected to the server")


@socketio.on('connect')
def handle_disconnect():
  print("Client has disconnected to the server")

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  socketio.run(app, debug=True)