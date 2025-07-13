import pandas as pd
import re

# Dosya yolunuzu güncelleyin
tsv_file_path = 'C:/{your_path}'

try:
    df = pd.read_csv(tsv_file_path, sep='\t', header=0, na_values=[':', ': '])
    print("Dosya başarıyla okundu.")

except Exception as e:
    print(f"Dosya okuma hatası: {e}")
    print("Lütfen dosya yolunuzun doğru olduğundan ve dosyanın bozuk olmadığından emin olun.")


df = df.rename(columns={df.columns[0]: 'category_keys'})

df.columns = [col.strip() for col in df.columns]

print("\nSütun Adları Temizlendi. İlk 5 satır:")
print(df.head())

year_columns = [col for col in df.columns if col.isdigit() and len(col) == 4]

for col in year_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^\d.]', '', x) if pd.notna(x) else x)
        df[col] = df[col].replace('', pd.NA)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    else:
        print(f"Uyarı: '{col}' sütunu DataFrame'de bulunamadı.")


print("\nYıl Sütunları Temizlendi ve Sayısallaştırıldı. DataFrame Bilgileri:")
df.info()
print("\nTemizlenmiş Yıl Sütunları ile İlk 5 Satır:")
print(df.head())

df_long = df.melt(id_vars=['category_keys'], value_vars=year_columns, var_name='year', value_name='registration_count')

df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce').astype('Int64')


print("\nUzun Formata Dönüştürüldü. İlk 5 satır:")
print(df_long.head())
print("\nUzun Formata Dönüştürülmüş DataFrame Bilgileri:")
df_long.info()


df_long[['freq', 'unit', 'mot_nrg', 'engine', 'geo']] = df_long['category_keys'].str.split(',', expand=True)

df_long = df_long.drop(columns=['category_keys'])

df_long = df_long[['freq', 'unit', 'mot_nrg', 'engine', 'geo', 'year', 'registration_count']]


print("\n'category_keys' Parçalandı ve Sütun Sırası Düzenlendi. İlk 5 satır:")
print(df_long.head())
print("\nSon DataFrame Bilgileri:")
df_long.info()

output_csv_path = 'C:/Users/dogan/Downloads/clean_new_car_registrations_long_format.csv'
df_long.to_csv(output_csv_path, index=False, sep=',', encoding='utf-8', na_rep='')

print(f"\nTemizlenmiş ve uzun formata dönüştürülmüş veri buraya kaydedildi: {output_csv_path}")