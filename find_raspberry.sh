# Find all Raspberries of the network
# and display their ip address
arp | grep 'b8:27:eb' | awk '{print $1}'