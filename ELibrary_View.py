import tkinter as tk
from tkinter import ttk, messagebox



class LibraryView:


    def __init__(self, root, controller):

        self.root = root
        self.controller = controller


        self.root.title(
            "Sistem Informasi E-Library"
        )


        self.root.geometry(
            "1000x650"
        )


        self.root.configure(
            bg="#eef6ff"
        )



        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=28
        )



        # ==========================
        # NOTEBOOK
        # ==========================


        self.tab_control = ttk.Notebook(
            root
        )


        self.tab_buku = tk.Frame(
            self.tab_control,
            bg="#eef6ff"
        )


        self.tab_anggota = tk.Frame(
            self.tab_control,
            bg="#eef6ff"
        )


        self.tab_pinjam = tk.Frame(
            self.tab_control,
            bg="#eef6ff"
        )



        self.tab_control.add(
            self.tab_buku,
            text="📚 Buku"
        )


        self.tab_control.add(
            self.tab_anggota,
            text="👤 Anggota"
        )


        self.tab_control.add(
            self.tab_pinjam,
            text="🔄 Peminjaman"
        )



        self.tab_control.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )



        self.buat_tab_buku()

        self.buat_tab_anggota()

        self.buat_tab_pinjam()




    # ==================================================
    # BUKU
    # ==================================================

    def buat_tab_buku(self):

        frame=self.tab_buku
        frame.grid_columnconfigure(2, weight=1)


        label=[
            "ID Buku",
            "Judul Buku",
            "Penulis",
            "Tahun Terbit",
            "Kategori"
        ]


        self.ent_id_buku=tk.Entry(
            frame,
            width=35
        )

        self.ent_judul=tk.Entry(
            frame,
            width=35
        )

        self.ent_penulis=tk.Entry(
            frame,
            width=35
        )

        self.ent_tahun=tk.Entry(
            frame,
            width=35
        )

        self.ent_kategori=tk.Entry(
            frame,
            width=35
        )



        entry=[
            self.ent_id_buku,
            self.ent_judul,
            self.ent_penulis,
            self.ent_tahun,
            self.ent_kategori
        ]



        for i,text in enumerate(label):

            tk.Label(
                frame,
                text=text,
                bg="#eef6ff"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=5
            )


            entry[i].grid(
                row=i,
                column=1
            )



        tombol=tk.Frame(
            frame,
            bg="#eef6ff"
        )


        tombol.grid(
            row=5,
            columnspan=2,
            pady=10
        )



        tk.Button(
    tombol,
    text="Tambah Buku",
    command=self.controller.tambah_buku,
    bg="#2196F3",
    fg="white",
    font=("Arial",10,"bold"),
    width=12
).pack(
    side="left",
    padx=5
)


        tk.Button(
    tombol,
    text="Update",
    command=self.controller.update_buku,
    bg="#FFC107",
    fg="black",
    font=("Arial",10,"bold"),
    width=12
).pack(
    side="left",
    padx=5
)


        tk.Button(
    tombol,
    text="Hapus",
    command=self.controller.hapus_buku,
    bg="#F44336",
    fg="white",
    font=("Arial",10,"bold"),
    width=12
).pack(
    side="left",
    padx=5
)


        tk.Button(
    tombol,
    text="Bersihkan",
    command=self.controller.bersihkan_form,
    bg="#E0E0E0",
    fg="black",
    font=("Arial",10,"bold"),
    width=12
).pack(
    side="left",
    padx=5
)



        kolom=(
            "ID",
            "Judul",
            "Penulis",
            "Tahun",
            "Kategori",
            "Status"
        )


        self.tabel_buku=ttk.Treeview(
            frame,
            columns=kolom,
            show="headings"
        )


        for k in kolom:

            self.tabel_buku.heading(
                k,
                text=k
            )

            self.tabel_buku.column(
    k,
    width=130,
    anchor="center"
)


        self.tabel_buku.grid(
    row=6,
    column=0,
    columnspan=3,
    sticky="nsew",
    pady=20
)


        self.tabel_buku.bind(
            "<ButtonRelease-1>",
            self.controller.pilih_buku
        )



    def get_input_buku(self):

        return(
            self.ent_id_buku.get(),
            self.ent_judul.get(),
            self.ent_penulis.get(),
            self.ent_tahun.get(),
            self.ent_kategori.get()
        )



    def isi_form_buku(
            self,
            id_buku,
            judul,
            penulis,
            tahun,
            kategori):


        self.ent_id_buku.delete(0,tk.END)
        self.ent_judul.delete(0,tk.END)
        self.ent_penulis.delete(0,tk.END)
        self.ent_tahun.delete(0,tk.END)
        self.ent_kategori.delete(0,tk.END)


        self.ent_id_buku.insert(0,id_buku)
        self.ent_judul.insert(0,judul)
        self.ent_penulis.insert(0,penulis)
        self.ent_tahun.insert(0,tahun)
        self.ent_kategori.insert(0,kategori)
            # ==================================================
    # ANGGOTA
    # ==================================================

    def buat_tab_anggota(self):

        frame=self.tab_anggota
        frame.grid_columnconfigure(2, weight=1)


        label=[
            "ID Anggota",
            "Nama",
            "Alamat",
            "No HP"
        ]


        self.ent_id_anggota=tk.Entry(
            frame,
            width=35
        )

        self.ent_nama=tk.Entry(
            frame,
            width=35
        )

        self.ent_alamat=tk.Entry(
            frame,
            width=35
        )

        self.ent_no_hp=tk.Entry(
            frame,
            width=35
        )


        entry=[
            self.ent_id_anggota,
            self.ent_nama,
            self.ent_alamat,
            self.ent_no_hp
        ]



        for i,text in enumerate(label):

            tk.Label(
                frame,
                text=text,
                bg="#eef6ff"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=5
            )


            entry[i].grid(
                row=i,
                column=1
            )



        tombol=tk.Frame(
            frame,
            bg="#eef6ff"
        )


        tombol.grid(
            row=4,
            columnspan=2,
            pady=10
        )



        tk.Button(
    tombol,
    text="Tambah Anggota",
    command=self.controller.tambah_anggota,
    bg="#2196F3",
    fg="white",
    font=("Arial",10,"bold"),
    width=12,
    height=1,
    relief="raised"
).pack(
    side="left",
    padx=5
)
        


        tk.Button(
    tombol,
    text="Update",
    command=self.controller.update_anggota,
    bg="#FFC107",
    fg="black",
    font=("Arial",10,"bold"),
    width=12,
    height=1,
    relief="raised"
).pack(
    side="left",
    padx=5
)


        tk.Button(
    tombol,
    text="Hapus",
    command=self.controller.hapus_anggota,
    bg="#F44336",
    fg="white",
    font=("Arial",10,"bold"),
    width=12,
    height=1,
    relief="raised"
).pack(
    side="left",
    padx=5
)


        tk.Button(
    tombol,
    text="Bersihkan",
    command=self.controller.bersihkan_form,
    bg="#E0E0E0",
    fg="black",
    font=("Arial",10,"bold"),
    width=12,
    height=1,
    relief="raised"
).pack(
    side="left",
    padx=5
)



        kolom=(
            "ID",
            "Nama",
            "Alamat",
            "No HP"
        )


        self.tabel_anggota=ttk.Treeview(
            frame,
            columns=kolom,
            show="headings"
        )



        for k in kolom:

            self.tabel_anggota.heading(
                k,
                text=k
            )


            self.tabel_anggota.column(
    k,
    width=130,
    anchor="center"
)



        self.tabel_anggota.grid(
    row=5,
    column=0,
    columnspan=3,
    sticky="nsew",
    pady=20
)



        self.tabel_anggota.bind(
            "<ButtonRelease-1>",
            self.controller.pilih_anggota
        )




    def get_input_anggota(self):

        return(
            self.ent_id_anggota.get(),
            self.ent_nama.get(),
            self.ent_alamat.get(),
            self.ent_no_hp.get()
        )




    def isi_form_anggota(
            self,
            id_anggota,
            nama,
            alamat,
            no_hp):


        self.ent_id_anggota.delete(0,tk.END)
        self.ent_nama.delete(0,tk.END)
        self.ent_alamat.delete(0,tk.END)
        self.ent_no_hp.delete(0,tk.END)



        self.ent_id_anggota.insert(
            0,
            id_anggota
        )

        self.ent_nama.insert(
            0,
            nama
        )

        self.ent_alamat.insert(
            0,
            alamat
        )

        self.ent_no_hp.insert(
            0,
            no_hp
        )





    # ==================================================
    # PEMINJAMAN
    # ==================================================

    def buat_tab_pinjam(self):

        frame=self.tab_pinjam
        frame.grid_columnconfigure(2, weight=1)



        label=[
            "ID Peminjaman",
            "ID Anggota",
            "ID Buku",
            "Tanggal Pinjam"
        ]



        self.ent_id_pinjam=tk.Entry(
            frame,
            width=35
        )


        self.ent_pinjam_anggota=tk.Entry(
            frame,
            width=35
        )


        self.ent_pinjam_buku=tk.Entry(
            frame,
            width=35
        )


        self.ent_tanggal_pinjam=tk.Entry(
            frame,
            width=35
        )



        entry=[
            self.ent_id_pinjam,
            self.ent_pinjam_anggota,
            self.ent_pinjam_buku,
            self.ent_tanggal_pinjam
        ]



        for i,text in enumerate(label):

            tk.Label(
                frame,
                text=text,
                bg="#eef6ff"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=5
            )


            entry[i].grid(
                row=i,
                column=1
            )



        tk.Button(
    frame,
    text="Simpan Peminjaman",
    command=self.controller.tambah_peminjaman,
    bg="#2196F3",
    fg="white",
    font=("Arial",10,"bold"),
    width=18
).grid(
            row=4,
            columnspan=2,
            pady=10
        )




        kolom=(
            "ID",
            "Anggota",
            "Buku",
            "Pinjam",
            "Batas",
            "Kembali",
            "Status",
            "Denda"
        )



        self.tabel_pinjam=ttk.Treeview(
            frame,
            columns=kolom,
            show="headings"
        )



        for k in kolom:

            self.tabel_pinjam.heading(
                k,
                text=k
            )


            self.tabel_pinjam.column(
    k,
    width=120,
    anchor="center"
)



        self.tabel_pinjam.grid(
    row=8,
    column=0,
    columnspan=3,
    sticky="nsew",
    pady=20
)



        # ==========================
        # PENGEMBALIAN
        # ==========================


        tk.Label(
            frame,
            text="ID Peminjaman Kembali",
            bg="#eef6ff"
        ).grid(
            row=5,
            column=0,
            pady=5
        )



        self.ent_id_kembali=tk.Entry(
            frame,
            width=35
        )


        self.ent_id_kembali.grid(
            row=5,
            column=1
        )



        tk.Label(
            frame,
            text="Tanggal Kembali",
            bg="#eef6ff"
        ).grid(
            row=6,
            column=0,
            pady=5
        )



        self.ent_tanggal_kembali=tk.Entry(
            frame,
            width=35
        )


        self.ent_tanggal_kembali.grid(
            row=6,
            column=1
        )



        tk.Button(
    frame,
    text="Kembalikan Buku",
    command=self.controller.pengembalian_buku,
    bg="#4CAF50",
    fg="white",
    font=("Arial",10,"bold"),
    width=18
).grid(
            row=7,
            columnspan=2,
            pady=10
        )
            # ==================================================
    # INPUT PEMINJAMAN
    # ==================================================

    def get_input_pinjam(self):

        return (

            self.ent_id_pinjam.get(),

            self.ent_pinjam_anggota.get(),

            self.ent_pinjam_buku.get(),

            self.ent_tanggal_pinjam.get()

        )



    # ==================================================
    # INPUT PENGEMBALIAN
    # ==================================================

    def get_input_kembali(self):

        return (

            self.ent_id_kembali.get(),

            self.ent_tanggal_kembali.get()

        )




    # ==================================================
    # BERSIHKAN FORM
    # ==================================================

    def bersihkan_form(self):


        daftar = [


            # Buku

            self.ent_id_buku,

            self.ent_judul,

            self.ent_penulis,

            self.ent_tahun,

            self.ent_kategori,



            # Anggota

            self.ent_id_anggota,

            self.ent_nama,

            self.ent_alamat,

            self.ent_no_hp,



            # Peminjaman

            self.ent_id_pinjam,

            self.ent_pinjam_anggota,

            self.ent_pinjam_buku,

            self.ent_tanggal_pinjam,



            # Pengembalian

            self.ent_id_kembali,

            self.ent_tanggal_kembali

        ]



        for item in daftar:

            item.delete(
                0,
                tk.END
            )





    # ==================================================
    # MESSAGE BOX
    # ==================================================

    def tampilkan_pesan(
            self,
            judul,
            pesan,
            error=False):


        if error:


            messagebox.showerror(
                judul,
                pesan
            )


        else:


            messagebox.showinfo(
                judul,
                pesan
            )
