# Projek Refactoring SOLID - Sistem Validasi Pendaftaran Mahasiswa

## Deskripsi Projek

Proyek ini mendemonstrasikan implementasi prinsip SOLID (SRP, OCP, DIP) pada sistem validasi pendaftaran mahasiswa dengan menggunakan abstraction (interface) dan dependency injection. Kode awalnya adalah contoh "kode buruk" yang melanggar prinsip SOLID, kemudian direfaktor menjadi desain yang lebih modular dan extensible.

## Prinsip SOLID yang Diimplementasikan

### 1. **Single Responsibility Principle (SRP)**

- Setiap kelas memiliki satu tanggung jawab khusus
- `SKSValidator`: hanya memvalidasi batas SKS
- `PrerequisiteValidator`: hanya memvalidasi prasyarat mata kuliah
- `IPKValidator`: hanya memvalidasi batas minimum IPK
- `RegistrationValidator`: hanya mengkoordinasi validator

### 2. **Open-Closed Principle (OCP)**

- Sistem terbuka untuk ekstensi, tertutup untuk modifikasi
- Menambahkan aturan validasi baru cukup dengan membuat kelas validator baru yang mengimplementasikan interface `IValidator`
- Tidak perlu mengubah kode existing di `RegistrationValidator`

### 3. **Dependency Inversion Principle (DIP)**

- Bergantung pada abstraksi (`IValidator`), bukan implementasi konkret
- Memudahkan pengujian dan pertukaran implementasi

## Struktur File

```
refactor_solid.py
├── Data Classes:
│   ├── Student: data mahasiswa (nama, kursus selesai, SKS saat ini, IPK)
│   └── Course: data mata kuliah (kode, SKS, prasyarat)
├── Contoh Kode Buruk:
│   └── ValidatorManagerBad: kelas "God" yang melanggar SOLID
├── Kode Refactor:
│   ├── IValidator: interface/abstract class untuk kontrak validator
│   ├── SKSValidator: validasi batas maksimum SKS
│   ├── PrerequisiteValidator: validasi pemenuhan prasyarat
│   ├── IPKValidator: validasi batas minimum IPK
│   └── RegistrationValidator: koordinator validator
└── main(): fungsi demonstrasi
```

## Cara Menjalankan

1. Jalankan file utama dari terminal:

```bash
python refactor_solid.py
```

## Output yang Dihasilkan

Program akan menampilkan tiga skenario:

1. **Skenario 0**: Menjalankan kode buruk sebagai perbandingan
2. **Skenario 1**: Kode refactor dengan SKS dan Prerequisite Validator
3. **Skenario 2**: Pembuktian OCP dengan menambahkan IPK Validator

## Version Control

Kode dikelola menggunakan Git. [https://github.com/hzBoydev/PBO-P12/commits/main/]