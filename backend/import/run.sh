cd /tmp
wget -o archive.zip $ARCHIVE_URL
unzip archive.zip
python3 /backend/batch_insert.py $FILE_NAME $ARCHIVE_CODE