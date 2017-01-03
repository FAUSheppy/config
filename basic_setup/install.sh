su
cat ../other/package_list_full.txt | while read line
do
        apt install --no-install-recommends --assume-yes $line
done
exit
