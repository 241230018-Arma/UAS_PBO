import sqlite3

class LibraryModel:
    def __init__(self, db_name="elibrary.db"):
        self.db_name = db_name
        self.buat_tabel()

    def eksekusi_query(self, query, parameter=()):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name, timeout=10)
            cursor = conn.cursor()
            cursor.execute(query, parameter)
            conn.commit()
            return cursor.fetchall(), None
        except sqlite3.Error as e:
            return None, str(e)
        finally:
            if conn:
                conn.close()

    def buat_tabel(self):
        query_buku = """
        CREATE TABLE IF NOT EXISTS buku(
            id_buku TEXT PRIMARY KEY,
            judul TEXT NOT NULL,
            penerbit TEXT NOT NULL,
            tahun TEXT NOT NULL,
            kategori TEXT NOT NULL,
            stok INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL
        )
        """
        query_anggota = """
        CREATE TABLE IF NOT EXISTS anggota(
            id_anggota TEXT PRIMARY KEY,
            nama TEXT NOT NULL,
            alamat TEXT NOT NULL,
            no_hp TEXT NOT NULL
        )
        """
        query_peminjaman = """
        CREATE TABLE IF NOT EXISTS peminjaman(
            id_pinjam TEXT PRIMARY KEY,
            id_anggota TEXT,
            id_buku TEXT,
            tanggal_pinjam TEXT,
            batas_kembali TEXT,
            tanggal_kembali TEXT,
            status TEXT,
            denda INTEGER
        )
        """
        self.eksekusi_query(query_buku)
        self.eksekusi_query(query_anggota)
        self.eksekusi_query(query_peminjaman)

    # --- BUKU ---
    def load_buku(self):
        return self.eksekusi_query("SELECT * FROM buku")

    def tambah_buku(self, id_buku, judul, penerbit, tahun, kategori, stok):
        status = "Tersedia" if int(stok) > 0 else "Habis"
        return self.eksekusi_query(
            "INSERT INTO buku VALUES(?,?,?,?,?,?,?)",
            (id_buku, judul, penerbit, tahun, kategori, stok, status)
        )

    def update_buku(self, judul, penerbit, tahun, kategori, stok, id_buku):
        status = "Tersedia" if int(stok) > 0 else "Habis"
        return self.eksekusi_query(
            "UPDATE buku SET judul=?, penerbit=?, tahun=?, kategori=?, stok=?, status=? WHERE id_buku=?",
            (judul, penerbit, tahun, kategori, stok, status, id_buku)
        )

    def hapus_buku(self, id_buku):
        return self.eksekusi_query("DELETE FROM buku WHERE id_buku=?", (id_buku,))

    def cari_buku(self, id_buku):
        return self.eksekusi_query("SELECT * FROM buku WHERE id_buku=?", (id_buku,))

    def cek_stok_buku(self, id_buku):
        result, error = self.eksekusi_query("SELECT stok FROM buku WHERE id_buku=?", (id_buku,))
        if error or not result:
            return None
        return int(result[0][0])

    def kurangi_stok_buku(self, id_buku):
        return self.eksekusi_query(
            "UPDATE buku SET stok = stok - 1, status = CASE WHEN stok - 1 <= 0 THEN 'Habis' ELSE 'Tersedia' END WHERE id_buku=? AND stok > 0",
            (id_buku,)
        )

    def tambah_stok_buku(self, id_buku):
        return self.eksekusi_query(
            "UPDATE buku SET stok = stok + 1, status = 'Tersedia' WHERE id_buku=?",
            (id_buku,)
        )

    # --- ANGGOTA ---
    def load_anggota(self):
        return self.eksekusi_query("SELECT * FROM anggota")

    def tambah_anggota(self, id_anggota, nama, alamat, no_hp):
        return self.eksekusi_query("INSERT INTO anggota VALUES(?,?,?,?)", (id_anggota, nama, alamat, no_hp))

    def update_anggota(self, nama, alamat, no_hp, id_anggota):
        return self.eksekusi_query("UPDATE anggota SET nama=?, alamat=?, no_hp=? WHERE id_anggota=?", (nama, alamat, no_hp, id_anggota))

    def hapus_anggota(self, id_anggota):
        return self.eksekusi_query("DELETE FROM anggota WHERE id_anggota=?", (id_anggota,))

    def cari_anggota(self, id_anggota):
        return self.eksekusi_query("SELECT * FROM anggota WHERE id_anggota=?", (id_anggota,))

    # --- PEMINJAMAN ---
    def load_peminjaman(self):
        return self.eksekusi_query("SELECT * FROM peminjaman")

    def tambah_peminjaman(self, id_pinjam, id_anggota, id_buku, tanggal_pinjam, batas_kembali):
        return self.eksekusi_query(
            "INSERT INTO peminjaman VALUES(?,?,?,?,?,?,?,?)",
            (id_pinjam, id_anggota, id_buku, tanggal_pinjam, batas_kembali, "-", "Dipinjam", 0)
        )

    def cari_peminjaman(self, id_pinjam):
        return self.eksekusi_query("SELECT * FROM peminjaman WHERE id_pinjam=?", (id_pinjam,))

    def pengembalian_buku(self, id_pinjam, tanggal_kembali, denda):
        return self.eksekusi_query(
            "UPDATE peminjaman SET tanggal_kembali=?, status='Selesai', denda=? WHERE id_pinjam=?",
            (tanggal_kembali, denda, id_pinjam)
        )