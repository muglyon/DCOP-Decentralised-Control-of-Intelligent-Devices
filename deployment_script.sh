# Find all Raspberries of the network
# and display their ip address
raspberries_ip = ($(arp | grep 'b8:27:eb' | awk '{print $1}'))
echo $raspberries_ip