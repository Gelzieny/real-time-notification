import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask import Flask, jsonify
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
  return jsonify({"message": "The payment has been created"})


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