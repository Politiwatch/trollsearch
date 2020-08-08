cd /tmp
wget -O archive.zip $ARCHIVE_URL
md5sum archive.zip
unzip -o archive.zip
python3 /backend/batch_insert.py $FILE_NAME $ARCHIVE_CODE