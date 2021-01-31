OperationTb = {"ADD": "18", "MUL": "20", "DIV": "24", "COMP": "28", "LDA": "00", "LDX": "04", "LDCH": "50", "LDL": "08", "JEQ": "30", "JGT": "34", "JLT": "38", "JSUB": "48",
               "RSUB": "4C", "TIX": "2C", "STA": "0C", " STCH": "54", "STX": "10", "AND": "40", "OR": "44", "TD": "E0", "WD": "DC", "J": "3C", "STL": "14", "RD": "D8", "SUB": "1C"}
Var_Ptr = {}
Assembly_file = open("Program Examples/input2.txt", "r")
ln1 = Assembly_file.readline()
print("\t\t     "+ln1.lstrip())
tmp_ln = ln1.strip().split()
MemPtr = tmp_ln[2]
start = MemPtr
ln_cnt = 5
inter = []
ind_cnt = 0
lines = Assembly_file.readlines()
for i in lines:
    ind_cnt += 1
for i in range(ind_cnt):
    inter.append([])
ln_ind = 0
for i in lines:
    tmp_ln = i.strip().split()
    if(tmp_ln[0] == '.'):
        continue
    else:
        inter[ln_ind].append(str(ln_cnt))
        inter[ln_ind].append("\t")
        inter[ln_ind].append(str(hex(int(MemPtr, 16)))[2:])
        inter[ln_ind].append(i)
        ln_ind += 1
        if len(tmp_ln) >= 3 and not(tmp_ln[0] in OperationTb.keys()):
            Var_Ptr[tmp_ln[0]] = '{:>04}'.format(hex(int(MemPtr, 16))[2:])
        if tmp_ln[0] in OperationTb.keys() or tmp_ln[1] in OperationTb.keys():
            MemPtr = str(hex(int(MemPtr, 16) + 3))
        elif tmp_ln[1] == "WORD" and len(tmp_ln) >= 3:
            MemPtr = str(hex(int(MemPtr, 16) + 3))
        elif tmp_ln[1] == "RESW" and len(tmp_ln) >= 3:
            tmp = 3 * int(tmp_ln[2])
            MemPtr = str(hex(int(MemPtr, 16) + tmp))
        elif tmp_ln[1] == "RESB" and len(tmp_ln) >= 3:
            MemPtr = str(hex(int(MemPtr, 16)+int(tmp_ln[2])))
        elif tmp_ln[1] == "BYTE" and len(tmp_ln) >= 3:
            if tmp_ln[2][0] == "X":
                MemPtr = str(hex(int(MemPtr, 16)+int((len(tmp_ln[2])-3)/2)))
            elif tmp_ln[2][0] == "C":
                MemPtr = str(hex(int(MemPtr, 16)+(len(tmp_ln[2])-3)))
        ln_cnt += 5

print("\n\n\n")

for i in range(ln_ind - 1):
    tmp_str_lst = (inter[i][3]).strip().split()
    if len(tmp_str_lst) == 3:
        if tmp_str_lst[0] in OperationTb.keys():
            tmp_str = OperationTb[tmp_str_lst[0]] + \
                str(hex(int("8000", 16) +
                        int(Var_Ptr[tmp_str_lst[1]], 16)))[2:]
            print(inter[i][0], inter[i][1], '{:>04}'.format(
                inter[i][2]), inter[i][3] + "\t", tmp_str + "\n")
            continue
        if tmp_str_lst[2] in Var_Ptr.keys():
            tmp_str = OperationTb[tmp_str_lst[1]] + Var_Ptr[tmp_str_lst[2]]
            print(inter[i][0], inter[i][1], '{:>04}'.format(
                inter[i][2]), inter[i][3] + "\t", tmp_str + "\n")
        else:
            if tmp_str_lst[1] == "BYTE":
                tmp_str = " "
                chr_lst = [c.encode("utf-8").hex() for c in tmp_str_lst[2]]
                for no in chr_lst:
                    tmp_str += str(no)
                print(inter[i][0], inter[i][1], '{:>04}'.format(
                    inter[i][2]), inter[i][3] + "\t", tmp_str[5:11] + "\n")
            elif tmp_str_lst[1] == "WORD":
                tmp_str = str(hex(int(tmp_str_lst[2])))[2:]
                print(inter[i][0], inter[i][1], '{:>04}'.format(
                    inter[i][2]), inter[i][3] + "\t", '{:>06}'.format(tmp_str.zfill(7-len(tmp_str))) + "\n")
            else:
                print(inter[i][0], inter[i][1], '{:>04}'.format(
                    inter[i][2]), inter[i][3]+"\n")
    elif len(tmp_str_lst) == 2 and (tmp_str_lst[0] != "END"):
        tmp_str = OperationTb[tmp_str_lst[0]] + Var_Ptr[tmp_str_lst[1]]
        print(inter[i][0], inter[i][1], '{:>04}'.format(
            inter[i][2]), inter[i][3] + "\t", tmp_str + "\n")
    elif len(tmp_str_lst) == 1 and tmp_str_lst[0] in OperationTb.keys():
        tmp_str = OperationTb[tmp_str_lst[0]]
        print(inter[i][0], inter[i][1], '{:>04}'.format(
            inter[i][2]), inter[i][3] + "\t", tmp_str + "0"*(6 - len(tmp_str)) + "\n")
    else:
        tmp_str = OperationTb[tmp_str_lst[1]] + \
            str(hex(int("8000", 16) + int(Var_Ptr[tmp_str_lst[2]], 16)))[2:]
        print(inter[i][0], inter[i][1], '{:>04}'.format(
            inter[i][2]), inter[i][3] + "\t", tmp_str + "\n")


print(inter[ln_ind - 1][0], inter[ln_ind - 1][1],
      inter[ln_ind - 1][2], inter[ln_ind - 1][3])
Assembly_file.close()
print("\n\n\n\tSymbol Table\n")
for key in Var_Ptr.keys():
    print(key+"\t"+Var_Ptr[key])