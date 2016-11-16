rmmod usbhid
echo "removed"
modprobe usbhid quirks=0x1a2c:0x0027:0x20000000
echo "DONE"
