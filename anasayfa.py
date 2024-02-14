import datetime
from PyQt5.QtWidgets import *
from listele import liste_tablosu
from anamenu import Ui_Form
from hizli_not_kod import hizli_Not
from gelir_liste_kod import GelirListe
import sqlite3
from PyQt5.QtCore import QDate
from datetime import datetime





class anamenu_ui(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.listepencere=liste_tablosu()
        self.ui.btnListele.clicked.connect(self.tablo_liste)
        self.ui.pushButton_2.clicked.connect(self.kayit_yap)
        self.ui.kayitTarih.selectionChanged.connect(self.tarihdegistir)
        self.aylikliste()
        self.ui.btnSil.clicked.connect(lambda: self.kayitsil())
        self.ui.chkToplam.stateChanged.connect(self.checkbox_kontrol)
        self.checkbox_kontrol()  # İlk başta checkbox durumuna göre işlevi çağır
        self.ui.btnGuncelle.clicked.connect(self.guncelle)
        self.notlarim=hizli_Not()
        self.gelirlistesi=GelirListe()
        self.ui.btnGelirListe.clicked.connect(self.GelirListeGoruntule)
        self.ui.btnNot.clicked.connect(self.not_listele)
        self.ui.chkButunKayitlar.stateChanged.connect(self.checkbox_kayitkontrol)
        self.ui.btnGelirKayit.clicked.connect(self.GelirKayit)
        # self.gunceldeger'i QLabel'e aktar


        # self.dolar_goruntule()


    def GelirListeGoruntule(self):
        self.gelirlistesi.show()

    def checkbox_kayitkontrol(self):
        if self.ui.chkButunKayitlar.isChecked():
            self.HepsiniGoster()
        else:
            self.aylikliste()


    def checkbox_kontrol(self):
        if self.ui.chkToplam.isChecked():
            self.ayliktoplam()
        else:

            self.aylikliste()

    def not_listele(self):
        self.notlarim.show()
        self.notlarim.not_listelekon()

    def tablo_liste(self):
        self.listepencere.show()

    def tarihdegistir(self):
        self.tarih = self.ui.kayitTarih.selectedDate().toString("yyyy-MM-dd")

    from PyQt5.QtCore import QDate

    def ayliktoplam(self):
        self.ui.tblYeni.setColumnWidth(0, 65)
        self.ui.tblYeni.setColumnWidth(1, 100)
        self.ui.tblYeni.setColumnWidth(2, 100)
        self.ui.tblYeni.setColumnWidth(3, 100)
        self.ui.tblYeni.setColumnWidth(4, 100)
        self.ui.tblYeni.setColumnWidth(5, 90)
        self.ui.tblYeni.clear()
        self.ui.tblYeni.setRowCount(0)  # Tabloyu temizle
        self.ui.tblYeni.setHorizontalHeaderLabels(
            ("Tarih", "Toplam Market", "Toplam Faturalar", "Toplam Diğer", "Açıklama", "Toplam Harcama"))
        # self.ui.tblYeni.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Bulunduğumuz ayın ilk ve son günlerini hesapla
        simdiki_ayin_ilk_gunu = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1)
        simdiki_ayin_son_gunu = QDate(QDate.currentDate().year(), QDate.currentDate().month(),
                                      QDate.currentDate().daysInMonth())

        # ayin_ilk_gunu ve ayin_son_gunu değişkenlerini str tipine dönüştür
        ayin_ilk_gunu = simdiki_ayin_ilk_gunu.toString("yyyy-MM-dd")
        ayin_son_gunu = simdiki_ayin_son_gunu.toString("yyyy-MM-dd")

        # Bulunduğumuz aya ait kayıtları veritabanından sorgula
        baglanti = sqlite3.connect("veriler1.db")
        islem = baglanti.cursor()

        sorgu = """
            SELECT
                tarih,
                SUM(market) AS ToplamMarket,
                SUM(fatura) AS ToplamFaturalar,
                SUM(harcama) AS ToplamDiğer,
                GROUP_CONCAT(aciklama, ', ') AS Aciklama
            FROM muhasebe
            WHERE tarih BETWEEN ? AND ?
            GROUP BY tarih
        """

        islem.execute(sorgu, (ayin_ilk_gunu, ayin_son_gunu))

        # Sonuçları tabloya ekle
        kayitlar = islem.fetchall()
        for satir in kayitlar:
            # Tarihi doğru formata dönüştür
            tarih_formatli = QDate.fromString(satir[0], "yyyy-MM-dd").toString("dd-MM-yyyy")

            # TL sembolünü Toplam Market, Toplam Faturalar ve Toplam Diğer sütunlarına ekleyin
            market_item = QTableWidgetItem(f"{satir[1]} TL")
            fatura_item = QTableWidgetItem(f"{satir[2]} TL")
            diger_item = QTableWidgetItem(f"{satir[3]} TL")

            self.ui.tblYeni.insertRow(self.ui.tblYeni.rowCount())
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 0, QTableWidgetItem(tarih_formatli))
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 1, market_item)
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 2, fatura_item)
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 3, diger_item)
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 4, QTableWidgetItem(satir[4]))

            # Toplam Harcamayı hesapla ve göster
            toplam_harcama = satir[1] + satir[2] + satir[3]
            harcama_item = QTableWidgetItem(f"{toplam_harcama} TL")
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 5, harcama_item)

        baglanti.close()


    def GelirKayit(self):
        baglanti = sqlite3.connect("veriler1.db")
        islem = baglanti.cursor()

        kayit = "INSERT INTO gelirler (id,tarih,kaynak,miktar,aciklama) VALUES (NULL,?,?,?,?)"
        kaynak = self.ui.cmbKaynak.currentText()
        miktar = self.ui.lneGelirMiktar.text().strip()
        aciklama = self.ui.lneGelirAciklama.text().strip()

        if miktar and kaynak:
            try:
                islem.execute(kayit, (self.tarih, kaynak, miktar, aciklama))
                baglanti.commit()
                print("Kayıt başarıyla yapıldı.")
            except Exception as e:
                print(f"Hata: {e}")
        else:
            print("Miktar ve kaynak bilgileri boş olamaz!.")

        self.ui.cmbKaynak.setCurrentIndex(-1)
        self.ui.lneGelirMiktar.clear()
        self.ui.lneGelirAciklama.clear()



    def HepsiniGoster(self):
            self.ui.tblYeni.setColumnWidth(0, 0)
            self.ui.tblYeni.setColumnWidth(1, 65)
            self.ui.tblYeni.setColumnWidth(5, 200)
            self.ui.tblYeni.clear()
            self.ui.tblYeni.setRowCount(0)  # Tabloyu temizle
            self.ui.tblYeni.setHorizontalHeaderLabels(
                ("ID", "Tarih", "Toplam Market", "Toplam Faturalar", "Toplam Diğer", "Açıklama"))
            # self.ui.tblYeni.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Tüm kayıtları veritabanından sorgula
            baglanti = sqlite3.connect("veriler1.db")
            islem = baglanti.cursor()

            sorgu = """
                          SELECT 
                              id,
                              tarih, 
                              market AS ToplamMarket,
                              fatura AS ToplamFaturalar, 
                              harcama AS ToplamDiğer,
                              aciklama AS Aciklama
                          FROM muhasebe 
                          ORDER BY tarih ASC  -- Verileri tarihe göre sırala (artan)
                      """

            islem.execute(sorgu)

            # Sonuçları tabloya ekle
            kayitlar = islem.fetchall()
            for satir in kayitlar:
                # Tarihi doğru formata dönüştür
                tarih_formatli = QDate.fromString(satir[1], "yyyy-MM-dd").toString("dd-MM-yyyy")

                # ID, Tarih, Toplam Market, Toplam Faturalar, Toplam Diğer ve Açıklama sütunlarını tabloya ekle
                self.ui.tblYeni.insertRow(self.ui.tblYeni.rowCount())
                self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 0, QTableWidgetItem(str(satir[0])))
                self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 1, QTableWidgetItem(tarih_formatli))

                if isinstance(satir[2], str) and satir[2][-2:] == "TL":
                    market_item = QTableWidgetItem(satir[2])
                else:
                    market_item = QTableWidgetItem(f"{str(satir[2])} TL")

                # Aynı işlemi fatura ve diğer öğeler için de tekrarlayın
                if isinstance(satir[3], str) and satir[3][-2:] == "TL":
                    fatura_item = QTableWidgetItem(satir[3])
                else:
                    fatura_item = QTableWidgetItem(f"{str(satir[3])} TL")

                if isinstance(satir[4], str) and satir[4][-2:] == "TL":
                    diger_item = QTableWidgetItem(satir[4])
                else:
                    diger_item = QTableWidgetItem(f"{str(satir[4])} TL")

                self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 2, market_item)
                self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 3, fatura_item)
                self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 4, diger_item)

                self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 5, QTableWidgetItem(satir[5]))

            baglanti.close()



    def aylikliste(self):
        self.ui.tblYeni.setColumnWidth(0, 0)
        self.ui.tblYeni.setColumnWidth(1, 65)
        self.ui.tblYeni.setColumnWidth(5, 200)
        self.ui.tblYeni.clear()
        self.ui.tblYeni.setRowCount(0)  # Tabloyu temizle
        self.ui.tblYeni.setHorizontalHeaderLabels(
            ("ID", "Tarih", "Toplam Market", "Toplam Faturalar", "Toplam Diğer", "Açıklama"))
       # self.ui.tblYeni.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        # Bulunduğumuz ayın ilk ve son günlerini hesapla
        simdiki_ayin_ilk_gunu = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1)
        simdiki_ayin_son_gunu = QDate(QDate.currentDate().year(), QDate.currentDate().month(),
                                      QDate.currentDate().daysInMonth())

        # ayin_ilk_gunu ve ayin_son_gunu değişkenlerini str tipine dönüştür
        ayin_ilk_gunu = simdiki_ayin_ilk_gunu.toString("yyyy-MM-dd")
        ayin_son_gunu = simdiki_ayin_son_gunu.toString("yyyy-MM-dd")

        # Bulunduğumuz aya ait kayıtları veritabanından sorgula
        baglanti = sqlite3.connect("veriler1.db")
        islem = baglanti.cursor()

        sorgu = """
                    SELECT 
                        id,
                        tarih, 
                        market AS ToplamMarket,
                        fatura AS ToplamFaturalar, 
                        harcama AS ToplamDiğer,
                        aciklama AS Aciklama
                    FROM muhasebe 
                    WHERE tarih BETWEEN ? AND ?
                """

        islem.execute(sorgu, (ayin_ilk_gunu, ayin_son_gunu))

        # Sonuçları tabloya ekle
        kayitlar = islem.fetchall()
        for satir in kayitlar:
            # Tarihi doğru formata dönüştür
            tarih_formatli = QDate.fromString(satir[1], "yyyy-MM-dd").toString("dd-MM-yyyy")

            # ID, Tarih, Toplam Market, Toplam Faturalar, Toplam Diğer ve Açıklama sütunlarını tabloya ekle
            self.ui.tblYeni.insertRow(self.ui.tblYeni.rowCount())
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 0, QTableWidgetItem(str(satir[0])))
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 1, QTableWidgetItem(tarih_formatli))

            if isinstance(satir[2], str) and satir[2][-2:] == "TL":
                market_item = QTableWidgetItem(satir[2])
            else:
                market_item = QTableWidgetItem(f"{str(satir[2])} TL")

            # Aynı işlemi fatura ve diğer öğeler için de tekrarlayın
            if isinstance(satir[3], str) and satir[3][-2:] == "TL":
                fatura_item = QTableWidgetItem(satir[3])
            else:
                fatura_item = QTableWidgetItem(f"{str(satir[3])} TL")

            if isinstance(satir[4], str) and satir[4][-2:] == "TL":
                diger_item = QTableWidgetItem(satir[4])
            else:
                diger_item = QTableWidgetItem(f"{str(satir[4])} TL")

            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 2, market_item)
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 3, fatura_item)
            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 4, diger_item)

            self.ui.tblYeni.setItem(self.ui.tblYeni.rowCount() - 1, 5, QTableWidgetItem(satir[5]))

        baglanti.close()
    def kayit_yap(self):
        baglanti = sqlite3.connect("veriler1.db")
        islem = baglanti.cursor()

        kayit = "INSERT INTO muhasebe (id, tarih, market, fatura, harcama, aciklama) VALUES (NULL,?,?,?,?,?)"
        market = self.ui.lneMarket.text().strip()
        fatura = self.ui.lneFatura.text().strip()
        harcama = self.ui.lneHarcama.text().strip()
        aciklama = self.ui.lneAciklama.text().strip()

        try:
            if market and not fatura and not harcama:
                islem.execute(kayit, (self.tarih, float(market), 0, 0, aciklama))
            elif not market and fatura and not harcama:
                islem.execute(kayit, (self.tarih, 0, float(fatura), 0, aciklama))
            elif not market and not fatura and harcama:
                islem.execute(kayit, (self.tarih, 0, 0, float(harcama), aciklama))
            elif market and fatura and not harcama:
                islem.execute(kayit, (self.tarih, float(market), float(fatura), 0, aciklama))
            elif market and not fatura and harcama:
                islem.execute(kayit, (self.tarih, float(market), 0, float(harcama), aciklama))
            elif not market and fatura and harcama:
                islem.execute(kayit, (self.tarih, 0, float(fatura), float(harcama), aciklama))
            elif market and fatura and harcama:
                islem.execute(kayit, (self.tarih, float(market), float(fatura), float(harcama), aciklama))
            else:
                print("En az bir alanın sayısal değer içermesi gerekiyor. Kayıt yapılmadı.")

            baglanti.commit()
            print("Kayıt başarıyla yapıldı.")
        except ValueError as ve:
            print(f"Hata oluştu: {ve}")
            print("Lütfen geçerli sayısal değerler girin.")
            # Hata durumunda yapılacak diğer işlemleri buraya ekleyebilirsiniz
        except Exception as e:
            print(f"Diğer bir hata oluştu: {e}")
            # Hata durumunda yapılacak diğer işlemleri buraya ekleyebilirsiniz

        self.ui.lneMarket.clear()
        self.ui.lneFatura.clear()
        self.ui.lneHarcama.clear()
        self.ui.lneAciklama.clear()
        self.aylikliste()  # Tabloyu güncelle
        baglanti.close()

    def kayitsil(self):
        selected_item = self.ui.tblYeni.currentItem()

        if not selected_item:
            # Eğer hiç hücre seçili değilse işlem yapma
            return

        # Kullanıcının seçtiği hücrenin bulunduğu satırı al
        selected_row = selected_item.row()

        # Seçilen satırın id değerini al
        id_sil_str = self.ui.tblYeni.item(selected_row, 0).text()

        # Seçilen id'ye göre veritabanından ilgili kaydı silen SQL sorgusu
        sorgu = "DELETE FROM muhasebe WHERE id = ?"

        try:
            # Seçilen id'yi integer'a çevir
            id_sil = int(id_sil_str)

            # Kullanıcıya onay mesajı göster
            onay = QMessageBox.question(self, "Onay", "Seçili kaydı silmek istediğinizden emin misiniz?",
                                        QMessageBox.Yes | QMessageBox.No)

            if onay == QMessageBox.No:
                # Kullanıcı "Hayır" derse işlemi iptal et
                return

            baglanti = sqlite3.connect("veriler1.db")
            islem = baglanti.cursor()

            islem.execute(sorgu, (id_sil,))
            baglanti.commit()

            if islem.rowcount > 0:
                # Eğer bir veya daha fazla satır silindi ise
                QMessageBox.information(self, "Başarılı", "Kayıt başarıyla silindi.")
            else:
                # Eğer hiç satır silinmediyse
                QMessageBox.warning(self, "Uyarı", "Seçili kriterlere sahip kayıt bulunamadı.")

        except ValueError:
            # Geçersiz id değeri durumunda bir mesaj göster
            QMessageBox.warning(self, "Hata", "Geçersiz id değeri.")

        except Exception as e:
            # Diğer hata durumlarında bir mesaj göster
            QMessageBox.warning(self, "Hata", f"Hata oluştu: {str(e)}")

        finally:
            # Veritabanı bağlantısını kapat
            baglanti.close()

        self.aylikliste()

    from datetime import datetime

    from datetime import datetime

    from datetime import datetime

    from datetime import datetime

    def guncelle(self):
        selected_item = self.ui.tblYeni.currentItem()

        if selected_item is None:
            # Eğer hiç hücre seçili değilse işlem yapma
            return

        # Kullanıcının seçtiği hücrenin bulunduğu satırı al
        selected_row = selected_item.row()

        try:
            baglanti = sqlite3.connect("veriler1.db")
            islem = baglanti.cursor()

            try:
                id_sutun_indeksi = 0  # id sütununun indeksi
                market_sutun_indeksi = 2  # market sütununun indeksi
                fatura_sutun_indeksi = 3  # fatura sütununun indeksi
                harcama_sutun_indeksi = 4  # harcama sütununun indeksi
                aciklama_sutun_indeksi = 5  # aciklama sütununun indeksi
                tarih_sutun_indeksi = 1  # tarih sütununun indeksi

                id_guncelle = int(self.ui.tblYeni.item(selected_row, id_sutun_indeksi).text())
            except ValueError:
                print(f"Hata: Geçersiz ID değeri: '{self.ui.tblYeni.item(selected_row, id_sutun_indeksi).text()}'")
                QMessageBox.warning(self, "Hata", "Geçersiz ID değeri. ID bir tam sayı olmalıdır.")
                return

            # Kullanıcının girdiği değerleri al
            market = self.ui.tblYeni.item(selected_row, market_sutun_indeksi).text()
            fatura = self.ui.tblYeni.item(selected_row, fatura_sutun_indeksi).text()
            harcama = self.ui.tblYeni.item(selected_row, harcama_sutun_indeksi).text()
            aciklama = self.ui.tblYeni.item(selected_row, aciklama_sutun_indeksi).text()
            tarih_text = self.ui.tblYeni.item(selected_row, tarih_sutun_indeksi).text()

            try:
                tarih = datetime.strptime(tarih_text, "%d-%m-%Y")
            except ValueError:
                print(f"Hata: Geçersiz tarih formatı: '{tarih_text}'")
                QMessageBox.warning(self, "Hata", "Geçersiz tarih formatı. Tarih 'dd-mm-yyyy' formatında olmalıdır.")
                return

            # Seçilen satırın tüm verilerini güncelleme
            sorgu = "UPDATE muhasebe SET market = ?, fatura = ?, harcama = ?, aciklama = ?, tarih = ? WHERE id = ?"
            islem.execute(sorgu, (market, fatura, harcama, aciklama, tarih.strftime("%Y-%m-%d"), id_guncelle))

            baglanti.commit()

            if islem.rowcount > 0:
                # Eğer bir veya daha fazla satır güncellendi ise
                QMessageBox.information(self, "Başarılı", "Kayıt başarıyla güncellendi.")
            else:
                # Eğer hiç satır güncellenmediyse
                QMessageBox.warning(self, "Uyarı", "Seçilen kriterlere sahip kayıt bulunamadı.")

        except Exception as e:
            # Hata durumunda bir mesaj göster
            QMessageBox.warning(self, "Hata", f"Hata oluştu: {str(e)}")

        finally:
            baglanti.close()

        self.aylikliste()