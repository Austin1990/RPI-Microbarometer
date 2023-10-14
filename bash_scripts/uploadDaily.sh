HOST='ftp_address_of_remote_site'
USER='  login_id  '
PASSWD=' your pwd'


ftp -p -n -v $HOST << EOT
ascii
user $USER $PASSWD
prompt
cd ....remote website directory...../projects/microbarometer/PlotsA
lcd /home/GeoPhysics/Plots
mput *.svg
rm *.svg


bye
EOT
