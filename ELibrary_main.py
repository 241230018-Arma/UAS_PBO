import tkinter as tk
from datetime import datetime, timedelta

from ELibrary_Model import LibraryModel
from ELibrary_View import LibraryView



class LibraryController:


    def __init__(self, root):

        self.model = LibraryModel()

        self.view = LibraryView(
            root,
            self
        )


        self.id_buku_terpilih = None
        self.id_anggota_terpilih = None


        self.tampilkan_semua_data()



    def tampilkan_semua_data(self):

        self.tampilkan_buku()
        self.tampilkan_anggota()
        self.tampilkan_peminjaman()



    # =================================
    # BUKU
    # =================================


    def tampilkan_buku(self):

        for item in self.view.tabel_buku.get_children():

            self.view.tabel_buku.delete(item)



        data,error = self.model.load_buku()



        if error:

            self.view.tampilkan_pesan(
                "Error",
                error,
                True
            )


        else:

            for buku in data:

                self.view.tabel_buku.insert(
                    "",
                    tk.END,
                    values=buku
                )




    def pilih_buku(self,event):

        item=self.view.tabel_buku.selection()


        if item:

            data=self.view.tabel_buku.item(item)["values"]


            self.id_buku_terpilih=data[0]


            self.view.isi_form_buku(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4]
            )




    def tambah_buku(self):

        data=self.view.get_input_buku()


        hasil,error=self.model.tambah_buku(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4]
        )


        if not error:

            self.view.tampilkan_pesan(
                "Berhasil",
                "Data buku berhasil ditambahkan"
            )

            self.tampilkan_buku()
            self.bersihkan_form()


        else:

            self.view.tampilkan_pesan(
                "Error",
                error,
                True
            )




    def update_buku(self):

        if self.id_buku_terpilih is None:
            return


        data=self.view.get_input_buku()


        hasil,error=self.model.update_buku(
            data[1],
            data[2],
            data[3],
            data[4],
            self.id_buku_terpilih
        )


        if not error:

            self.view.tampilkan_pesan(
                "Berhasil",
                "Data buku berhasil diperbarui"
            )


            self.tampilkan_buku()
            self.bersihkan_form()




    def hapus_buku(self):

        if self.id_buku_terpilih is None:
            return


        hasil,error=self.model.hapus_buku(
            self.id_buku_terpilih
        )


        if not error:

            self.view.tampilkan_pesan(
                "Berhasil",
                "Data buku berhasil dihapus"
            )


            self.tampilkan_buku()
            self.bersihkan_form()





    # =================================
    # ANGGOTA
    # =================================


    def tampilkan_anggota(self):

        for item in self.view.tabel_anggota.get_children():

            self.view.tabel_anggota.delete(item)



        data,error=self.model.load_anggota()



        if error:

            self.view.tampilkan_pesan(
                "Error",
                error,
                True
            )


        else:

            for anggota in data:

                self.view.tabel_anggota.insert(
                    "",
                    tk.END,
                    values=anggota
                )




    def pilih_anggota(self,event):

        item=self.view.tabel_anggota.selection()


        if item:

            data=self.view.tabel_anggota.item(item)["values"]


            self.id_anggota_terpilih=data[0]


            self.view.isi_form_anggota(
                data[0],
                data[1],
                data[2],
                data[3]
            )




    def tambah_anggota(self):

        data=self.view.get_input_anggota()


        hasil,error=self.model.tambah_anggota(
            data[0],
            data[1],
            data[2],
            data[3]
        )


        if not error:

            self.view.tampilkan_pesan(
                "Berhasil",
                "Anggota berhasil ditambahkan"
            )


            self.tampilkan_anggota()
            self.bersihkan_form()


        else:

            self.view.tampilkan_pesan(
                "Error",
                error,
                True
            )




    def update_anggota(self):

        if self.id_anggota_terpilih is None:
            return


        data=self.view.get_input_anggota()


        hasil,error=self.model.update_anggota(
            data[1],
            data[2],
            data[3],
            self.id_anggota_terpilih
        )


        if not error:

            self.view.tampilkan_pesan(
                "Berhasil",
                "Data anggota diperbarui"
            )


            self.tampilkan_anggota()
            self.bersihkan_form()




    def hapus_anggota(self):

        if self.id_anggota_terpilih is None:
            return


        hasil,error=self.model.hapus_anggota(
            self.id_anggota_terpilih
        )


        if not error:

            self.view.tampilkan_pesan(
                "Berhasil",
                "Data anggota dihapus"
            )


            self.tampilkan_anggota()
            self.bersihkan_form()





    # =================================
    # PEMINJAMAN
    # =================================


    def tampilkan_peminjaman(self):

        for item in self.view.tabel_pinjam.get_children():

            self.view.tabel_pinjam.delete(item)



        data,error=self.model.load_peminjaman()



        if error:

            self.view.tampilkan_pesan(
                "Error",
                error,
                True
            )


        else:

            for pinjam in data:

                self.view.tabel_pinjam.insert(
                    "",
                    tk.END,
                    values=pinjam
                )




    def tambah_peminjaman(self):

        data=self.view.get_input_pinjam()


        try:

            tanggal=datetime.strptime(
                data[3],
                "%d-%m-%Y"
            )


            batas=tanggal+timedelta(days=7)


            batas=batas.strftime(
                "%d-%m-%Y"
            )


        except:

            self.view.tampilkan_pesan(
                "Error",
                "Format tanggal harus DD-MM-YYYY",
                True
            )

            return



        hasil,error=self.model.tambah_peminjaman(
            data[0],
            data[1],
            data[2],
            data[3],
            batas
        )



        if not error:


            self.model.ubah_status_buku(
                data[2],
                "Dipinjam"
            )


            self.view.tampilkan_pesan(
                "Berhasil",
                "Peminjaman berhasil\nBatas kembali : "+batas
            )


            self.tampilkan_semua_data()

            self.bersihkan_form()




    def pengembalian_buku(self):

        data=self.view.get_input_kembali()


        pinjam,error=self.model.cari_peminjaman(
            data[0]
        )


        if error or not pinjam:

            self.view.tampilkan_pesan(
                "Error",
                "Data peminjaman tidak ditemukan",
                True
            )

            return



        batas=datetime.strptime(
            pinjam[0][4],
            "%d-%m-%Y"
        )


        kembali=datetime.strptime(
            data[1],
            "%d-%m-%Y"
        )


        terlambat=(kembali-batas).days



        if terlambat > 0:

            denda=terlambat*1000

        else:

            denda=0



        self.model.pengembalian_buku(
            data[0],
            data[1],
            denda
        )


        self.model.ubah_status_buku(
            pinjam[0][2],
            "Tersedia"
        )


        self.view.tampilkan_pesan(
            "Berhasil",
            f"Pengembalian selesai\nDenda: Rp {denda}"
        )


        self.tampilkan_semua_data()




    def bersihkan_form(self):

        self.view.bersihkan_form()


        self.id_buku_terpilih=None

        self.id_anggota_terpilih=None





window=tk.Tk()

app=LibraryController(window)

window.mainloop()
