# Analisis Refactoring Kode: SOLID Principles

## Ringkasan Perubahan
Kode asli (`OrderManager`) telah direfaktor menjadi kode baru (`CheckoutService` dengan abstraksi `IPaymentProcessor` dan `INotificationService`). Berikut analisis pelanggaran dan perbaikan berdasarkan prinsip SOLID:

## 1. **Single Responsibility Principle (SRP)**

### **Sebelum Refactor - PELANGGARAN:**
```python
class OrderManager:
    def process_checkout(self, order: Order, payment_method: str):
        # LOGIKA PEMBAYARAN
        if payment_method == "credit_card":
            # ... kode pembayaran ...
        elif payment_method == "bank_transfer":
            # ... kode pembayaran ...
        
        # LOGIKA NOTIFIKASI
        print(f"Mengirim notifikasi...")
```
**Masalah:**
- `OrderManager` memiliki **multiple responsibilities**:
  1. Menangani logika pembayaran
  2. Menangani logika notifikasi
  3. Mengubah status order
- Perubahan pada salah satu tanggung jawab akan mempengaruhi seluruh kelas

### **Setelah Refactor - PERBAIKAN:**
```python
class CheckoutService:  # SRP: Hanya koordinasi checkout
    def run_checkout(self, order: Order):
        payment_success = self.payment_processor.process(order)  # Delegasi ke specialist
        if payment_success:
            self.notifier.send(order)  # Delegasi ke specialist
```

**Keuntungan:**
- `CheckoutService`: Hanya bertanggung jawab **mengkoordinasi proses checkout**
- `IPaymentProcessor`: Specialist menangani **hanya pembayaran**
- `INotificationService`: Specialist menangani **hanya notifikasi**
- Setiap kelas punya **satu alasan untuk berubah**

## 2. **Open/Closed Principle (OCP)**

### **Sebelum Refactor - PELANGGARAN:**
```python
def process_checkout(self, order: Order, payment_method: str):
    if payment_method == "credit_card":
        # ... kode credit card ...
    elif payment_method == "bank_transfer":
        # ... kode bank transfer ...
    else:
        print("Metode tidak valid.")
```
**Masalah:**
- Setiap penambahan metode pembayaran **harus memodifikasi kode yang sudah ada**
- Membutuhkan perubahan pada method `process_checkout()`
- Risiko tinggi: perubahan bisa merusak fungsi yang sudah berjalan

### **Setelah Refactor - PERBAIKAN:**
```python
# Kontrak abstrak
class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

# Implementasi konkrit
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

# PENAMBAHAN BARU - tanpa ubah kode yang ada
class QrisProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses QRIS.")
        return True
```
**Bukti OCP:**
```python
# Menambahkan QRIS TANPA mengubah CheckoutService
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)
checkout_qris.run_checkout(budi_order)  # Tetap bekerja!
```

**Keuntungan:**
- Sistem **terbuka untuk ekstensi** (bisa tambah payment processor baru)
- **Tertutup untuk modifikasi** (tidak perlu ubah `CheckoutService`)
- Dukungan untuk plugin architecture

## 3. **Dependency Inversion Principle (DIP)**

### **Sebelum Refactor - PELANGGARAN:**
```python
class OrderManager:
    def process_checkout(self, order: Order, payment_method: str):
        # KETERGANTUNGAN PADA IMPLEMENTASI KONKRIT
        if payment_method == "credit_card":
            # Hardcoded implementation
        elif payment_method == "bank_transfer":
            # Hardcoded implementation
```
**Masalah:**
- **High-level module** (`OrderManager`) bergantung pada **low-level details**
- **Coupling tinggi**: `OrderManager` tahu detail implementasi setiap payment method
- **Tidak bisa di-test** dengan mudah (dependency hardcoded)

### **Setelah Refactor - PERBAIKAN:**
```python
# Abstraksi (high-level)
class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

# Implementasi (low-level) bergantung pada abstraksi
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        # ... implementasi spesifik ...

# High-level module bergantung pada abstraksi
class CheckoutService:
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        self.payment_processor = payment_processor  # Dependency Injection
        self.notifier = notifier
```
**Keuntungan:**
- **Dependency Injection**: Dependency disuntikkan dari luar
- **Bergantung pada abstraksi**: `CheckoutService` hanya tahu interface `IPaymentProcessor`
- **Inversi kontrol**: Low-level modules mengikuti kontrak high-level modules
- **Mudah di-test**: Bisa inject mock objects
- **Decoupling**: Bisa ganti implementasi tanpa mengubah client code

## **Kesimpulan Perbaikan**

| Prinsip | Sebelum | Setelah | Manfaat |
|---------|---------|---------|---------|
| **SRP** | Satu kelas banyak tanggung jawab | Setiap kelas satu tanggung jawab | Maintenance lebih mudah, perubahan terisolasi |
| **OCP** | Harus modifikasi untuk tambah fitur | Cukup extend untuk tambah fitur | Ekstensibilitas tinggi, risiko perubahan rendah |
| **DIP** | High-level tergantung low-level | Bergantung pada abstraksi | Decoupling, testability, flexibility |
