import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from datetime import datetime, timedelta
from flask import Flask, jsonify, request
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

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  data = request.get_json()

  if 'value' not in data or not isinstance(data['value'], (int, float)):
    return jsonify({"message": "O campo 'value' é inválido ou ausente."}), 400

  if data['value'] <= 0:
    return jsonify({"message": "O campo 'value' deve ser maior que zero."}), 400

  expiration_date = datetime.now() + timedelta(minutes=30)

  new_payment = Payment(value=data['value'], expiration_date=expiration_date)

  db.session.add(new_payment)
  db.session.commit()

  return jsonify({
    "message": "O pagamento foi criado com sucesso.",
    "payment": new_payment.to_dict(),
  })


@app.route('/payments/pix/confirmation', methods=['POST'])
def confirmation_pix():
  return jsonify({"message": "The payment has been confirmed"})


@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
  return 'pagamento pix'


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)