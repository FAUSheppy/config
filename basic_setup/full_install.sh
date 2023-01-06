su
mv ~/.config/basic_setup/sources.list /etc/apt/sources.list
apt update
apt upgrade --asume-yes
cat ../other/package_list_full.txt | while read line
do
    apt install --no-install-recommends --assume-yes $line
done
exit
