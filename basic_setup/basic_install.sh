apt update
apt upgrade --asume-yes
cat ../other/package_list_desktop_essential.txt | while read line
do
    apt install --no-install-recommends --assume-yes $line
done
exit
