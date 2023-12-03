import os
import sys

dir_name = None
mod = None

try:
    dir_name = sys.argv[1] + "/"
    mod = int(sys.argv[2])
    print("Dir: \t", os.getcwd() + "/" + dir_name)
    print("Mod: \t", mod)

    for file in os.listdir(dir_name):
        filename = os.fsdecode(file)
        num = int(filename.split(".")[0])
        if num % mod == 0:
            print(num)
            continue
        else:
            print(num)
            os.remove(dir_name + filename)
except:
    if dir_name is None or mod is None:
        print("MISSING INPUT---------------------------------------------------")
        print("Example usage: clean_models.py \t models1 \t 1000000")
        print("Example usage: \t\t\t dir_name \t value to mod by ")
        print("MISSING INPUT---------------------------------------------------")
    else:
        print("somthin else went wrong")
