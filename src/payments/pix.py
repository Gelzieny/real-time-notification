import os
import uuid
import qrcode


class Pix:

  def __init__(self) -> None:
    self.output_dir = os.path.join("src", "static", "img")
    os.makedirs(self.output_dir, exist_ok=True)

  def create_payment(self):
    bank_payment_id = uuid.uuid4()

    hash_payment = f'hash_payment_{bank_payment_id}'

    img = qrcode.make(hash_payment)

    file_name = f"qr_code_payment_{bank_payment_id}.png"

    file_path = os.path.join(self.output_dir, file_name)

    img.save(file_path)

    qr_code_path = file_name.replace(os.sep, "/").replace(".png", "")

    return {
        "bank_payment_id": str(bank_payment_id),
        "qr_code_path": qr_code_path, 
    }