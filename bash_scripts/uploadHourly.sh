HOST='ftp_address_of_remote_site'
USER='  login_id  '
PASSWD=' your pwd'

ftp -p -n -v $HOST << EOT
ascii
user $USER $PASSWD
prompt
cd ....remote website directory...../projects/microbarometer/Plots
ls -la
put /home/ian/GeoPhysics/Plots/today_pressure.svg today_pressure.svg
put /home/ian/GeoPhysics/Plots/weekly_pressure.svg weekly_pressure.svg
put /home/ian/GeoPhysics/Plots/prev168hrs_pressure.svg prev168hrs_pressure.svg
put /home/ian/GeoPhysics/Plots/prev168hrs_temperature.svg prev168hrs_temperature.svg
bye
EOT


