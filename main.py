# KULLANILACAK MODÜLLER
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3
from tkinter import *
import csv
from tkinter import ttk
from tkinter import Tk, Label, Button, Entry, StringVar, Frame, ttk,messagebox
from tkinter import messagebox
# VERİ TABANI
veriler= sqlite3.connect('MARKET_ZİNCİRİ.db')
market = veriler.cursor()
market.execute("create table if not exists urun(urun_adi TEXT, urun_fiyati TEXT, urun_kdv TEXT)")
market.execute("create table if not exists stok(urun_id integer,urun_adi TEXT, adet integer)")
veriler.commit()

# Mevcut tabloları oluşturma
market.execute("CREATE TABLE IF NOT EXISTS urun (urun_adi TEXT, urun_fiyati TEXT, urun_kdv TEXT)")
market.execute("CREATE TABLE IF NOT EXISTS stok (urun_id INTEGER, urun_adi TEXT, adet INTEGER)")


market.execute("CREATE TABLE IF NOT EXISTS urun (urun_adi TEXT, urun_fiyati TEXT, urun_kdv TEXT)")
market.execute("CREATE TABLE IF NOT EXISTS stok (urun_id INTEGER, urun_adi TEXT, adet INTEGER)")

# Kullanıcılar tablosunu oluştur
market.execute('''
CREATE TABLE IF NOT EXISTS kullanicilar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
)
''')
# Raporlar tablosunu oluşturma
market.execute('''
CREATE TABLE IF NOT EXISTS raporlar (
    rapor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rapor_turu TEXT NOT NULL,
    aciklama TEXT NOT NULL,
    tarih DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')



# UYARILAR
def kayıt_başarılı(text):
    mesaj = messagebox.showinfo(text, "Kayıt Başarılı...")
def kayıt_mevcut(text):
    mesaj = messagebox.showerror(text, "Bu isimde Ürün Mevcut...")
def kayıt_sil(text):
    mesaj = messagebox.showinfo(text, "Kayıt Silindi...")
def kayıt_güncele(text):
    mesaj = messagebox.showinfo(text, "Kaydınız Güncellendi...")

# MENÜ PENCERESİ
def Ana_Menü():
    for i in pen.winfo_children():  # Eğer pen doluysa sil
        i.destroy()
    pen.title("ANA MENÜ")

    # Market Adı
    market_adi = Label(text="Bakkal360", bg="#6200EA", fg="#BBDEFB", font="Helvetica 28")
    market_adi.place(x=120, y=10, width=360, height=50)

    # Butonları yerleştirmek için bir çerçeve oluştur
    buton_cerceve = Frame(pen)
    buton_cerceve.place(relx=0.5, rely=0.6, anchor=CENTER)  # Y konumunu 0.5'ten 0.6'ya kaydırdık

    # Butonların boyutları ve fontları
    button_font = ("Helvetica", 20)

    # Ürün Ekranı Butonu
    urun_buton = Button(buton_cerceve, text="ÜRÜN EKRANI", command=Ürün_Pen, bg="#B71C1C", fg="#F3E5F5", font=button_font)
    urun_buton.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # Stok Ekranı Butonu
    stok_buton = Button(buton_cerceve, text="STOK EKRANI", command=stok_menu, bg="#B71C1C", fg="#F3E5F5", font=button_font)
    stok_buton.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Satış Ekranı Butonu
    satis_buton = Button(buton_cerceve, text="SATIŞ EKRANI", command=satis_menu, bg="#B71C1C", fg="#F3E5F5", font=button_font)
    satis_buton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Raporlama Butonu
    raporlama_buton = Button(buton_cerceve, text="RAPORLAMA", command=raporlama_menu, bg="#B71C1C", fg="#F3E5F5", font=button_font)
    raporlama_buton.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Ayarlar Butonu
    ayarlar_buton = Button(buton_cerceve, text="AYARLAR", command=ayarlar_menu, bg="#B71C1C", fg="#F3E5F5", font=button_font)
    ayarlar_buton.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Yardım Butonu
    yardim_buton = Button(buton_cerceve, text="YARDIM", command=yardim_menu, bg="#B71C1C", fg="#F3E5F5", font=button_font)
    yardim_buton.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
# Satış Menüsü Fonksiyonu
# Satış ekranı
# Satış ekranı
def satis_menu():
    for widget in pen.winfo_children():
        widget.destroy()
    pen.title("SATIŞ EKRANI")

    # Başlık
    header = Label(pen, text="SATIŞ", font="Helvetica 24 bold", fg="#4A90E2")
    header.pack(pady=20)

    # Ürün Seçimi ve Miktar Girişi
    frame = Frame(pen)
    frame.pack(pady=10)

    Label(frame, text="Ürün Seçin:", font="Helvetica 14").grid(row=0, column=0, padx=10, pady=5)
    urun_secimi = StringVar()

    # Ürünleri yükle
    market.execute("SELECT urun_adi FROM urun")
    urunler = [row[0] for row in market.fetchall()]
    
    urun_menu = ttk.Combobox(frame, textvariable=urun_secimi, values=urunler, font="Helvetica 14")
    urun_menu.grid(row=0, column=1, padx=10, pady=5)

    Label(frame, text="Miktar:", font="Helvetica 14").grid(row=1, column=0, padx=10, pady=5)
    miktar_girisi = Entry(frame, font="Helvetica 14")
    miktar_girisi.grid(row=1, column=1, padx=10, pady=5)

    # Toplam Fiyat Hesaplama
    toplam_label = Label(pen, text="Toplam Fiyat: 0.00 TL", font="Helvetica 16 bold", fg="#4A90E2")
    toplam_label.pack(pady=15)

    def toplam_hesapla():
        selected_urun = urun_secimi.get()
        market.execute("SELECT urun_fiyati FROM urun WHERE urun_adi=?", (selected_urun,))
        urun_fiyat = market.fetchone()
        if urun_fiyat:
            try:
                miktar = int(miktar_girisi.get())
                toplam = miktar * float(urun_fiyat[0])  # Fiyatı float olarak al
                toplam_label.config(text=f"Toplam Fiyat: {toplam:.2f} TL")
            except ValueError:
                toplam_label.config(text="Lütfen geçerli bir miktar girin.")

    hesapla_buton = Button(pen, text="Hesapla", command=toplam_hesapla, bg="#4CAF50", fg="white", font="Helvetica 14")
    hesapla_buton.pack(pady=10)

    # Satışı Kaydet
    def satis_kaydet():
        selected_urun = urun_secimi.get()
        try:
            miktar = int(miktar_girisi.get())
            market.execute("SELECT urun_id, adet FROM stok WHERE urun_adi=?", (selected_urun,))
            stok_bilgisi = market.fetchone()
            if stok_bilgisi:
                mevcut_stok = stok_bilgisi[1]
                if mevcut_stok >= miktar:
                    yeni_stok = mevcut_stok - miktar
                    market.execute("UPDATE stok SET adet=? WHERE urun_id=?", (yeni_stok, stok_bilgisi[0]))
                    veriler.commit()
                    messagebox.showinfo("BAŞARILI", f"{miktar} adet {selected_urun} satıldı. Yeni stok: {yeni_stok}.")
                    miktar_girisi.delete(0, "end")
                    toplam_label.config(text="Toplam Fiyat: 0.00 TL")
                else:
                    messagebox.showerror("HATA", "Yeterli stok yok!")
            else:
                messagebox.showerror("HATA", "Ürün bulunamadı!")
        except ValueError:
            messagebox.showerror("HATA", "Lütfen geçerli bir miktar girin.")

    kaydet_buton = Button(pen, text="Satışı Kaydet", command=satis_kaydet, bg="#2196F3", fg="white", font="Helvetica 14")
    kaydet_buton.pack(pady=10)

    # Ana Menü Butonu
    geri_buton = Button(pen, text="Ana Menü", command=Ana_Menü, bg="#B71C1C", fg="white", font="Helvetica 14")
    geri_buton.pack(side='top', anchor='nw', padx=10, pady=10)
# Raporlama Menüsü Fonksiyonu
def raporlama_menu():
    for i in pen.winfo_children():
        i.destroy()
    pen.title("RAPORLAMA")
    
    # Raporlama ekranı içeriği
    Label(text="Raporlama Ekranı", font="Helvetica 24 bold", bg="#E0E0E0").pack(pady=20)

    # Ana Menü butonu
    ana_menu_buton = Button(text="ANA MENÜ", command=Ana_Menü, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 12")
    ana_menu_buton.place(x=10, y=10)  # Sol üst köşe için konum ayarı

    # Raporlama seçenekleri
    Label(text="Rapor Türü Seçin:", font="Helvetica 18").pack(pady=10)

    # Rapor türleri için seçim
    rapor_turleri = ["Tüm Ürünler", "Stok Durumu", "Satış Raporu"]
    rapor_turu = StringVar(value=rapor_turleri[0])

    for tur in rapor_turleri:
        Radiobutton(pen, text=tur, variable=rapor_turu, value=tur, font="Helvetica 16").pack(anchor=W)

    # Raporu oluştur butonu
    rapor_buton = Button(text="Raporu Oluştur", command=lambda: rapor_olustur(rapor_turu.get()), bg="#4CAF50", fg="#FFFFFF", font="Helvetica 18")
    rapor_buton.pack(pady=20)

    # Kaydedilen raporları görüntüleme butonu
    görüntüle_buton = Button(text="Kaydedilen Raporları Görüntüle", command=görüntüle_raporlar, bg="#2196F3", fg="#FFFFFF", font="Helvetica 18")
    görüntüle_buton.pack(pady=10)
def rapor_olustur(tur):
    # Yeni bir pencere aç
    rapor_penceresi = Toplevel(pen)
    rapor_penceresi.title(f"{tur} Raporu")
    rapor_penceresi.geometry("600x400")
    
    # Rapor oluşturma içeriği
    Label(rapor_penceresi, text=f"{tur} Raporu", font="Helvetica 24 bold").pack(pady=20)

    # Metin girişi için etiket ve alan
    Label(rapor_penceresi, text="Açıklama Yazın:", font="Helvetica 16").pack(pady=10)
    metin_girisi = Text(rapor_penceresi, height=10, width=50)
    metin_girisi.pack(pady=10)

    # Raporu oluşturma butonu
    olustur_buton = Button(rapor_penceresi, text="Raporu Oluştur", command=lambda: save_rapor(tur, metin_girisi.get("1.0", END)), bg="#4CAF50", fg="#FFFFFF", font="Helvetica 18")
    olustur_buton.pack(pady=20)

    # Geri butonu
    geri_buton = Button(rapor_penceresi, text="Geri", command=rapor_penceresi.destroy, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 18")
    geri_buton.pack(pady=20)

def save_rapor(tur, aciklama):
    # Raporu veritabanına kaydet
    market.execute("INSERT INTO raporlar (rapor_turu, aciklama) VALUES (?, ?)", (tur, aciklama.strip()))
    veriler.commit()
    
    messagebox.showinfo("BAŞARILI", f"{tur} raporu başarıyla kaydedildi.\n\nAçıklama: {aciklama.strip()}")

    # Raporları görüntüleme
    görüntüle_raporlar()

def görüntüle_raporlar():
    # Raporları gösteren yeni bir pencere aç
    rapor_goruntuleme_penceresi = Toplevel(pen)
    rapor_goruntuleme_penceresi.title("Raporları Görüntüle")
    rapor_goruntuleme_penceresi.geometry("600x400")

    Label(rapor_goruntuleme_penceresi, text="Kaydedilen Raporlar", font="Helvetica 24 bold").pack(pady=20)

    # Raporları listelemek için bir liste kutusu
    rapor_listesi = Listbox(rapor_goruntuleme_penceresi, width=80, height=15)
    rapor_listesi.pack(pady=10)

    # Veritabanından raporları çek ve listeye ekle
    market.execute("SELECT rapor_turu, aciklama, tarih FROM raporlar")
    for rapor in market.fetchall():
        rapor_listesi.insert(END, f"{rapor[0]}: {rapor[1]} (Tarih: {rapor[2]})")

    geri_buton = Button(rapor_goruntuleme_penceresi, text="Geri", command=rapor_goruntuleme_penceresi.destroy, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 18")
    geri_buton.pack(pady=20)

def ayarlar_menu():
    for i in pen.winfo_children():
        i.destroy()
    pen.title("AYARLAR")

    # Başlık
    Label(text="Ayarlar Menüsü", font="Helvetica 24 bold").pack(pady=20)

    # Buton çubuğu
    buton_cubugu = Frame(pen)
    buton_cubugu.pack(pady=10)

    # Butonlar
    Button(buton_cubugu, text="Tema", command=tema_ayarları, width=10).grid(row=0, column=0, padx=5)
    Button(buton_cubugu, text="Bildirim", command=bildirim_ayarları, width=10).grid(row=0, column=1, padx=5)
    Button(buton_cubugu, text="Dil", command=dil_ayarları, width=10).grid(row=0, column=2, padx=5)
    Button(buton_cubugu, text="Güvenlik", command=guvenlik_ayarları, width=10).grid(row=0, column=3, padx=5)

    # Geri Butonu
    geri_buton = Button(pen, text="ANA MENÜ", command=Ana_Menü, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 18", height=2, width=20)
    geri_buton.pack(pady=20)

def tema_ayarları():
    ayarlar_guncelle("Tema Seçenekleri", ["Açık Tema", "Koyu Tema"], tema_degistir)

def bildirim_ayarları():
    ayarlar_guncelle("Bildirim Ayarları", ["Bildirimleri Aç", "Bildirimleri Kapat"], bildirim_degistir)

def dil_ayarları():
    ayarlar_guncelle("Dil Seçenekleri", ["Türkçe", "İngilizce", "Almanca"], dil_degistir)

def guvenlik_ayarları():
    ayarlar_guncelle("Güvenlik Ayarları", ["İki Aşamalı Doğrulama Aç", "İki Aşamalı Doğrulama Kapat"], guvenlik_degistir)

def ayarlar_guncelle(baslik, secenekler, guncelleme_fonksiyonu):
    for i in pen.winfo_children():
        i.destroy()
    Label(text=baslik, font="Helvetica 20").pack(pady=20)

    for secenek in secenekler:
        Button(pen, text=secenek, command=lambda s=secenek: guncelleme_fonksiyonu(s), width=20).pack(pady=5)

    geri_buton = Button(pen, text="Geri", command=ayarlar_menu, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 14", height=1, width=10)
    geri_buton.pack(pady=20)

def tema_degistir(tema):
    if tema == "Koyu Tema":
        pen.configure(bg="#333333")
        for widget in pen.winfo_children():
            widget.configure(bg="#333333", fg="#FFFFFF")
    else:
        pen.configure(bg="#FFFFFF")
        for widget in pen.winfo_children():
            widget.configure(bg="#FFFFFF", fg="#000000")
    bildirim_gonder(f"Tema değiştirildi: {tema}")

def bildirim_degistir(secenek):
    if secenek == "Bildirimleri Aç":
        print("Bildirimler açıldı.")
        global bildirim_acik
        bildirim_acik = True
    else:
        print("Bildirimler kapatıldı.")
        bildirim_acik = False

def dil_degistir(secenek):
    print(f"Dil ayarı değiştirildi: {secenek}")
    if secenek == "İngilizce":
        bildirim_degistir("Bildirimleri Aç")  # Bildirimleri aç
        bildirim_gonder("Dil değiştirildi: İngilizce")

def guvenlik_degistir(secenek):
    if secenek == "İki Aşamalı Doğrulama Aç":
        print("İki aşamalı doğrulama açıldı.")
        bildirim_gonder("İki aşamalı doğrulama açıldı.")
    else:
        print("İki aşamalı doğrulama kapatıldı.")
        bildirim_gonder("İki aşamalı doğrulama kapatıldı.")

def bildirim_gonder(mesaj):
    if bildirim_acik:
        print(f"BILDIRIM: {mesaj}")

# Başlangıçta bildirimlerin kapalı olduğunu varsayalım
bildirim_acik = False
# Yardım Menüsü Fonksiyonu
def yardim_menu():
    for i in pen.winfo_children():
        i.destroy()
    pen.title("YARDIM")

    # Başlık
    Label(text="Yardım ve Destek", font="Helvetica 24").pack(pady=20)

    # Yardım içeriği için çerçeve
    yardim_cerceve = Frame(pen)
    yardim_cerceve.pack(pady=20)

    # Yardım bilgileri ve butonlar
    Label(yardim_cerceve, text="Sıkça Sorulan Sorular", font="Helvetica 16").grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Ürün Ekranı
    Label(yardim_cerceve, text="1. Ürün eklemek için 'Ürün Ekranı'na gidin.", font="Helvetica 12").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    urun_buton = Button(yardim_cerceve, text="Git", command=Ürün_Pen, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 10")
    urun_buton.grid(row=1, column=1, padx=5, pady=5)

    # Stok Ekranı
    Label(yardim_cerceve, text="2. Stok durumunu kontrol etmek için 'Stok Ekranı'na gidin.", font="Helvetica 12").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    stok_buton = Button(yardim_cerceve, text="Git", command=stok_menu, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 10")
    stok_buton.grid(row=2, column=1, padx=5, pady=5)

    # Yardım Menüsü
    Label(yardim_cerceve, text="3. Yardım almak için bu menüyü kullanın.", font="Helvetica 12").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    # Bu satıra buton eklemek gerekli değil, çünkü zaten bu menüdeyiz.
    
    # Geri Butonu
    geri_buton = Button(pen, text="ANA MENÜ", command=Ana_Menü, bg="#B71C1C", fg="#F3E5F5", font="Helvetica 18")
    geri_buton.pack(pady=20)

# ÜRÜN MENÜSÜ PENCERESİ
def Ürün_Pen():
    # ÜRÜN KAYIT BÖLÜMÜ
    def Ürün_Ekle():
        ürün_ad = veri_adı.get()
        fiyat = veri_fiyatı.get()
        kdv = veri_kdv.get()

        def Ürünler():
            market.execute("insert into urun values(?,?,?)", [ürün_ad, fiyat, kdv])
            veriler.commit()
            #STOK VERI TABANINA YAZMA
            market.execute("""SELECT rowid,urun_adi FROM urun""")
            kontrol_ara = market.fetchall()
            for i in kontrol_ara:
                stok_ad_kontrol = i[1]
                ürün_id_no=i[0]
                if stok_ad_kontrol == ürün_ad:
                    market.execute("insert into stok values(?,?,?)", [ürün_id_no,ürün_ad, '0'])
                    veriler.commit()

        kod = 0
        market.execute("""SELECT urun_adi FROM urun""")
        kontrol = market.fetchall()
        for i in kontrol:  # KONTROL PANELİ ÜRÜNÜN OLUP OLMADIĞINI KONTROL EDER
            ad_kontrol = i[0]
            if ad_kontrol == ürün_ad:
                kayıt_mevcut("MALESEF AYNI KAYIT MEVCUT...")
                kod = 1
        if kod == 0:
            Ürünler()
            kayıt_başarılı("KAYIT YAPILDI...")
            veri_adı.delete(0, "end")
            veri_fiyatı.delete(0, "end")
            veri_kdv.delete(0, "end")
            for i in liste.get_children():
                liste.delete(i)
            market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
            urun_liste = market.fetchall()
            for i in urun_liste:
                liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))

    def Ürün_Silme():
        A = veri_adı.get()
        # STOKTAN KAYIT SILME
        market.execute("""SELECT rowid,urun_adi FROM urun""")
        kontrol_ara = market.fetchall()
        for i in kontrol_ara:
            stok_ad_kontrol = i[1]
            if stok_ad_kontrol == A:
                silmek=i[0]
        msg = messagebox.askyesno("SİLME İŞLEMİ", "EMİN MİSİN?")
        if msg == True:
            market.execute("delete from urun where urun_adi= ? ", [A])
            market.execute("delete from stok where urun_id= ? ", [silmek])
            veriler.commit()
            veri_adı.delete(0, "end")
            veri_fiyatı.delete(0, "end")
            veri_kdv.delete(0, "end")
            kayıt_sil("SİLME İŞLEMİ YAPILDI...")
            for i in liste.get_children():
                liste.delete(i)
            market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
            urun_liste = market.fetchall()
            for i in urun_liste:
                liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))

#KAYIT GÜNCELLEME
    def Ürün_Günceleme():
        veri_al = liste.selection()[0]
        item = liste.item(veri_al)
        sec_id_no = item['values'][0]
        # update kodu ile mevcut olan veriyi değiştirile bilir.
        market.execute("update urun set urun_adi='{}',urun_fiyati='{}',urun_kdv='{}' WHERE rowid='{}'".
                   format(veri_adı.get(),veri_fiyatı.get(),veri_kdv.get(),sec_id_no))
        veriler.commit()

        veri_adı.delete(0, "end")
        veri_fiyatı.delete(0, "end")
        veri_kdv.delete(0, "end")
        kayıt_güncele("KAYDINIZ GÜNCELENDİ...")
        for i in liste.get_children():
            liste.delete(i)
        market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
        urun_liste = market.fetchall()
        for i in urun_liste:
            liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))



    for i in pen.winfo_children():
        i.destroy() #Mevcut pencere temizleniyor
    pen.title("ÜRÜN") #ÜRÜN SAYFASI TASLAĞI OLUŞTURULUYOR
    Label(text="Ürün Adı", font="Helvetica 12 ").place(x=250, y=20)
    Label(text="Ürün Fiyatı", font="Helvetica 12 ").place(x=250, y=60)
    Label(text="KDV", font="Helvetica 12 ").place(x=250, y=95)
    veri_adı = Entry(width=35)
    veri_adı.place(x=330, y=20,height=28)
    veri_fiyatı = Entry(width=35)
    veri_fiyatı.place(x=330, y=60,height=28)
    veri_kdv = Entry(width=35)
    veri_kdv.place(x=330, y=95,height=28)
    #butonlar
    ürün_menü = Button(text="ANA MENÜ", command=Ana_Menü, font="Helvetica 12 ",bg="#1E88E5")
    ürün_menü.place(x=10, y=20, width=100, height=40)
    ürün_kaydet = Button(text="KAYDET", command=Ürün_Ekle,font="Helvetica 12 ",bg="#1E88E5")
    ürün_kaydet.place(x=130, y=20, width=100, height=40)
    ürün_yenile= Button(text="GÜNCELLE", command=Ürün_Günceleme,font="Helvetica 12 ",bg="#1E88E5")
    ürün_yenile.place(x=10, y=80, width=100, height=40)
    Silme_işlemi = Button(text="SİL", command=Ürün_Silme,font="Helvetica 12 ",bg="#1E88E5")
    Silme_işlemi.place(x=130, y=80, width=100, height=40)

    #SQLİTE verileri listeleme ve ekrana yansıtma
    liste = Treeview(pen)
    liste["columns"] = ("id_no", "Ad", "fiyat", "kdv")
    liste.column('#0', width=0, stretch=NO)
    liste.column('id_no', width=35, anchor=CENTER)
    liste.column('Ad', anchor=CENTER, width=180)
    liste.column('fiyat', anchor=CENTER, width=110)
    liste.column('kdv', anchor=CENTER, width=110)
    liste.place(x=15, y=140, width=520, height=250)
    liste.heading("#0", text="")
    liste.heading("id_no", text="ID")
    liste.heading("Ad", text="Ürün Adı")
    liste.heading("fiyat", text="Ürün Fiyatı")
    liste.heading("kdv", text="KDV %")
    # ürün veri tabanındaki veriler
    market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
    urun_liste = market.fetchall()
    for i in urun_liste:
        liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))

    def aktarma(object): # eğer veri giriş ekranında veri varsa temizle ve tabloda seçili veriyi giriş ekranına yansıt
        veri_adı.delete(0, "end")
        veri_fiyatı.delete(0, "end")
        veri_kdv.delete(0, "end")
        veri_al = liste.selection()[0]
        item = liste.item(veri_al)
        veri_adı.insert(0, item['values'][1])
        veri_fiyatı.insert(0, item['values'][2])
        veri_kdv.insert(0, item['values'][3])

    liste.bind("<Double-1>", aktarma)

def stok_menu():
    def temizle_gecersiz_kayitlar():
        market.execute("DELETE FROM stok WHERE urun_adi IS NULL OR urun_adi='None'")
        veriler.commit()

    def stok_ekle():
        urun_adi = urun_ad_entry.get().strip()  # Boşlukları temizle
        try:
            adet_miktar = int(adet_entry.get())
            if adet_miktar < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("HATA", "Geçersiz adet girişi!")
            return
        
        if not urun_adi:  # Ürün adı boş mu kontrol et
            messagebox.showerror("HATA", "Ürün adı boş olamaz!")
            return

        market.execute("INSERT INTO stok (urun_adi, adet) VALUES (?, ?)", (urun_adi, adet_miktar))
        veriler.commit()
        urun_ad_entry.delete(0, "end")
        adet_entry.delete(0, "end")
        güncelle_stok_liste()
        messagebox.showinfo("BAŞARILI", f"{urun_adi} başarıyla eklendi!")

    def stok_cikar():
        ekli_ürün = combo.get()
        try:
            adet_miktar = int(adet_entry.get())
            if adet_miktar < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("HATA", "Geçersiz adet girişi!")
            return

        market.execute("SELECT adet FROM stok WHERE urun_adi=?", (ekli_ürün,))
        mevcut_stok = market.fetchone()
        
        if mevcut_stok and mevcut_stok[0] >= adet_miktar:
            yeni_stok = mevcut_stok[0] - adet_miktar
            market.execute("UPDATE stok SET adet=? WHERE urun_adi=?", (yeni_stok, ekli_ürün))
            veriler.commit()
            adet_entry.delete(0, "end")
            güncelle_stok_liste()
            messagebox.showinfo("BAŞARILI", f"{ekli_ürün} için stok güncellendi! Yeni stok: {yeni_stok}.")
        else:
            messagebox.showerror("HATA", "Yeterli stok yok veya ürün bulunamadı!")

    def satis_kaydet():
        ekli_ürün = combo.get()
        try:
            adet_miktar = int(adet_entry.get())
            if adet_miktar < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("HATA", "Geçersiz adet girişi!")
            return

        market.execute("SELECT adet FROM stok WHERE urun_adi=?", (ekli_ürün,))
        mevcut_stok = market.fetchone()

        if mevcut_stok and mevcut_stok[0] >= adet_miktar:
            yeni_stok = mevcut_stok[0] - adet_miktar
            market.execute("UPDATE stok SET adet=? WHERE urun_adi=?", (yeni_stok, ekli_ürün))
            veriler.commit()
            adet_entry.delete(0, "end")
            güncelle_stok_liste()
            messagebox.showinfo("BAŞARILI", f"{ekli_ürün} için satış yapıldı! Yeni stok: {yeni_stok}.")
        else:
            messagebox.showerror("HATA", "Yeterli stok yok veya ürün bulunamadı!")

    def stok_sil():
        ekli_ürün = combo.get()
        if ekli_ürün == "None":
            messagebox.showerror("HATA", "Silmek istediğiniz ürün geçersiz!")
            return

        market.execute("DELETE FROM stok WHERE urun_adi=?", (ekli_ürün,))
        veriler.commit()
        güncelle_stok_liste()
        messagebox.showinfo("BAŞARILI", f"{ekli_ürün} başarıyla silindi!")

    def güncelle_stok_liste():
        for i in liste.get_children():
            liste.delete(i)
        market.execute("SELECT urun_id, urun_adi, adet FROM stok")
        stok_liste = market.fetchall()
        for i in stok_liste:
            liste.insert(parent='', index='end', values=(i[0], i[1], i[2]))

    def csv_dışa_aktar():
        with open('stok_listesi.csv', mode='w', newline='') as stok_file:
            stok_writer = csv.writer(stok_file)
            stok_writer.writerow(["ID", "Ürün Adı", "Adet"])
            market.execute("SELECT urun_id, urun_adi, adet FROM stok")
            for row in market.fetchall():
                stok_writer.writerow(row)
        messagebox.showinfo("BAŞARILI", "CSV dosyası başarıyla dışa aktarıldı!")

    # Temizleme fonksiyonunu çağır
    temizle_gecersiz_kayitlar()

    for i in pen.winfo_children():
        i.destroy()  # Kayıtlı olan pencereyi temizler
    pen.title("STOK")  # Yeni stok penceresi oluşturuluyor

    Label(text="Ürün Adı", font="Helvetica 12").place(x=20, y=20)
    urun_ad_entry = Entry(pen, width=30)
    urun_ad_entry.place(x=150, y=20)

    Label(text="Ürün Adedi", font="Helvetica 12").place(x=20, y=60)
    adet_entry = Entry(pen, width=30)
    adet_entry.place(x=150, y=60)

    Stok_kaydet = Button(text="ÜRÜN EKLE", command=stok_ekle, bg="#1E88E5")
    Stok_kaydet.place(x=20, y=100, width=180, height=30)

    Stok_cık = Button(text="ÜRÜN ÇIKART", command=stok_cikar, bg="#1E88E5")
    Stok_cık.place(x=20, y=140, width=180, height=30)

    Stok_sil = Button(text="ÜRÜN SİL", command=stok_sil, bg="#1E88E5")
    Stok_sil.place(x=20, y=180, width=180, height=30)

    Stok_csv = Button(text="CSV Dışa Aktar", command=csv_dışa_aktar, bg="#1E88E5")
    Stok_csv.place(x=20, y=220, width=180, height=30)

    ana = Button(text="ANA MENÜ", command=Ana_Menü, bg="#1E88E5")
    ana.place(x=20, y=260, width=180, height=30)

    # Ürün combobox
    combo = ttk.Combobox(pen, width=28)
    combo.place(x=350, y=20)
    market.execute("SELECT urun_adi FROM stok")
    stok_liste = market.fetchall()
    combo['values'] = [i[0] for i in stok_liste]

    # Stok listesi
    liste = ttk.Treeview(pen, columns=("id_no", "Ad", "adet"), show='headings')
    liste.heading("id_no", text="ID")
    liste.heading("Ad", text="Ürün Adı")
    liste.heading("adet", text="Adet")
    liste.place(x=20, y=300, width=460, height=180)
    güncelle_stok_liste()
    def stok_ekle_cikart(args):
        try:
            ekle = int(adet.get())
            ekli_ürün = combo.get()
            if ekli_ürün == "":
                messagebox.showerror("HATA", "Lütfen bir ürün seçin!")
                return
        except ValueError:
            messagebox.showerror("HATA", "Adet sayısı geçersiz!")
            return

        market.execute("SELECT urun_adi, adet FROM stok WHERE urun_adi=?", (ekli_ürün,))
        kontrol_ara = market.fetchone()
        
        if kontrol_ara:
            mevcut_stok = kontrol_ara[1]
            son_stok = mevcut_stok + ekle if args == 1 else mevcut_stok - ekle
            
            if son_stok < 0:
                messagebox.showerror("HATA", "Stok miktarı negatif olamaz!")
                return
            
            market.execute("UPDATE stok SET adet=? WHERE urun_adi=?", (son_stok, ekli_ürün))
            veriler.commit()
            adet.delete(0, "end")
            güncelle_stok_liste()
            messagebox.showinfo("BAŞARILI", f"{ekli_ürün} için yeni stok: {son_stok}")
        else:
            messagebox.showerror("HATA", "Ürün bulunamadı!")

    def güncelle_stok_liste():
        for i in liste.get_children():
            liste.delete(i)
        market.execute("SELECT urun_id, urun_adi, adet FROM stok")
        stok_liste = market.fetchall()
        for i in stok_liste:
            liste.insert(parent='', index='end', values=(i[0], i[1], i[2]))

    for i in pen.winfo_children():
        i.destroy()  # Kayıtlı olan pencereyi temizler
    pen.title("STOK")  # Yeni stok penceresi oluşturuluyor

    Stok_kaydet = Button(text="ÜRÜN EKLE", command=lambda: stok_ekle_cikart(1), bg="#1E88E5")
    Stok_kaydet.place(x=20, y=20, width=180, height=30)
    
    Stok_cık = Button(text="ÜRÜN ÇIKART", command=lambda: stok_ekle_cikart(2), bg="#1E88E5")
    Stok_cık.place(x=20, y=60, width=180, height=30)
    
    ana = Button(text="ANA MENÜ", command=Ana_Menü, bg="#1E88E5")
    ana.place(x=20, y=100, width=180, height=30)

    Label(text="Ürün Adı", font="Helvetica 12").place(x=266, y=40)
    Label(text="Ürün Adedi", font="Helvetica 12").place(x=266, y=80)

    # Ürün combobox
    combo = Combobox(width=28)
    combo.place(x=350, y=40, height=30)
    market.execute("SELECT urun_adi FROM stok")
    stok_liste = market.fetchall()
    combo['values'] = [i[0] for i in stok_liste]

    adet = Entry(width=31)
    adet.place(x=350, y=80, height=30)

    # Stok listesi
    liste = Treeview(pen)
    liste["columns"] = ("id_no", "Ad", "adet")
    liste.column('#0', width=0, stretch=NO)
    liste.column('id_no', width=20, anchor=CENTER)
    liste.column('Ad', anchor=CENTER, width=220)
    liste.column('adet', anchor=CENTER, width=100)
    liste.place(x=20, y=140, width=460, height=180)
    liste.heading("#0", text="")
    liste.heading("id_no", text="ID")
    liste.heading("Ad", text="Ürün Adı")
    liste.heading("adet", text="Adet")

    güncelle_stok_liste()

    Label(text="Ürün Adı", font="Helvetica 12 ").place(x=266, y=40)
    Label(text="Ürün Adedi", font="Helvetica 12 ").place(x=266, y=80)

    combo= Combobox(width=28) #ÜRÜN TABLOSUNDAKİ VERİLERİ ALIP LİSTELİ ŞEKİLDE GÖSTERMESİ
    combo.place(x=350,y=40,height=30)
    market.execute("""SELECT urun_adi, adet FROM stok""")
    stok_liste = market.fetchall()
    for i in stok_liste:
        combo['values'] = tuple(list(combo['values']) + [str(i[0])])
    adet = Entry(width=31)
    adet.place(x=350, y=80,height=30)

    liste = Treeview(pen)
    liste["columns"] = ("id_no", "Ad", "adet")
    liste.column('#0', width=0, stretch=NO)
    liste.column('id_no', width=20, anchor=CENTER)
    liste.column('Ad', anchor=CENTER, width=220)
    liste.column('adet', anchor=CENTER, width=100)

    liste.place(x=20, y=140, width=460, height=180)
    liste.heading("#0", text="")
    liste.heading("id_no", text="ID")
    liste.heading("Ad", text="Ürün Adı")
    liste.heading("adet", text="Adet")

    market.execute("""SELECT urun_id,urun_adi, adet FROM stok""")
    stok_liste = market.fetchall()
    for i in stok_liste:
        liste.insert(parent='', index='end', values=(i[0],i[1],i[2]))

# PENCERE OLUŞTURMA
pen = tk.Tk()
pen.geometry("550x400+500+200")
pen.resizable(False, False)
Ana_Menü()

pen.mainloop()