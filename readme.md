# 🌐 CubDomain Mass Domain Grabber

Fast and reliable tool to scrape registered domain lists from CubDomain.com with parallel processing support.

**Tool untuk mengambil daftar domain terdaftar dari CubDomain.com dengan dukungan parallel processing yang cepat.**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-pengodehandal-181717?logo=github)](https://github.com/pengodehandal/)

---

## 📑 Table of Contents / Daftar Isi

- [English Version](#english-version)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Examples](#examples)
- [Versi Indonesia](#versi-indonesia)
  - [Fitur](#fitur)
  - [Persyaratan](#persyaratan)
  - [Instalasi](#instalasi)
  - [Cara Penggunaan](#cara-penggunaan)
  - [Contoh Penggunaan](#contoh-penggunaan)

---

# English Version

## ✨ Features

- 🚀 **Fast Parallel Processing** - Grab multiple pages simultaneously
- 📅 **Auto Date Detection** - Automatically detects available date ranges
- 🎯 **Two Grabbing Modes**:
  - Single Date: Grab domains from one specific date
  - Date Range: Grab domains from multiple dates
- ⚡ **Speed Options** - Choose between sequential or parallel mode
- 🔍 **Smart Filtering** - Auto-skip dates with no data
- 💾 **Custom Output** - Choose your own output filename
- 📊 **Progress Tracking** - Real-time progress updates per page
- 🛡️ **Reliable** - Built-in error handling and retry mechanisms

## 📋 Requirements

- Python 3.8 or higher
- Internet connection
- Windows, Linux, or macOS

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/pengodehandal/cubdomain-grabber.git
cd cubdomain-grabber
```

### 2. Install dependencies

```bash
pip install playwright
```

### 3. Install Playwright browsers

```bash
playwright install chromium
```

**That's it! You're ready to go.**

## 🚀 Usage

### Run the tool

```bash
python grabber_final.py
```

### Step-by-Step Guide

#### **Step 1: Mode Selection**

Choose between two modes:

```
[1] Single Date Grabbing
    → Grab domains from one specific date

[2] Date Range Grabbing
    → Grab domains from multiple dates
```

#### **Step 2: Enter Date(s)**

**Mode 1 - Single Date:**
```
Enter date (YYYY-MM-DD) [2025-08-14]: 2025-08-03
```

**Mode 2 - Date Range:**
```
Start date (YYYY-MM-DD) [2017-06-30]: 2025-01-01
End date (YYYY-MM-DD) [2025-08-14]: 2025-01-10
```

#### **Step 3: Configure Options**

```
Grab all pages? (y/n): y
Use parallel mode (faster)? (y/n): y
Number of threads [5]: 10
Output filename [domains_2025-08-03.txt]: mydomains.txt
```

#### **Step 4: Wait for Completion**

The tool will automatically:
- ✅ Detect total pages available
- ✅ Skip dates with no data
- ✅ Save domains to your specified file
- ✅ Show real-time progress

## 💡 Examples

### Example 1: Grab Single Date (All Pages)

```bash
→ Select mode [1/2]: 1
Enter date (YYYY-MM-DD): 2025-08-03
Grab all 781 pages? (y/n): y
Use parallel mode? (y/n): y
Number of threads [5]: 10
Output filename: domains_aug03.txt
```

**Result:** All domains from 2025-08-03 saved to `domains_aug03.txt`

### Example 2: Grab Date Range (First Page Only)

```bash
→ Select mode [1/2]: 2
Start date (YYYY-MM-DD): 2025-08-01
End date (YYYY-MM-DD): 2025-08-10
Grab all pages for each date? (y/n): n
Use parallel mode? (y/n): y
Number of threads [5]: 5
Output filename: august_week1.txt
```

**Result:** First page of domains from Aug 1-10 saved to `august_week1.txt`

### Example 3: Sequential Mode (Slower but More Reliable)

```bash
→ Select mode [1/2]: 1
Enter date (YYYY-MM-DD): 2025-08-03
Grab all 781 pages? (y/n): n
Start page: 1
End page: 10
Use parallel mode? (y/n): n
Output filename: test.txt
```

**Result:** Pages 1-10 grabbed sequentially, saved to `test.txt`

## ⚙️ Configuration Tips

### Speed vs Reliability

| Mode | Speed | Reliability | Recommended For |
|------|-------|-------------|----------------|
| **Sequential** | 🐢 Slow | ⭐⭐⭐⭐⭐ | Small jobs, unstable connection |
| **Parallel (5 threads)** | 🚀 Fast | ⭐⭐⭐⭐ | Balanced performance |
| **Parallel (10+ threads)** | ⚡ Very Fast | ⭐⭐⭐ | Large jobs, stable connection |

### Recommended Settings

- **Small job (1-10 pages)**: Sequential mode
- **Medium job (10-100 pages)**: Parallel with 5 threads
- **Large job (100+ pages)**: Parallel with 10 threads
- **Massive job (500+ pages)**: Parallel with 10-15 threads

## 📊 Output Format

Domains are saved in plain text format, one per line:

```
0-1.pl
0-1products.com
0-23.cn
0-32.pl
0-9-0.cn
...
```

## ⚠️ Disclaimer

- Use this tool responsibly
- Respect the website's Terms of Service
- Don't overload the server with too many requests
- For educational and research purposes only

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Created by:** [pengodehandal](https://github.com/pengodehandal/)

---

# Versi Indonesia

## ✨ Fitur

- 🚀 **Parallel Processing Cepat** - Ambil beberapa halaman secara bersamaan
- 📅 **Deteksi Tanggal Otomatis** - Mendeteksi rentang tanggal yang tersedia secara otomatis
- 🎯 **Dua Mode Pengambilan**:
  - Tanggal Tunggal: Ambil domain dari satu tanggal spesifik
  - Rentang Tanggal: Ambil domain dari beberapa tanggal
- ⚡ **Pilihan Kecepatan** - Pilih antara mode sequential atau parallel
- 🔍 **Filter Pintar** - Otomatis skip tanggal yang tidak ada data
- 💾 **Output Custom** - Pilih nama file output sendiri
- 📊 **Tracking Progress** - Update progress real-time per halaman
- 🛡️ **Handal** - Dengan error handling dan retry mechanism

## 📋 Persyaratan

- Python 3.8 atau lebih tinggi
- Koneksi internet
- Windows, Linux, atau macOS

## 🔧 Instalasi

### 1. Clone repository

```bash
git clone https://github.com/pengodehandal/cubdomain-grabber.git
cd cubdomain-grabber
```

### 2. Install dependencies

```bash
pip install playwright
```

### 3. Install browser Playwright

```bash
playwright install chromium
```

**Selesai! Siap digunakan.**

## 🚀 Cara Penggunaan

### Jalankan tool

```bash
python grabber_final.py
```

### Panduan Step-by-Step

#### **Langkah 1: Pilih Mode**

Pilih salah satu dari dua mode:

```
[1] Single Date Grabbing
    → Ambil domain dari satu tanggal spesifik

[2] Date Range Grabbing
    → Ambil domain dari beberapa tanggal
```

#### **Langkah 2: Masukkan Tanggal**

**Mode 1 - Tanggal Tunggal:**
```
Enter date (YYYY-MM-DD) [2025-08-14]: 2025-08-03
```

**Mode 2 - Rentang Tanggal:**
```
Start date (YYYY-MM-DD) [2017-06-30]: 2025-01-01
End date (YYYY-MM-DD) [2025-08-14]: 2025-01-10
```

#### **Langkah 3: Konfigurasi Opsi**

```
Grab all pages? (y/n): y
Use parallel mode (faster)? (y/n): y
Number of threads [5]: 10
Output filename [domains_2025-08-03.txt]: domain_saya.txt
```

#### **Langkah 4: Tunggu Selesai**

Tool akan otomatis:
- ✅ Deteksi total halaman yang tersedia
- ✅ Skip tanggal yang tidak ada data
- ✅ Simpan domain ke file yang sudah ditentukan
- ✅ Tampilkan progress real-time

## 💡 Contoh Penggunaan

### Contoh 1: Ambil Tanggal Tunggal (Semua Halaman)

```bash
→ Select mode [1/2]: 1
Enter date (YYYY-MM-DD): 2025-08-03
Grab all 781 pages? (y/n): y
Use parallel mode? (y/n): y
Number of threads [5]: 10
Output filename: domain_agustus03.txt
```

**Hasil:** Semua domain dari 2025-08-03 tersimpan di `domain_agustus03.txt`

### Contoh 2: Ambil Rentang Tanggal (Halaman Pertama Saja)

```bash
→ Select mode [1/2]: 2
Start date (YYYY-MM-DD): 2025-08-01
End date (YYYY-MM-DD): 2025-08-10
Grab all pages for each date? (y/n): n
Use parallel mode? (y/n): y
Number of threads [5]: 5
Output filename: agustus_minggu1.txt
```

**Hasil:** Halaman pertama domain dari 1-10 Agustus tersimpan di `agustus_minggu1.txt`

### Contoh 3: Mode Sequential (Lebih Lambat tapi Lebih Aman)

```bash
→ Select mode [1/2]: 1
Enter date (YYYY-MM-DD): 2025-08-03
Grab all 781 pages? (y/n): n
Start page: 1
End page: 10
Use parallel mode? (y/n): n
Output filename: test.txt
```

**Hasil:** Halaman 1-10 diambil secara berurutan, tersimpan di `test.txt`

## ⚙️ Tips Konfigurasi

### Kecepatan vs Keandalan

| Mode | Kecepatan | Keandalan | Direkomendasikan Untuk |
|------|-----------|-----------|------------------------|
| **Sequential** | 🐢 Lambat | ⭐⭐⭐⭐⭐ | Pekerjaan kecil, koneksi tidak stabil |
| **Parallel (5 thread)** | 🚀 Cepat | ⭐⭐⭐⭐ | Performa seimbang |
| **Parallel (10+ thread)** | ⚡ Sangat Cepat | ⭐⭐⭐ | Pekerjaan besar, koneksi stabil |

### Pengaturan yang Direkomendasikan

- **Pekerjaan kecil (1-10 halaman)**: Mode sequential
- **Pekerjaan menengah (10-100 halaman)**: Parallel dengan 5 thread
- **Pekerjaan besar (100+ halaman)**: Parallel dengan 10 thread
- **Pekerjaan masif (500+ halaman)**: Parallel dengan 10-15 thread

## 📊 Format Output

Domain disimpan dalam format text biasa, satu per baris:

```
0-1.pl
0-1products.com
0-23.cn
0-32.pl
0-9-0.cn
...
```

## ⚠️ Disclaimer

- Gunakan tool ini dengan bijak
- Hormati Terms of Service dari website
- Jangan overload server dengan terlalu banyak request
- Hanya untuk tujuan edukasi dan riset

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:
- Laporkan bug
- Sarankan fitur baru
- Submit pull request

## 📝 Lisensi

Project ini dilisensikan under MIT License.

## 👤 Pembuat

**Dibuat oleh:** [pengodehandal](https://github.com/pengodehandal/)

---

## 🆘 Troubleshooting

### Common Issues / Masalah Umum

**Problem:** `playwright not found`
```bash
# Solution:
pip install playwright
playwright install chromium
```

**Problem:** No domains grabbed / Tidak ada domain yang diambil
```bash
# Solution:
# Try sequential mode instead of parallel
# Increase wait time if needed
```

**Problem:** Too slow / Terlalu lambat
```bash
# Solution:
# Use parallel mode with more threads
# Grab only first page of each date
```

## 📞 Support

If you have questions or need help:
- Open an issue on GitHub
- Check existing issues first

Jika ada pertanyaan atau butuh bantuan:
- Buka issue di GitHub
- Cek issue yang sudah ada terlebih dahulu

---

**⭐ If you find this useful, please give it a star!**

**⭐ Jika tool ini berguna, mohon berikan bintang!**
