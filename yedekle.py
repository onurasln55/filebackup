import paramiko
import logging
from datetime import datetime
import os

# SSH bağlantısını kurmak için gerekli bilgiler
hostname = ""#sunucu adresi girilir
username = ""#kullanıcı adı 
password = ""#şifre girilir.

# Log dosyasının ayarları
logging.basicConfig(filename="transfer.log", level=logging.INFO, encoding="utf-8")

try:
    # SSH client nesnesi oluştur
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    # Dosyaları karşıya yüklemek için SFTP nesnesi oluştur
    sftp = client.open_sftp()

    # Dosya listesini al
    with open("files_list.txt", "r") as f:
        files = [line.strip() for line in f]

    # Dosyaları karşıya yükle
    current_time = datetime.now().strftime("%Y-%m-%d %H.%M")
    remote_path = "/tmp/mnt/4AEE97C5EE97A7A9/"+username+"/"+current_time
    try:
        sftp.mkdir(remote_path)
    except IOError:
        pass
    for file in files:
        local_path = os.path.normpath(file)
        file_name = os.path.basename(file)
        sftp.put(local_path, remote_path + "/" + file_name)

    # Bağlantıyı kapat
    sftp.close()
    client.close()
    current_time = datetime.now()
    logging.info("[{}] Dosya Transferi Başarılı".format(current_time))

except Exception as e:
    current_time = datetime.now()
    logging.error("[{}] Dosya Transferi Başarısız: {}".format(current_time, e))
 
