import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class LibraryView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Sistem Informasi Manajemen E-Library")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 680)
        self.center_window()

        self.colors = {
            'sidebar': '#1e293b', 'sidebar_btn': '#334155', 'sidebar_active': '#3b82f6',
            'bg': '#f8fafc', 'card': '#ffffff', 'primary': '#3b82f6', 'success': '#10b981',
            'warning': '#f59e0b', 'danger': '#ef4444', 'text_dark': '#0f172a',
            'text_muted': '#64748b', 'border': '#e2e8f0'
        }
        self.val_number_cmd = self.root.register(self.validate_only_numbers)
        self.setup_styles()
        self.create_main_layout()

    def center_window(self):
        self.root.update_idletasks()
        w, h = 1280, 780
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def validate_only_numbers(self, char):
        return char.isdigit() or char == ""

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', rowheight=38, background=self.colors['card'], fieldbackground=self.colors['card'], foreground=self.colors['text_dark'], font=('Segoe UI', 10), borderwidth=0)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#f1f5f9', foreground=self.colors['text_dark'], relief='flat', borderwidth=0)
        style.map('Treeview', background=[('selected', self.colors['primary'])], foreground=[('selected', 'white')])
        style.configure("Vertical.TScrollbar", gripcount=0, background=self.colors['border'], troughcolor=self.colors['bg'], arrowcolor=self.colors['text_muted'])

    def bind_mousewheel(self, treeview):
        def _on_mousewheel(event):
            treeview.yview_scroll(int(-1 * (event.delta / 120)), "units")
        treeview.bind("<MouseWheel>", _on_mousewheel)

    def create_main_layout(self):
        self.sidebar = tk.Frame(self.root, bg=self.colors['sidebar'], width=240)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        brand_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        brand_frame.pack(fill='x', padx=20, pady=(25, 30))
        tk.Label(brand_frame, text="📚 E-Library", font=('Segoe UI', 18, 'bold'), bg=self.colors['sidebar'], fg='white').pack(anchor='w')
        tk.Label(brand_frame, text="Management System v1.0", font=('Segoe UI', 9), bg=self.colors['sidebar'], fg=self.colors['text_muted']).pack(anchor='w')

        self.nav_buttons = {}
        for key, text in [("dashboard", "📊  Dashboard"), ("buku", "📖  Kelola Buku"), ("anggota", "👥  Kelola Anggota"), ("pinjam", "🔄  Transaksi")]:
            btn = tk.Button(self.sidebar, text=text, font=('Segoe UI', 11, 'bold'), bg=self.colors['sidebar'], fg='#94a3b8', activebackground=self.colors['sidebar_btn'], activeforeground='white', bd=0, anchor='w', padx=20, pady=12, cursor='hand2', command=lambda k=key: self.switch_tab(k))
            btn.pack(fill='x', padx=10, pady=3)
            self.nav_buttons[key] = btn

        self.content_area = tk.Frame(self.root, bg=self.colors['bg'])
        self.content_area.pack(side='right', fill='both', expand=True)

        self.pages = {k: tk.Frame(self.content_area, bg=self.colors['bg']) for k in ["dashboard", "buku", "anggota", "pinjam"]}
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky='nsew')
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.buat_tab_dashboard()
        self.buat_tab_buku()
        self.buat_tab_anggota()
        self.buat_tab_pinjam()
        self.switch_tab("dashboard")

    def switch_tab(self, page_key):
        self.pages[page_key].tkraise()
        for key, btn in self.nav_buttons.items():
            btn.config(bg=self.colors['sidebar_active'] if key == page_key else self.colors['sidebar'], fg='white' if key == page_key else '#94a3b8')

    def create_header(self, parent, title, subtitle):
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', padx=35, pady=(25, 15))
        tk.Label(header_frame, text=title, font=('Segoe UI', 20, 'bold'), bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w')
        tk.Label(header_frame, text=subtitle, font=('Segoe UI', 10), bg=self.colors['bg'], fg=self.colors['text_muted']).pack(anchor='w')

    def create_btn(self, parent, text, bg_color, command, width=15):
        return tk.Button(parent, text=text, font=('Segoe UI', 10, 'bold'), bg=bg_color, fg='white', activebackground=bg_color, activeforeground='white', bd=0, relief='flat', padx=15, pady=8, cursor='hand2', command=command, width=width)

    def create_form_field(self, parent, label_text, attr_name, only_numbers=False):
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(fill='x', pady=6)
        tk.Label(frame, text=label_text, font=('Segoe UI', 9, 'bold'), bg=self.colors['card'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 4))
        entry = tk.Entry(frame, font=('Segoe UI', 10), bg='#f8fafc', fg=self.colors['text_dark'], relief='flat', bd=1, highlightthickness=1, highlightbackground=self.colors['border'], highlightcolor=self.colors['primary'], validate="key", validatecommand=(self.val_number_cmd, '%P')) if only_numbers else tk.Entry(frame, font=('Segoe UI', 10), bg='#f8fafc', fg=self.colors['text_dark'], relief='flat', bd=1, highlightthickness=1, highlightbackground=self.colors['border'], highlightcolor=self.colors['primary'])
        entry.pack(fill='x', ipady=7, ipadx=8)
        setattr(self, attr_name, entry)

    def buat_tab_dashboard(self):
        page = self.pages['dashboard']
        self.create_header(page, "Dashboard Ringkasan", "Selamat datang di Sistem Manajemen Perpustakaan")
        stats_frame = tk.Frame(page, bg=self.colors['bg'])
        stats_frame.pack(fill='x', padx=35, pady=10)
        self.create_stat_card(stats_frame, "Total Buku", "buku_total", "📚", self.colors['primary'], 0)
        self.create_stat_card(stats_frame, "Total Anggota", "anggota_total", "👥", self.colors['success'], 1)
        self.create_stat_card(stats_frame, "Peminjaman Aktif", "peminjaman_aktif", "⏳", self.colors['warning'], 2)
        self.create_stat_card(stats_frame, "Total Denda", "total_denda", "💰", self.colors['danger'], 3)

    def create_stat_card(self, parent, title, var_name, icon, color, col):
        card = tk.Frame(parent, bg=self.colors['card'], bd=1, relief='solid', highlightthickness=0)
        card.config(highlightbackground=self.colors['border'])
        card.grid(row=0, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        tk.Frame(card, bg=color, height=4).pack(fill='x')
        content = tk.Frame(card, bg=self.colors['card'], padx=20, pady=20)
        content.pack(fill='both', expand=True)
        top_row = tk.Frame(content, bg=self.colors['card'])
        top_row.pack(fill='x')
        tk.Label(top_row, text=title, font=('Segoe UI', 10, 'bold'), bg=self.colors['card'], fg=self.colors['text_muted']).pack(side='left')
        tk.Label(top_row, text=icon, font=('Segoe UI', 16), bg=self.colors['card']).pack(side='right')
        val_label = tk.Label(content, text="0", font=('Segoe UI', 24, 'bold'), bg=self.colors['card'], fg=self.colors['text_dark'])
        val_label.pack(anchor='w', pady=(10, 0))
        setattr(self, f"stat_{var_name}", val_label)

    def buat_tab_buku(self):
        page = self.pages['buku']
        self.create_header(page, "Kelola Katalog Buku", "Tambah, ubah, dan hapus koleksi buku perpustakaan")
        main_container = tk.Frame(page, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=35, pady=(0, 20))
        form_card = tk.Frame(main_container, bg=self.colors['card'], padx=20, pady=20)
        form_card.pack(fill='x', pady=(0, 15))
        grid_form = tk.Frame(form_card, bg=self.colors['card'])
        grid_form.pack(fill='x')
        col1 = tk.Frame(grid_form, bg=self.colors['card'])
        col1.grid(row=0, column=0, sticky='ew', padx=(0, 15))
        col2 = tk.Frame(grid_form, bg=self.colors['card'])
        col2.grid(row=0, column=1, sticky='ew', padx=(15, 0))
        grid_form.grid_columnconfigure(0, weight=1)
        grid_form.grid_columnconfigure(1, weight=1)

        self.create_form_field(col1, "ID Buku", "ent_id_buku")
        self.create_form_field(col1, "Judul Buku", "ent_judul")
        self.create_form_field(col1, "Penerbit", "ent_penerbit")
        self.create_form_field(col2, "Tahun Terbit", "ent_tahun", only_numbers=True)
        self.create_form_field(col2, "Kategori", "ent_kategori")
        self.create_form_field(col2, "Jumlah Stok", "ent_stok", only_numbers=True)

        btn_bar = tk.Frame(form_card, bg=self.colors['card'])
        btn_bar.pack(fill='x', pady=(15, 0))
        self.create_btn(btn_bar, "➕ Tambah", self.colors['success'], self.controller.tambah_buku).pack(side='left', padx=(0, 8))
        self.create_btn(btn_bar, "✏️ Edit", self.colors['warning'], self.controller.update_buku).pack(side='left', padx=8)
        self.create_btn(btn_bar, "🗑️ Hapus", self.colors['danger'], self.controller.hapus_buku).pack(side='left', padx=8)
        self.create_btn(btn_bar, "🔄 Reset", self.colors['text_muted'], self.controller.bersihkan_form).pack(side='left', padx=8)

        table_card = tk.Frame(main_container, bg=self.colors['card'], padx=15, pady=15)
        table_card.pack(fill='both', expand=True)
        columns = ("ID Buku", "Judul Buku", "Penerbit", "Kategori", "Tahun", "Stok")
        self.tabel_buku = ttk.Treeview(table_card, columns=columns, show="headings")
        for col in columns:
            self.tabel_buku.heading(col, text=col)
            self.tabel_buku.column(col, width=120, anchor="center")
        self.tabel_buku.column("Judul Buku", width=280, anchor="w")
        self.tabel_buku.column("Penerbit", width=180, anchor="w")
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tabel_buku.yview, style="Vertical.TScrollbar")
        self.tabel_buku.configure(yscrollcommand=scrollbar.set)
        self.tabel_buku.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.bind_mousewheel(self.tabel_buku)
        self.tabel_buku.bind("<ButtonRelease-1>", self.controller.pilih_buku)

    def buat_tab_anggota(self):
        page = self.pages['anggota']
        self.create_header(page, "Kelola Data Anggota", "Manajemen pendaftaran dan data anggota perpustakaan")
        main_container = tk.Frame(page, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=35, pady=(0, 20))
        form_card = tk.Frame(main_container, bg=self.colors['card'], padx=20, pady=20)
        form_card.pack(fill='x', pady=(0, 15))
        grid_form = tk.Frame(form_card, bg=self.colors['card'])
        grid_form.pack(fill='x')
        col1 = tk.Frame(grid_form, bg=self.colors['card'])
        col1.grid(row=0, column=0, sticky='ew', padx=(0, 15))
        col2 = tk.Frame(grid_form, bg=self.colors['card'])
        col2.grid(row=0, column=1, sticky='ew', padx=(15, 0))
        grid_form.grid_columnconfigure(0, weight=1)
        grid_form.grid_columnconfigure(1, weight=1)

        self.create_form_field(col1, "ID Anggota", "ent_id_anggota")
        self.create_form_field(col1, "Nama Lengkap", "ent_nama")
        self.create_form_field(col2, "Alamat", "ent_alamat")
        self.create_form_field(col2, "No HP", "ent_no_hp", only_numbers=True)

        btn_bar = tk.Frame(form_card, bg=self.colors['card'])
        btn_bar.pack(fill='x', pady=(15, 0))
        self.create_btn(btn_bar, "➕ Tambah", self.colors['success'], self.controller.tambah_anggota).pack(side='left', padx=(0, 8))
        self.create_btn(btn_bar, "✏️ Edit", self.colors['warning'], self.controller.update_anggota).pack(side='left', padx=8)
        self.create_btn(btn_bar, "🗑️ Hapus", self.colors['danger'], self.controller.hapus_anggota).pack(side='left', padx=8)
        self.create_btn(btn_bar, "🔄 Reset", self.colors['text_muted'], self.controller.bersihkan_form).pack(side='left', padx=8)

        table_card = tk.Frame(main_container, bg=self.colors['card'], padx=15, pady=15)
        table_card.pack(fill='both', expand=True)
        columns = ("ID Anggota", "Nama", "Alamat", "No HP")
        self.tabel_anggota = ttk.Treeview(table_card, columns=columns, show="headings")
        for col in columns:
            self.tabel_anggota.heading(col, text=col)
            self.tabel_anggota.column(col, width=150, anchor="center")
        self.tabel_anggota.column("Nama", width=220, anchor="w")
        self.tabel_anggota.column("Alamat", width=300, anchor="w")
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tabel_anggota.yview, style="Vertical.TScrollbar")
        self.tabel_anggota.configure(yscrollcommand=scrollbar.set)
        self.tabel_anggota.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.bind_mousewheel(self.tabel_anggota)
        self.tabel_anggota.bind("<ButtonRelease-1>", self.controller.pilih_anggota)

    def buat_tab_pinjam(self):
        page = self.pages['pinjam']
        self.create_header(page, "Transaksi Peminjaman & Pengembalian", "Proses peminjaman buku dan pengembalian secara real-time")
        main_container = tk.Frame(page, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=35, pady=(0, 20))
        forms_frame = tk.Frame(main_container, bg=self.colors['bg'])
        forms_frame.pack(fill='x', pady=(0, 15))

        pinjam_card = tk.Frame(forms_frame, bg=self.colors['card'], padx=20, pady=15)
        pinjam_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        tk.Label(pinjam_card, text="📥 Form Peminjaman Baru", font=('Segoe UI', 12, 'bold'), bg=self.colors['card'], fg=self.colors['primary']).pack(anchor='w', pady=(0, 10))
        self.create_form_field(pinjam_card, "ID Peminjaman", "ent_id_pinjam")
        self.create_form_field(pinjam_card, "ID Anggota", "ent_pinjam_anggota")
        self.create_form_field(pinjam_card, "ID Buku", "ent_pinjam_buku")
        tk.Label(pinjam_card, text="Tanggal Pinjam", font=('Segoe UI', 9, 'bold'), bg=self.colors['card'], fg=self.colors['text_dark']).pack(anchor='w', pady=(6, 4))
        self.ent_tanggal_pinjam = DateEntry(pinjam_card, width=20, background=self.colors['primary'], foreground='white', borderwidth=1, date_pattern='yyyy-mm-dd', font=('Segoe UI', 10))
        self.ent_tanggal_pinjam.pack(fill='x', ipady=5)
        self.create_btn(pinjam_card, "💾 Simpan Peminjaman", self.colors['primary'], self.controller.tambah_peminjaman, width=25).pack(pady=(15, 5))

        kembali_card = tk.Frame(forms_frame, bg=self.colors['card'], padx=20, pady=15)
        kembali_card.pack(side='right', fill='both', expand=True, padx=(10, 0))
        tk.Label(kembali_card, text="📤 Form Pengembalian Buku", font=('Segoe UI', 12, 'bold'), bg=self.colors['card'], fg=self.colors['success']).pack(anchor='w', pady=(0, 10))
        self.create_form_field(kembali_card, "ID Peminjaman Target", "ent_id_kembali")
        tk.Label(kembali_card, text="Tanggal Pengembalian", font=('Segoe UI', 9, 'bold'), bg=self.colors['card'], fg=self.colors['text_dark']).pack(anchor='w', pady=(6, 4))
        self.ent_tanggal_kembali = DateEntry(kembali_card, width=20, background=self.colors['success'], foreground='white', borderwidth=1, date_pattern='yyyy-mm-dd', font=('Segoe UI', 10))
        self.ent_tanggal_kembali.pack(fill='x', ipady=5)
        tk.Frame(kembali_card, bg=self.colors['card'], height=45).pack()
        self.create_btn(kembali_card, "✅ Process Pengembalian", self.colors['success'], self.controller.pengembalian_buku, width=25).pack(pady=(15, 5))

        table_card = tk.Frame(main_container, bg=self.colors['card'], padx=15, pady=15)
        table_card.pack(fill='both', expand=True)
        columns = ("ID", "Anggota", "Buku", "Pinjam", "Batas", "Kembali", "Status", "Denda")
        self.tabel_pinjam = ttk.Treeview(table_card, columns=columns, show="headings", height=6)
        for col in columns:
            self.tabel_pinjam.heading(col, text=col)
            self.tabel_pinjam.column(col, width=100, anchor="center")
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tabel_pinjam.yview, style="Vertical.TScrollbar")
        self.tabel_pinjam.configure(yscrollcommand=scrollbar.set)
        self.tabel_pinjam.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.bind_mousewheel(self.tabel_pinjam)
        self.tabel_pinjam.bind("<ButtonRelease-1>", self.controller.pilih_pinjam)

    def get_input_buku(self):
        return (self.ent_id_buku.get(), self.ent_judul.get(), self.ent_penerbit.get(), self.ent_tahun.get(), self.ent_kategori.get(), self.ent_stok.get())

    def get_input_anggota(self):
        return (self.ent_id_anggota.get(), self.ent_nama.get(), self.ent_alamat.get(), self.ent_no_hp.get())

    def get_input_pinjam(self):
        return (self.ent_id_pinjam.get(), self.ent_pinjam_anggota.get(), self.ent_pinjam_buku.get(), self.ent_tanggal_pinjam.get())

    def get_input_kembali(self):
        return (self.ent_id_kembali.get(), self.ent_tanggal_kembali.get())

    def isi_form_buku(self, id_buku, judul, penerbit, tahun, kategori, stok):
        self.ent_id_buku.delete(0, tk.END); self.ent_id_buku.insert(0, id_buku)
        self.ent_judul.delete(0, tk.END); self.ent_judul.insert(0, judul)
        self.ent_penerbit.delete(0, tk.END); self.ent_penerbit.insert(0, penerbit)
        self.ent_tahun.delete(0, tk.END); self.ent_tahun.insert(0, tahun)
        self.ent_kategori.delete(0, tk.END); self.ent_kategori.insert(0, kategori)
        self.ent_stok.delete(0, tk.END); self.ent_stok.insert(0, stok)

    def isi_form_anggota(self, id_anggota, nama, alamat, no_hp):
        self.ent_id_anggota.delete(0, tk.END); self.ent_id_anggota.insert(0, id_anggota)
        self.ent_nama.delete(0, tk.END); self.ent_nama.insert(0, nama)
        self.ent_alamat.delete(0, tk.END); self.ent_alamat.insert(0, alamat)
        self.ent_no_hp.delete(0, tk.END); self.ent_no_hp.insert(0, no_hp)

    def bersihkan_form(self):
        self.ent_id_buku.delete(0, tk.END); self.ent_judul.delete(0, tk.END); self.ent_penerbit.delete(0, tk.END); self.ent_tahun.delete(0, tk.END); self.ent_kategori.delete(0, tk.END); self.ent_stok.delete(0, tk.END)
        self.ent_id_anggota.delete(0, tk.END); self.ent_nama.delete(0, tk.END); self.ent_alamat.delete(0, tk.END); self.ent_no_hp.delete(0, tk.END)
        self.ent_id_pinjam.delete(0, tk.END); self.ent_pinjam_anggota.delete(0, tk.END); self.ent_pinjam_buku.delete(0, tk.END); self.ent_tanggal_pinjam.set_date('today')
        self.ent_id_kembali.delete(0, tk.END); self.ent_tanggal_kembali.set_date('today')

    def update_dashboard_stats(self, stats):
        try:
            self.stat_buku_total.config(text=str(stats['buku_total']))
            self.stat_anggota_total.config(text=str(stats['anggota_total']))
            self.stat_peminjaman_aktif.config(text=str(stats['peminjaman_aktif']))
            self.stat_total_denda.config(text=f"Rp {stats['total_denda']:,}")
        except Exception as e:
            print(f"Error update dashboard: {e}")

    def tampilkan_pesan(self, judul, pesan, error=False):
        messagebox.showerror(judul, pesan) if error else messagebox.showinfo(judul, pesan)