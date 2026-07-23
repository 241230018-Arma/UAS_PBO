import tkinter as tk
from tkinter import messagebox  # <-- FIX: Import messagebox agar dialog hapus berfungsi
from datetime import datetime, timedelta
from collections import Counter
from ELibrary_Model import LibraryModel
from ELibrary_View import LibraryView

class LibraryController:
    def __init__(self, root):
        self.model = LibraryModel()
        self.view = LibraryView(root, self)
        self.id_buku_terpilih = None
        self.id_anggota_terpilih = None
        self.id_pinjam_terpilih = None
        self.tampilkan_semua_data()
        self.update_dashboard()

    def tampilkan_semua_data(self):
        self.tampilkan_buku()
        self.tampilkan_anggota()
        self.tampilkan_peminjaman()

    def update_dashboard(self):
        try:
            data_buku, _ = self.model.load_buku()
            buku_total = len(data_buku) if data_buku else 0
            
            data_anggota, _ = self.model.load_anggota()
            anggota_total = len(data_anggota) if data_anggota else 0

            data_pinjam, _ = self.model.load_peminjaman()
            peminjaman_aktif = sum(1 for p in data_pinjam if p[6] == "Dipinjam") if data_pinjam else 0
            
            total_denda = 0
            if data_pinjam:
                for p in data_pinjam:
                    if p[7]: total_denda += int(p[7])

            stats = {
                'buku_total': buku_total, 'anggota_total': anggota_total,
                'peminjaman_aktif': peminjaman_aktif, 'total_denda': total_denda
            }
            self.view.update_dashboard_stats(stats)
        except Exception as e:
            print(f"Error update dashboard: {e}")

    def tampilkan_buku(self):
        for item in self.view.tabel_buku.get_children(): self.view.tabel_buku.delete(item)
        data, error = self.model.load_buku()
        if not error and data:
            for buku in data:
                self.view.tabel_buku.insert("", tk.END, values=(buku[0], buku[1], buku[2], buku[4], buku[3], buku[5]))

    def pilih_buku(self, event):
        item = self.view.tabel_buku.selection()
        if item:
            data = self.view.tabel_buku.item(item)["values"]
            self.id_buku_terpilih = data[0]
            self.view.isi_form_buku(data[0], data[1], data[2], data[4], data[3], data[5])

    def tambah_buku(self):
        data = self.view.get_input_buku()
        if not all(data) or not data[5].isdigit():
            self.view.tampilkan_pesan("Error", "Semua field harus diisi dan Stok harus angka", True)
            return
        hasil, error = self.model.tambah_buku(*data)
        if not error:
            self.view.tampilkan_pesan("Berhasil", "Data buku berhasil ditambahkan")
            self.tampilkan_buku(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def update_buku(self):
        if not self.id_buku_terpilih:
            self.view.tampilkan_pesan("Error", "Pilih buku yang akan diupdate", True); return
        data = self.view.get_input_buku()
        if not data[5].isdigit():
            self.view.tampilkan_pesan("Error", "Stok harus berupa angka", True); return
        hasil, error = self.model.update_buku(data[1], data[2], data[3], data[4], data[5], self.id_buku_terpilih)
        if not error:
            self.view.tampilkan_pesan("Berhasil", "Data buku berhasil diperbarui")
            self.tampilkan_buku(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def hapus_buku(self):
        if not self.id_buku_terpilih:
            self.view.tampilkan_pesan("Error", "Pilih buku yang akan dihapus", True); return
        if not self.konfirmasi_aksi("Hapus Buku", "Yakin ingin menghapus buku ini?"): return
        hasil, error = self.model.hapus_buku(self.id_buku_terpilih)
        if not error:
            self.view.tampilkan_pesan("Berhasil", "Data buku berhasil dihapus")
            self.tampilkan_buku(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def tampilkan_anggota(self):
        for item in self.view.tabel_anggota.get_children(): self.view.tabel_anggota.delete(item)
        data, error = self.model.load_anggota()
        if not error and data:
            for anggota in data: self.view.tabel_anggota.insert("", tk.END, values=anggota)

    def pilih_anggota(self, event):
        item = self.view.tabel_anggota.selection()
        if item:
            data = self.view.tabel_anggota.item(item)["values"]
            self.id_anggota_terpilih = data[0]
            self.view.isi_form_anggota(*data)

    def tambah_anggota(self):
        data = self.view.get_input_anggota()
        if not all(data):
            self.view.tampilkan_pesan("Error", "Semua field harus diisi", True); return
        hasil, error = self.model.tambah_anggota(*data)
        if not error:
            self.view.tampilkan_pesan("Berhasil", "Anggota berhasil ditambahkan")
            self.tampilkan_anggota(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def update_anggota(self):
        if not self.id_anggota_terpilih:
            self.view.tampilkan_pesan("Error", "Pilih anggota yang akan diupdate", True); return
        data = self.view.get_input_anggota()
        hasil, error = self.model.update_anggota(data[1], data[2], data[3], self.id_anggota_terpilih)
        if not error:
            self.view.tampilkan_pesan("Berhasil", "Data anggota diperbarui")
            self.tampilkan_anggota(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def hapus_anggota(self):
        if not self.id_anggota_terpilih:
            self.view.tampilkan_pesan("Error", "Pilih anggota yang akan dihapus", True); return
        if not self.konfirmasi_aksi("Hapus Anggota", "Yakin ingin menghapus anggota ini?"): return
        hasil, error = self.model.hapus_anggota(self.id_anggota_terpilih)
        if not error:
            self.view.tampilkan_pesan("Berhasil", "Data anggota dihapus")
            self.tampilkan_anggota(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def tampilkan_peminjaman(self):
        for item in self.view.tabel_pinjam.get_children(): self.view.tabel_pinjam.delete(item)
        data, error = self.model.load_peminjaman()
        if not error and data:
            for pinjam in data: self.view.tabel_pinjam.insert("", tk.END, values=pinjam)

    def pilih_pinjam(self, event):
        item = self.view.tabel_pinjam.selection()
        if item:
            data = self.view.tabel_pinjam.item(item)["values"]
            self.id_pinjam_terpilih = data[0]
            self.view.ent_id_kembali.delete(0, tk.END)
            self.view.ent_id_kembali.insert(0, data[0])

    def tambah_peminjaman(self):
        data = self.view.get_input_pinjam()
        if not all(data):
            self.view.tampilkan_pesan("Error", "Semua field harus diisi", True); return
        
        stok = self.model.cek_stok_buku(data[2])
        if stok is None or stok <= 0:
            self.view.tampilkan_pesan("Error", "Buku tidak ditemukan atau stok habis", True); return
        
        anggota, error = self.model.cari_anggota(data[1])
        if error or not anggota:
            self.view.tampilkan_pesan("Error", "Anggota tidak ditemukan", True); return

        try:
            tanggal = datetime.strptime(data[3], "%Y-%m-%d")
            batas = (tanggal + timedelta(days=7)).strftime("%Y-%m-%d")
        except:
            self.view.tampilkan_pesan("Error", "Format tanggal tidak valid", True); return

        hasil, error = self.model.tambah_peminjaman(data[0], data[1], data[2], data[3], batas)
        if not error:
            self.model.kurangi_stok_buku(data[2])
            self.view.tampilkan_pesan("Berhasil", f"Peminjaman berhasil\nBatas kembali: {batas}")
            self.tampilkan_semua_data(); self.update_dashboard(); self.view.bersihkan_form()
        else:
            self.view.tampilkan_pesan("Error", error, True)

    def pengembalian_buku(self):
        data = self.view.get_input_kembali()
        if not all(data):
            self.view.tampilkan_pesan("Error", "Semua field harus diisi", True); return

        pinjam, error = self.model.cari_peminjaman(data[0])
        if error or not pinjam:
            self.view.tampilkan_pesan("Error", "Data peminjaman tidak ditemukan", True); return
        if pinjam[0][6] == "Selesai":
            self.view.tampilkan_pesan("Error", "Buku sudah dikembalikan", True); return

        try:
            batas = datetime.strptime(pinjam[0][4], "%Y-%m-%d")
            kembali = datetime.strptime(data[1], "%Y-%m-%d")
        except:
            self.view.tampilkan_pesan("Error", "Format tanggal tidak valid", True); return

        terlambat = (kembali - batas).days
        denda = terlambat * 1000 if terlambat > 0 else 0

        self.model.pengembalian_buku(data[0], data[1], denda)
        self.model.tambah_stok_buku(pinjam[0][2])
        self.view.tampilkan_pesan("Berhasil", f"Pengembalian selesai\nDenda: Rp {denda:,}")
        self.tampilkan_semua_data(); self.update_dashboard(); self.view.bersihkan_form()

    def bersihkan_form(self):
        self.view.bersihkan_form()
        self.id_buku_terpilih = self.id_anggota_terpilih = self.id_pinjam_terpilih = None

    def konfirmasi_aksi(self, judul, pesan):
        return messagebox.askyesno(judul, pesan)

if __name__ == "__main__":
    window = tk.Tk()
    app = LibraryController(window)
    window.mainloop()