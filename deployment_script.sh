# Ping all devices of the network 
nmap -sn 10.33.120.1-255 
 
# Find all Raspberries and send them messages in order to update every one 
raspberries_ip=$(arp | grep 'b8:27:eb' | awk '{print $1}') 
 
for ip in $raspberries_ip 
do 
    mosquitto_pub -h 10.33.120.194 -p 1883 -m "Update yourself please" -t "DCOP/$ip" 
    echo "Update msg sent to DCOP/$ip" 
done