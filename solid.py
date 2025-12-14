from abc import ABC, abstractmethod
from dataclasses import dataclass

# Model Sederhana
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# === KODE BURUK (SEBELUM REFACTOR) ===
class OrderManager:  # Melanggar SRP, OCP, DIP
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}...")

        # LOGIKA PEMBAYARAN (pelanggaran OCP/DIP)
        if payment_method == "credit_card":
            # Logika detail implementasi hardcoded di sini
            print("Processing Credit Card...")
        elif payment_method == "bank_transfer":
            # Logika detail implementasi hardcoded di sini
            print("Processing Bank Transfer...")
        else:
            print("Metode tidak valid.")
            return False

        # LOGIKA NOTIFIKASI (pelanggaran SRP)
        print(f"Mengirim notifikasi ke {order.customer_name}...")
        order.status = "paid"
        return True