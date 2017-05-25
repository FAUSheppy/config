CONF_DIR=~/.config/atlantislaptop

#system config
cp $CONF_DIR/openvpn /etc/default/
cp $CONF_DIR/openfaupn.conf /etc/openvpn/
cp $CONF_DIR/ssh_config /etc/ssh/
cp $CONF_DIR/sudoers /etc/
cp $CONF_DIR/active /etc/wicd/encryption/templates/
cp $CONF_DIR/edurom /etc/wicd/encryption/templates/

#scripts in path
cp $CONF_DIR/openvpn_cip.sh /usr/bin/
cp $CONF_DIR/stopvpn.sh /usr/bin/

gpg --output /etc/openvpn/auth.txt -d auth.txt.gpg
chmod 500 /etc/openvpn/auth.txt
