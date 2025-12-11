import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# ----------------------------
# Contoh "KODE BURUK" (God Class)
# ----------------------------
@dataclass
class Student:
    """Kelas yang merepresentasikan data mahasiswa.
    
    Attributes:
        name (str): Nama lengkap mahasiswa.
        completed_courses (List[str]): Daftar kode mata kuliah yang telah diselesaikan.
        current_sks (int): Jumlah SKS yang sedang diambil saat ini.
        ipk (float): Indeks Prestasi Kumulatif mahasiswa.
    """
    name: str
    completed_courses: List[str]
    current_sks: int
    ipk: float

@dataclass
class Course:
    """Kelas yang merepresentasikan data mata kuliah.
    
    Attributes:
        code (str): Kode mata kuliah.
        sks (int): Jumlah Satuan Kredit Semester.
        prereqs (List[str]): Daftar kode mata kuliah prasyarat yang harus dipenuhi.
    """
    code: str
    sks: int
    prereqs: List[str]

class ValidatorManagerBad:
    """
    Contoh implementasi yang melanggar prinsip SOLID.
    
    Class ini memiliki beberapa masalah:
    - SRP (Single Responsibility Principle): Memiliki banyak tanggung jawab dalam satu kelas
    - OCP (Open-Closed Principle): Sulit untuk menambah aturan validasi baru
    - DIP (Dependency Inversion Principle): Bergantung pada implementasi konkret
    
    Args:
        max_sks (int, optional): Batas maksimum SKS yang diizinkan. Defaults to 24.
    """
    
    def __init__(self, max_sks=24):
        """
        Inisialisasi ValidatorManagerBad.
        
        Args:
            max_sks (int): Batas maksimum SKS untuk validasi.
        """
        self.max_sks = max_sks

    def validate_registration(self, student: Student, course: Course) -> bool:
        """
        Memvalidasi pendaftaran mahasiswa untuk suatu mata kuliah.
        
        Method ini melakukan beberapa validasi sekaligus:
        1. Mengecek apakah penambahan SKS melebihi batas maksimum
        2. Mengecek apakah semua prasyarat telah terpenuhi
        3. Mengecek apakah IPK memenuhi batas minimum
        
        Args:
            student (Student): Data mahasiswa yang akan divalidasi.
            course (Course): Mata kuliah yang akan diambil.
            
        Returns:
            bool: True jika semua validasi berhasil, False jika salah satu gagal.
        """
        logging.info(f"[BAD] Memvalidasi pendaftaran {student.name} untuk {course.code} ...")
        
        # cek SKS
        if student.current_sks + course.sks > self.max_sks:
            logging.warning(" - Gagal: Melebihi batas SKS.")
            return False

        # cek prasyarat
        missing = [c for c in course.prereqs if c not in student.completed_courses]
        if missing:
            logging.warning(f" - Gagal: Prasyarat tidak terpenuhi: {missing}")
            return False

        # cek IPK (misal rule tambahan)
        if student.ipk < 2.5:
            logging.warning(" - Gagal: IPK di bawah batas minimal.")
            return False

        # notifikasi (hardcoded)
        logging.info(f" - Sukses: {student.name} terdaftar. Mengirim notifikasi email...")
        return True

# ----------------------------
# Refactor: SRP, OCP, DIP
# ----------------------------

# --- Abstraksi: kontrak validator ---
class IValidator(ABC):
    """
    Interface/abstract class untuk kontrak validator.
    
    Semua kelas validator harus mengimplementasikan method validate().
    Ini mengikuti Dependency Inversion Principle (DIP).
    """
    
    @abstractmethod
    def validate(self, student: Student, course: Course) -> (bool, str):
        """
        Melakukan validasi berdasarkan aturan tertentu.
        
        Args:
            student (Student): Data mahasiswa yang akan divalidasi.
            course (Course): Mata kuliah yang akan diambil.
            
        Returns:
            tuple: (bool, str) - status validasi dan pesan deskriptif.
        """
        pass

# --- Implementasi konkret (plug-in validators) ---
class SKSValidator(IValidator):
    """
    Validator untuk memeriksa batas maksimum SKS.
    
    Args:
        max_sks (int, optional): Batas maksimum SKS yang diizinkan. Defaults to 24.
    """
    
    def __init__(self, max_sks: int = 24):
        """
        Inisialisasi SKSValidator.
        
        Args:
            max_sks (int): Batas maksimum SKS untuk validasi.
        """
        self.max_sks = max_sks

    def validate(self, student: Student, course: Course):
        """
        Memvalidasi apakah penambahan SKS melebihi batas maksimum.
        
        Args:
            student (Student): Data mahasiswa yang akan divalidasi.
            course (Course): Mata kuliah yang akan diambil.
            
        Returns:
            tuple: (bool, str) - True jika valid, False jika gagal beserta pesan.
        """
        if student.current_sks + course.sks > self.max_sks:
            logging.warning(f"SKSValidator: Melebihi batas SKS (max {self.max_sks})")
            return False, f"Melebihi batas SKS (max {self.max_sks})"
        logging.info(f"SKSValidator: SKS OK")
        return True, "SKS OK"

class PrerequisiteValidator(IValidator):
    """
    Validator untuk memeriksa pemenuhan prasyarat mata kuliah.
    """
    
    def validate(self, student: Student, course: Course):
        """
        Memvalidasi apakah semua prasyarat mata kuliah telah dipenuhi.
        
        Args:
            student (Student): Data mahasiswa yang akan divalidasi.
            course (Course): Mata kuliah yang akan diambil.
            
        Returns:
            tuple: (bool, str) - True jika valid, False jika gagal beserta pesan.
        """
        missing = [c for c in course.prereqs if c not in student.completed_courses]
        if missing:
            logging.warning(f"PrerequisiteValidator: Prasyarat tidak terpenuhi: {missing}")
            return False, f"Prasyarat tidak terpenuhi: {missing}"
        logging.info(f"PrerequisiteValidator: Prasyarat OK")
        return True, "Prasyarat OK"

# Contoh validator baru: rule tambahan untuk membuktikan OCP
class IPKValidator(IValidator):
    """
    Validator untuk memeriksa batas minimum IPK.
    
    Args:
        min_ipk (float, optional): Batas minimum IPK yang diizinkan. Defaults to 2.5.
    """
    
    def __init__(self, min_ipk: float = 2.5):
        """
        Inisialisasi IPKValidator.
        
        Args:
            min_ipk (float): Batas minimum IPK untuk validasi.
        """
        self.min_ipk = min_ipk

    def validate(self, student: Student, course: Course):
        """
        Memvalidasi apakah IPK memenuhi batas minimum.
        
        Args:
            student (Student): Data mahasiswa yang akan divalidasi.
            course (Course): Mata kuliah yang akan diambil.
            
        Returns:
            tuple: (bool, str) - True jika valid, False jika gagal beserta pesan.
        """
        if student.ipk < self.min_ipk:
            logging.warning(f"IPKValidator: IPK harus >= {self.min_ipk}")
            return False, f"IPK harus >= {self.min_ipk}"
        logging.info(f"IPKValidator: IPK OK")
        return True, "IPK OK"

# --- Koordinator (Coordinator) ---
class RegistrationValidator:
    """
    Koordinator untuk mengelola eksekusi beberapa validator.
    
    Kelas ini mengikuti Single Responsibility Principle (SRP) dengan
    hanya bertanggung jawab mengkoordinasi validator, bukan mengimplementasikan
    logika validasi.
    
    Args:
        validators (List[IValidator]): Daftar validator yang akan digunakan.
    """
    
    def __init__(self, validators: List[IValidator]):
        """
        Inisialisasi RegistrationValidator.
        
        Args:
            validators (List[IValidator]): Daftar validator yang akan dijalankan.
        """
        self.validators = validators

    def validate(self, student: Student, course: Course) -> bool:
        """
        Menjalankan semua validator dan mengumpulkan hasilnya.
        
        Args:
            student (Student): Data mahasiswa yang akan divalidasi.
            course (Course): Mata kuliah yang akan diambil.
            
        Returns:
            bool: True jika semua validator berhasil, False jika ada yang gagal.
        """
        logging.info(f"[REFAC] Memvalidasi pendaftaran {student.name} untuk {course.code} ...")
        all_ok = True
        for v in self.validators:
            ok, message = v.validate(student, course)
            logging.info(f" - {v.__class__.__name__}: {message}")
            if not ok:
                all_ok = False
                # tetap lanjutkan untuk menampilkan semua pesan (atau bisa return False langsung)
        
        if all_ok:
            logging.info(" - Semua validator lulus. Daftar berhasil. Mengirim notifikasi...")
            return True
        else:
            logging.warning(" - Validasi gagal. Tidak jadi mendaftar.")
            return False

# ----------------------------
# Eksekusi & Pembuktian OCP
# ----------------------------
def main():
    """
    Fungsi utama untuk menjalankan demonstrasi sistem validasi.
    
    Menampilkan:
    1. Contoh kode buruk yang melanggar prinsip SOLID
    2. Contoh kode refactor yang mengikuti prinsip SOLID
    3. Demonstrasi Open-Closed Principle dengan menambah validator baru
    """
    # Contoh Data
    siti = Student(name="Siti", completed_courses=["IF101", "MATH101"], current_sks=15, ipk=3.0)
    udin = Student(name="Udin", completed_courses=["IF101"], current_sks=22, ipk=2.0)

    advanced_ai = Course(code="AI201", sks=3, prereqs=["IF101", "MATH101"])
    networks = Course(code="NET202", sks=3, prereqs=["IF101"])

    logging.info("\n=== Skenario 0: Menjalankan Kode Buruk (sebagai perbandingan) ===")
    bad = ValidatorManagerBad(max_sks=24)
    bad.validate_registration(siti, advanced_ai)
    bad.validate_registration(udin, networks)

    logging.info("\n=== Skenario 1: Refactor - Inject SKS + Prerequisite Validators ===")
    validators = [SKSValidator(max_sks=24), PrerequisiteValidator()]
    coord = RegistrationValidator(validators=validators)
    coord.validate(siti, advanced_ai)  # sukses
    coord.validate(udin, networks)       # gagal karena SKS atau IPK

    logging.info("\n=== Skenario 2: Pembuktian OCP - Tambah Validator baru (IPK) TANPA ubah RegistrationValidator ===")
    # Tambah validator baru cukup buat kelas baru dan inject ke dalam coordinator
    validators_with_ipk = [SKSValidator(24), PrerequisiteValidator(), IPKValidator(min_ipk=2.5)]
    coord2 = RegistrationValidator(validators=validators_with_ipk)
    coord2.validate(siti, advanced_ai)  # sukses
    coord2.validate(udin, networks)       # gagal karena IPK < 2.5

if __name__ == "__main__":
    """
    Entry point program.
    """
    main()