# Menggunakan base image Python
FROM python:3.9

# Menyalin kode aplikasi ke dalam kontainer
COPY . /app
WORKDIR /app

# Menginstal dependensi yang diperlukan
RUN pip install -r requirements.txt

EXPOSE 3000

# Menjalankan aplikasi
CMD [ "python", "TUBESEAI.py" ]
 
