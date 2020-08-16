import os
import sys

def fixEncoding(file_name):

    final_name = 'Monsterliste_fixedEncoding.csv'
    if os.path.exists(final_name):
        os.remove(final_name)


    with open(file_name, 'r', encoding='cp1252') as f1:
        lines = f1.read()
        f2 = open(final_name, 'w', encoding='utf-8')
        f2.write(lines)
        f2.close()
    #os.remove(file_name)
    print("All done and file saved as: "+ final_name)

def fixString(input):
    temp = input.encode('cp1252')
    result = temp.decode('cp1252')
    return result

