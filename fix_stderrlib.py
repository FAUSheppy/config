import os

rc = open("zshrc",'w+')
old = open("zshrc_old",'r')
for line in old:
        if line.startswith("LD_PRELOAD="):
                line = "LD_PRELOAD='"+os.getcwd()+"'\n"
        rc.write(line)
