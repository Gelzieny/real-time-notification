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

    file_path = os.path.join(self.output_dir, f"qr_code_payment_{bank_payment_id}.png")

    img.save(file_path)

    return {
      "bank_payment_id": str(bank_payment_id),
      "qr_code_path": file_path,
    }