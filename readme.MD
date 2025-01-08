# **Veri Tabanı Projesi**

## **Proje Hakkında**
Bu proje, etkili ve güvenilir bir veri tabanı sistemi oluşturmayı amaçlamaktadır. Proje kapsamında temel veri tabanı yönetimi işlevleri uygulanmış ve SQL sorguları ile işlemler gerçekleştirilmiştir.

---

## **Özellikler**
- Tabloların oluşturulması ve düzenlenmesi.
- Veri ekleme, güncelleme, silme işlemleri.
- Referans bütünlüğü (Referential Integrity) kurallarının uygulanması.
- SQL ile veri sorgulama ve filtreleme işlemleri.
- Yerleşik SQL fonksiyonlarının kullanımı ile gelişmiş analiz.
- Abonelik yönetimi (bireysel ve kurumsal aboneler).
- Fatura oluşturma ve doğrulama.
- Karbon emisyonu hesaplama.
- Veri bütünlüğünü sağlayan tetikleyiciler.
- Veri sorgulama için özel SQL fonksiyonları ve görünümler.

---

## **Dosya Yapısı**
- `greensaverdb-schema.sql`: Tabloların oluşturulması ve verilerin işlenmesi için kullanılan ana SQL dosyası.
- `greensaverdb-insert.sql`: Çeşitli sorguların yer aldığı SQL dosyası.
- `README.md`: Proje ile ilgili bilgilerin yer aldığı doküman.
- `main.py`: PyQt5 ile oluşturulmuş olan GUI uygulaması.
- `database.py`: Veritabanı bağlantısını sağlayan sınıf.
- `gui.py`: GUI ile ilgili kodların yer aldığı dosya.   

---

## **Kullanım**
1. SQL dosyalarını bir veri tabanı yönetim sistemine (ör. MySQL, PostgreSQL) yükleyin.
2. `greensaverdb-schema.sql` dosyasını çalıştırarak temel tabloları oluşturun.
3. `greensaverdb-insert.sql` dosyasını kullanarak veri üzerinde işlemler yapabilirsiniz.
4. `main.py` dosyasını çalıştırarak uygulamayı başlatın.
---

## **Gereksinimler**
- Python 3.x
- PyQt5
- PostgreSQL

---

## **Proje Durumu**
Bu proje şu anda temel veri tabanı işlevlerini desteklemektedir. İleride daha gelişmiş özellikler eklenmesi planlanmaktadır.

### **Proje Kodlama Durumu**
Aşağıdaki fonksiyonlar ve tetikleyiciler projede kullanılmaktadır. Tamamlananları işaretleyebilirsiniz:

- [X] **`insert_individual_subscriber`**: Bireysel abone ekleme fonksiyonu.
- [X] **`insert_corporate_subscriber`**: Kurumsal abone ekleme fonksiyonu.
- [X] **`insert_invoice`**: Fatura ekleme fonksiyonu.
- [X] **`invoice_collision_func`**: Aynı tarih ve türde fatura ekleme kontrolünü sql içinde yapan fonksiyon.
- [X] **`invoice_collision_trig`**: Fatura çakışma kontrolü için sql içinde yapan tetikleyici.
- [X] **`calculate_carbon_emission`**: Karbon emisyonu hesaplama fonksiyonu.
- [ ] **`all_sub_view`**: Admin sayfasında Abonelerin birleştirilmiş görünümünü gösteren fonksiyon.
- [X] **`trig_invoiceInsertControl`**: Abonelik kontrolü için tetikleyici fonksiyon.
- [X] **`get_all_individualInvoices`**: Bireysel abonenin tüm faturalarını listeleme fonksiyonu.
- [X] **`get_all_corporateInvoices`**: Kurumsal abonenin tüm faturalarını listeleme fonksiyonu.
- [X] **`get_invoice`**: Abone numarasına göre fatura bilgilerini getirme fonksiyonu.
- [X] **`update_password`**: Kullanıcı şifresini güncelleme fonksiyonu.
- [X] **`delete_invoice`**: Fatura silme fonksiyonu.
- [X] **`update_invoice`**: Fatura güncelleme fonksiyonu.
- [X] **`get_top_spenders`**: Admin panelinde belirtilen eşik değerinden fazka fatura ödeyen aboneleri listeleme fonksiyonu.
---

## **Katkıda Bulunma**
Katkılarından dolayı ekip arkadaşlarım Burakhan Saruhan ve Alihan Uludağ'a teşekkür ederim. Projemize katkıda bulunmak isterseniz lütfen bir "Pull Request" gönderin veya [e-posta adresinizi buraya ekleyin].

---

## **Lisans**
Bu proje MIT Lisansı ile lisanslanmıştır.
