import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os

# Veritabanı bağlantısı
conn = sqlite3.connect('MARKET_ZİNCİRİ.db')
cursor = conn.cursor()

# Kullanıcılar tablosunu oluşturma
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT,
    name TEXT,
    surname TEXT,
    birth_date TEXT,
    tc_number TEXT
)""")
conn.commit()

# Kullanıcı kayıt fonksiyonu
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    name = reg_name_entry.get()
    surname = reg_surname_entry.get()
    birth_date = reg_birth_date_entry.get()
    tc_number = reg_tc_number_entry.get()

    if username and password and name and surname and birth_date and tc_number:
        try:
            cursor.execute("INSERT INTO users (username, password, name, surname, birth_date, tc_number) VALUES (?, ?, ?, ?, ?, ?)",
                           (username, password, name, surname, birth_date, tc_number))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt işlemi başarılı! Giriş ekranına yönlendiriliyorsunuz.")
            register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Kullanıcı adı zaten mevcut!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt yapılamadı: {e}")
    else:
        messagebox.showwarning("Eksik Bilgi", "Tüm alanlar doldurulmalıdır!")

# Giriş fonksiyonu
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Başarılı", "Giriş başarılı! Yönetim paneline yönlendiriliyorsunuz.")
        login_window.destroy()
        open_admin_panel(username)
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

# Admin panelini açan fonksiyon
def open_admin_panel(username):
    admin_window = tk.Tk()
    admin_window.title("Yönetim Paneli")
    admin_window.geometry("400x400")

    welcome_label = tk.Label(admin_window, text=f"Hoş geldiniz, {username}!", font=("Arial", 16))
    welcome_label.pack(pady=20)

    # Kullanıcı listesini gösteren fonksiyon
    def show_user_list():
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        user_list_window = tk.Toplevel(admin_window)
        user_list_window.title("Kullanıcı Listesi")
        user_list_window.geometry("300x300")

        tk.Label(user_list_window, text="Kullanıcılar:", font=("Arial", 14)).pack(pady=10)

        for user in users:
            tk.Label(user_list_window, text=f"{user[0]} - {user[2]} {user[3]}").pack()

    tk.Button(admin_window, text="Kullanıcıları Göster", command=show_user_list, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

    # Admin panelini açma butonu
    def open_other_module():
        main_script_path = "C:\\Users\\goktu\\Desktop\\FuatMarket\\main.py"
        if not os.path.exists(main_script_path):
            messagebox.showerror("Hata", "main.py dosyası bulunamadı!")
            return
        try:
            subprocess.Popen(["python", main_script_path], shell=True)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı: {e}")

    tk.Button(admin_window, text="Admin Panelini Aç", command=open_other_module, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
    tk.Button(admin_window, text="Çıkış Yap", command=admin_window.destroy, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=10)

    admin_window.mainloop()

# Kayıt ekranı
def open_register_window():
    global register_window, reg_username_entry, reg_password_entry, reg_name_entry, reg_surname_entry, reg_birth_date_entry, reg_tc_number_entry

    register_window = tk.Toplevel(login_window)
    register_window.title("Kayıt Ol")
    register_window.geometry("350x300")
    register_window.resizable(False, False)
    register_window.config(bg="#f7f7f7")
    
    # Form elemanları
    tk.Label(register_window, text="Ad:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=3)
    reg_name_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_name_entry.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(register_window, text="Soyad:", bg="#f7f7f7", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=3)
    reg_surname_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_surname_entry.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(register_window, text="Kullanıcı Adı:", bg="#f7f7f7", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=3)
    reg_username_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_username_entry.grid(row=2, column=1, padx=5, pady=3)

    tk.Label(register_window, text="Şifre:", bg="#f7f7f7", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=3)
    reg_password_entry = tk.Entry(register_window, show="*", font=("Arial", 12))
    reg_password_entry.grid(row=3, column=1, padx=5, pady=3)

    tk.Label(register_window, text="Doğum Tarihi (GG/AA/YYYY):", bg="#f7f7f7", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=3)
    reg_birth_date_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_birth_date_entry.grid(row=4, column=1, padx=5, pady=3)

    tk.Label(register_window, text="TC Kimlik Numarası:", bg="#f7f7f7", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=3)
    reg_tc_number_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_tc_number_entry.grid(row=5, column=1, padx=5, pady=3)

    # Kayıt ve Geri Dön butonları
    tk.Button(register_window, text="Kayıt Ol", command=register_user, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(register_window, text="Giriş Ekranına Dön", command=register_window.destroy, bg="#f44336", fg="white", font=("Arial", 12)).grid(row=7, column=0, columnspan=2, pady=5)

# Giriş ekranı
login_window = tk.Tk()
login_window.title("Giriş Yap")
login_window.geometry("350x300")
login_window.config(bg="#f7f7f7")

# Giriş ekranı bileşenleri
tk.Label(login_window, text="Kullanıcı Adı:", bg="#f7f7f7", font=("Arial", 12)).pack(pady=5)
login_username_entry = tk.Entry(login_window, font=("Arial", 12))
login_username_entry.pack(pady=5)

tk.Label(login_window, text="Şifre:", bg="#f7f7f7", font=("Arial", 12)).pack(pady=5)
login_password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
login_password_entry.pack(pady=5)

button_frame = tk.Frame(login_window, bg="#f7f7f7")
button_frame.pack(pady=10)

# Giriş ve Kayıt Ol butonları
tk.Button(button_frame, text="Giriş Yap", command=login_user, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Kayıt Ol", command=open_register_window, bg="#f44336", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=5)

login_window.mainloop()

# Veritabanını kapatma
cursor.close()
conn.close()