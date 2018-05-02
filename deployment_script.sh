# Ping all devices of the network
nmap -sn 10.33.120.1-255

# Find all Raspberries and display their ip address
raspberries_ip = $(arp | grep 'b8:27:eb' | awk '{print $1}')
echo $raspberries_ip