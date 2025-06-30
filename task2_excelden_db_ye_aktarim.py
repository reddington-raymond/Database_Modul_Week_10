import os
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL bağlantı ayarları
db_user = 'postgres'
db_password = 'POSTGRES'
db_host = 'localhost'
db_port = '5432'
db_name = 'crm'

# SQLAlchemy engine oluştur
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Excel dosyalarının bulunduğu klasör
excel_klasor = 'excel_tablolarim'

# Aktarılacak dosya isimleri
dosyalar = [
    'Basvurular.xlsx',
    'Kullanicilar.xlsx',
    'Kursiyerler.xlsx',
    'MentorGorusme.xlsx',
    'ProjeTakip.xlsx'
]

for dosya in dosyalar:
    dosya_yolu = os.path.join(excel_klasor, dosya)
    tablo_adi = os.path.splitext(dosya)[0].lower()  # Tablo adı: dosya adı küçük harfli ve uzantısız
    df = pd.read_excel(dosya_yolu)
    df.to_sql(tablo_adi, engine, if_exists='replace', index=False)
    print(f"{dosya} dosyasındaki veriler '{tablo_adi}' tablosuna aktarıldı.")

print("Tüm dosyalar başarıyla PostgreSQL'e aktarıldı.")