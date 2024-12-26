import os
import uuid
import qrcode


class Pix:

  def __init__(self) -> None:
        # Diretório onde os QR codes serão salvos
        self.output_dir = os.path.join("src", "static", "img")
        os.makedirs(self.output_dir, exist_ok=True)

  def create_payment(self):
      # Geração de um ID único para o pagamento
      bank_payment_id = uuid.uuid4()

      # Criação do hash do pagamento
      hash_payment = f'hash_payment_{bank_payment_id}'

      # Geração do QR code
      img = qrcode.make(hash_payment)

      # Nome do arquivo para o QR code
      file_name = f"qr_code_payment_{bank_payment_id}.png"

      # Caminho completo para salvar a imagem
      file_path = os.path.join(self.output_dir, file_name)

      # Salvar a imagem do QR code
      img.save(file_path)

      # Corrige o caminho para usar barras normais
      qr_code_path = file_name.replace(os.sep, "/").replace(".png", "")

      return {
          "bank_payment_id": str(bank_payment_id),
          "qr_code_path": qr_code_path,  # Caminho correto para ser salvo no banco de dados
      }