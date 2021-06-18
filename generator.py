from Lexical_analyzer import filename as in_file, result, operators, keywords, delimiters, ref_codes, ref_table, \
    op_lines, IF_lines, FOR_lines

filename = in_file + '.asm'

op_vars = {}

if_stat = False
loop_stat = False
new_line = True
repeat = False

reg_a = False  # true means in use
sub_op = ""
div_op = ""
operand1 = ""
line_count = 1
FOR_bound1 = ""
FOR_bound2 = ""
FOR_line = 0


def isInteger(s):
    if s[0] == "-":
        return s[1:].isdigit()
    return s.isdigit()


def op_sort(arr):
    global operators
    return sorted(arr, key=operators.index)


def get_progname():
    name = result['token_specifier'][1]
    f = open(filename, 'w')
    f.write('START ' + name + ' 0')
    f.close()


def get_vars():
    for i in range(2, get_begin()):
        if result['token_type'][i] == "id":
            op_vars[result['token_specifier'][i]
                    ] = result['token_specifier'][i + 2]


def get_begin():
    for i in range(len(result['token_specifier'])):
        if result['token_specifier'][i] == "BEGIN":
            return i + 1


def declare_vars():
    f = open(filename, 'a')
    for key, value in op_vars.items():
        if is_used(key):
            if isInteger(value):
                f.write("\n{} WORD {}".format(key, value))
            else:
                f.write("\n{} BYTE {}".format(key, value))
    f.close()


def is_used(var):
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        if var in line.strip().split():
            return True
    return False


def mul(line, op_ind):
    f = open(filename, 'a')
    global line_count
    if new_line:
        f.write(f"\nL{line_count}\t")
    else:
        f.write("\n\t")
    global reg_a
    global sub_op
    global div_op
    global operand1
    op1 = line[op_ind - 1]
    if op_ind + 1 < len(line):
        op2 = line[op_ind + 1]
    else:
        op2 = False
    if reg_a == False:
        f.write(f"LDA {op1}\n\tMUL {op2}")
        reg_a = True
        if len(line) - 3 >= 2:
            if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                if line[op_ind - 2] == "-":
                    sub_op = op1
                else:
                    div_op = op1
        del line[op_ind: op_ind + 2]
        line[op_ind - 1] = op1
        operand1 = op1
        return line
    else:
        if op1 in operators:
            f.write(f"MUL {op2}")
            if len(line) - 3 >= 2:
                if line[op_ind - 1] == "-" or line[op_ind - 1] == "/":
                    if line[op_ind - 2] == "-":
                        sub_op = op1
                    else:
                        div_op = op1
            del line[op_ind:op_ind + 2]
            operand1 = op1
            return line
        elif op2 in operators:
            f.write(f"MUL {op1}")
            if len(line) - 3 >= 2:
                if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                    if line[op_ind - 2] == "-":
                        sub_op = op1
                    else:
                        div_op = op1
            del line[op_ind - 1: op_ind + 1]
            operand1 = op1
            return line
        else:
            if line[op_ind - 2] not in operators:
                f.write(f"MUL {op1}")
                if len(line) - 3 >= 2:
                    if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                        if line[op_ind - 2] == "-":
                            sub_op = op1
                        else:
                            div_op = op1
                del line[op_ind - 1:op_ind + 1]
                operand1 = op1
                return line
            else:
                if operand1 != "":
                    f.write(f"STA {operand1}\n\tLDA {op1}\n\tMUL {op2}")
                    del line[op_ind: op_ind + 2]
                    line[op_ind - 1] = op1
                    operand1 = op1
                    return line
                else:
                    f.write(f"LDA {op1}\n\tMUL {op2}")
                    del line[op_ind: op_ind + 2]
                    line[op_ind - 1] = op1
                    operand1 = op1
                    return line
    f.close()


def add(line, op_ind):
    f = open(filename, 'a')
    global reg_a
    global sub_op
    global div_op
    global operand1
    global line_count
    if new_line:
        f.write(f"\nL{line_count}\t")
    else:
        f.write("\n\t")
    op1 = line[op_ind - 1]
    if op_ind + 1 < len(line):
        op2 = line[op_ind + 1]
    else:
        op2 = False
    if not reg_a:
        f.write(f"LDA {op1}\n\tADD {op2}")
        reg_a = True
        if len(line) - 3 >= 2:
            if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                if line[op_ind - 2] == "-":
                    sub_op = op1
                else:
                    div_op = op1
        del line[op_ind: op_ind + 2]
        line[op_ind - 1] = op1
        operand1 = op1
        return line
    else:
        if op1 in operators:
            f.write(f"ADD {op2}")
            if len(line) - 3 >= 2:
                if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                    if line[op_ind - 2] == "-":
                        sub_op = op1
                    else:
                        div_op = op1
            del line[op_ind:op_ind + 2]
            operand1 = op1
            return line
        elif op2 in operators:
            f.write(f"ADD {op1}")
            if len(line) - 3 >= 2:
                if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                    if line[op_ind - 2] == "-":
                        sub_op = op1
                    else:
                        div_op = op1
            del line[op_ind - 1: op_ind + 1]
            operand1 = op1
            return line
        else:
            if line[op_ind - 2] not in operators:
                f.write(f"ADD {op1}")
                if len(line) - 3 >= 2:
                    if line[op_ind - 2] == "-" or line[op_ind - 2] == "/":
                        if line[op_ind - 2] == "-":
                            sub_op = op1
                        else:
                            div_op = op1
                del line[op_ind - 1:op_ind + 1]
                operand1 = op1
                return line
            else:
                if operand1 != "":
                    f.write(f"STA {operand1}\n\tLDA {op1}\n\tADD {op2}")
                    del line[op_ind: op_ind + 2]
                    line[op_ind - 1] = op1
                    operand1 = op1
                    return line
                else:
                    f.write(f"LDA {op1}\n\tADD {op2}")
                    del line[op_ind: op_ind + 2]
                    line[op_ind - 1] = op1
                    operand1 = op1
                    return line
    f.close()


def sub(line, op_ind):
    f = open(filename, 'a')
    global reg_a
    global operand1
    global line_count
    if new_line:
        f.write(f"\nL{line_count}\t")
    else:
        f.write("\n\t")
    op1 = line[op_ind - 1]
    if op_ind + 1 < len(line):
        op2 = line[op_ind + 1]
    else:
        op2 = False
    if not reg_a and op2 != False and op2 not in operators and len(line) > 4 and op1 not in operators:
        if operand1 != "":
            f.write(f"STA {operand1}\n\tLDA {op1}\n\tSUB {op2}")
        else:
            f.write(f"LDA {op1}\n\tSUB {op2}")
        reg_a = True
        del line[(op_ind): (op_ind + 2)]
        line[op_ind - 1] = op1
        if len(line) == 3 and line[2] == "-":
            f.write(f"SUB {sub_op}")
            del line[2]
        operand1 = op1
        return line
    elif not reg_a and op2 == False:
        f.write(f"STA {sub_op}\n\tLDA {op1}\n\tSUB {sub_op}")
        del line[(op_ind - 1): (op_ind + 1)]
        operand1 = op1
        return line
    else:
        if op1 in operators:
            f.write(f"SUB {op2}")
            del line[op_ind:op_ind + 2]
            operand1 = op1
            return line
        elif op2 in operators and sub_op != "":
            f.write(f"STA {sub_op[0]}\n\tLDA {op1}\n\tSUB {sub_op[0]}")
            del line[op_ind - 1: op_ind + 1]
            operand1 = op1
            return line
        else:
            if sub_op != "":
                f.write(f"LDA {op1}\n\tSUB {sub_op[0]}")
                del line[op_ind - 1: op_ind + 1]
                operand1 = op1
                return line
            else:
                f.write(f"SUB {op1}")
                del line[op_ind - 1:op_ind + 1]
                operand1 = op1
                return line
    f.close()


def div(line, op_ind):
    f = open(filename, 'a')
    global reg_a
    global operand1
    global line_count
    if new_line:
        f.write(f"\nL{line_count}\t")
    else:
        f.write("\n\t")
    op1 = line[op_ind - 1]
    if op_ind + 1 < len(line):
        op2 = line[op_ind + 1]
    else:
        op2 = False
    if not reg_a and op2 != False and op2 not in operators and len(line) > 4 and op1 not in operators:
        if operand1 != "":
            f.write(f"STA {operand1}\n\tLDA {op1}\n\tDIV {op2}")
        else:
            f.write(f"LDA {op1}\n\tDIV {op2}")
        reg_a = True
        del line[op_ind: (op_ind + 2)]
        line[op_ind - 1] = op1
        if len(line) == 3 and line[2] == "-":
            f.write(f"DIV {div_op}")
            del line[2]
        operand1 = op1
        return line
    elif not reg_a and op2 == False:
        f.write(f"DIV {div_op}\n\tLDA {op1}\n\tDIV {div_op}")
        del line[(op_ind - 1): (op_ind + 1)]
        operand1 = op1
        return line
    else:
        if op1 in operators:
            f.write(f"DIV {op2}")
            del line[op_ind:op_ind + 2]
            operand1 = op1
            return line
        elif op2 in operators and div_op != "":
            f.write(f"STA {div_op}\n\tLDA {op1}\n\tDIV {div_op}")
            del line[op_ind - 1: op_ind + 1]
            operand1 = op1
            return line
        else:
            if sub_op != "":
                f.write(f"LDA {op1}\n\tDIV {div_op}")
                del line[op_ind - 1: op_ind + 1]
                operand1 = op1
                return line
            else:
                f.write(f"DIV {op1}")
                del line[op_ind - 1:op_ind + 1]
                operand1 = op1
                return line
    f.close()


def equate(line, op_ind, ld=False):
    global new_line
    f = open(filename, 'a')
    if new_line:
        f.write(f"\nL{line_count}\t")
    else:
        f.write("\n\t")
    if len(line) == 3 and line[1] == "=" and line[2] not in operators:
        if not ld:
            f.write(f"STA {line[0]}")
            f.close()
            return line
        else:
            f.write(f"LDA {line[2]}\n\tSTA {line[0]}")
            f.close()
            return line
    f.close()


def core():
    global reg_a
    global sub_op
    global div_op
    global new_line
    global line_count
    global operand1
    global FOR_bound1
    global FOR_bound2
    global FOR_line
    global repeat
    op = []
    tmp_repeated_lines = []
    r_count = 0
    r_lines = {}
    r_lines_rand_vars = {}
    break1 = 0
    for key, value in op_lines.items():
        if key not in tmp_repeated_lines:
            r_lines[key] = []
        for key1, value1 in op_lines.items():
            if not (key == key1) and value[2:] == value1[
                    2:] and key not in IF_lines.keys() and key not in FOR_lines.keys() and key not in tmp_repeated_lines:
                op_vars["tmp" + str(r_count)] = str(0)
                tmp_repeated_lines.append(key1)
                r_lines[key].append(key1)
                r_lines_rand_vars[key] = str("tmp" + str(r_count))
                r_count += 1

    for key, value in op_lines.items():
        if key not in IF_lines.keys() and key not in FOR_lines.keys():
            break1 = 0
            op.clear()
            new_line = True
            operand1 = ""
            line = op_lines[key]

            for i in range(len(line)):
                if line[i] in operators:
                    op.append(line[i])
            op = op_sort(op)
            if key in tmp_repeated_lines:
                for ky_tmp, value_tmp in r_lines.items():
                    for item in value_tmp:
                        if key == item:
                            line = line[:3]
                            line[2] = r_lines_rand_vars[ky_tmp]
                            line = equate(line, 1, True)
                            line_count += 1
                            break1 = 1
                            break
                    if break1 == 1:
                        break
            if break1 == 0:
                for i in range(len(op)):
                    for j in range(len(line)):
                        if op[i] == line[j] and not repeat:
                            if op[i] == "*":
                                line = mul(line, j)
                                new_line = False
                                break
                            elif op[i] == "+":
                                line = add(line, j)
                                new_line = False
                                break
                            elif op[i] == "-":
                                reg_a = False
                                line = sub(line, j)
                                new_line = False
                                break
                            elif op[i] == "/":
                                reg_a = False
                                line = div(line, j)
                                new_line = False
                                break
                            elif op[i] == "=":
                                line = equate(line, j)
                                new_line = False
                                break
                if key in r_lines_rand_vars.keys():
                    f = open(filename, 'a')
                    f.write(f"\n\tSTA {r_lines_rand_vars[key]}")
                    f.close()
                line_count += 1
        elif key in IF_lines.keys() and key not in FOR_lines.keys():
            if key in IF_lines.keys():
                f = open(filename, 'a')
                if_op1 = IF_lines[key][0]
                if_op2 = IF_lines[key][2]
                if_op = IF_lines[key][1]
                if if_op == "<":
                    f.write(
                        f"\nL{line_count}\tLDA {if_op1}\n\tCOMP {if_op2}\n\tJLT L{line_count + 1}")
                elif if_op == ">":
                    f.write(
                        f"\nL{line_count}\tLDA {if_op1}\n\tCOMP {if_op2}\n\tJGT L{line_count + 1}")
                elif if_op == "==":
                    f.write(
                        f"\nL{line_count}\tLDA {if_op1}\n\tCOMP {if_op2}\n\tJEQ L{line_count + 1}")
                if list(op_lines).index(key) < len(list(op_lines)) - 1:
                    f.write(f"\n\tJ L{line_count + 2}")
                else:
                    f.write(f"\n\t J EXIT")
                f.close()
                line_count += 1
                op.clear()
                new_line = True
                operand1 = ""
                line = op_lines[key]
                for i in range(len(line)):
                    if line[i] in operators:
                        op.append(line[i])
                op = op_sort(op)
                if key in tmp_repeated_lines:
                    for ky_tmp, value_tmp in r_lines.items():
                        for item in value_tmp:
                            if key == item and key > ky_tmp:
                                line = line[:3]
                                line[2] = r_lines_rand_vars[ky_tmp]
                                line = equate(line, 1, True)
                                line_count += 1
                                break1 = 1
                                break
                        if break1 == 1:
                            break
                if break1 == 0:
                    for i in range(len(op)):
                        for j in range(len(line)):
                            if op[i] == line[j] and not repeat:
                                if op[i] == "*":
                                    line = mul(line, j)
                                    new_line = False
                                    break
                                elif op[i] == "+":
                                    line = add(line, j)
                                    new_line = False
                                    break
                                elif op[i] == "-":
                                    reg_a = False
                                    line = sub(line, j)
                                    new_line = False
                                    break
                                elif op[i] == "/":
                                    reg_a = False
                                    line = div(line, j)
                                    new_line = False
                                    break
                                elif op[i] == "=":
                                    line = equate(line, j)
                                    new_line = False
                                    break
                    if key in r_lines_rand_vars.keys():
                        f = open(filename, 'a')
                        f.write(f"\n\tSTA {r_lines_rand_vars[key]}")
                        f.close()
                    line_count += 1
        else:
            f = open(filename, "a")
            FOR_bound1 = FOR_lines[key][2]
            FOR_bound2 = FOR_lines[key][4]
            f.write(f"\nL{line_count}\tLDX {FOR_bound1}")
            line_count += 1
            f.write(f"\nL{line_count}\tLDA {FOR_bound1}\n\tCOMP {FOR_bound2}")
            if list(op_lines).index(key) < len(list(op_lines)) - 1:
                f.write(f"\n\tJGT L{line_count + 2}")
            else:
                f.write(f"\n\t JGT EXIT")
            f.close()
            line_count += 1
            op.clear()
            new_line = True
            operand1 = ""
            line = op_lines[key]
            for i in range(len(line)):
                if line[i] in operators:
                    op.append(line[i])
            op = op_sort(op)
            if key in tmp_repeated_lines:
                for ky_tmp, value_tmp in r_lines.items():
                    for item in value_tmp:
                        if key == item:
                            line = line[:3]
                            line[2] = r_lines_rand_vars[ky_tmp]
                            line = equate(line, 1, True)
                            line_count += 1
                            break1 = 1
                            break
                    if break1 == 1:
                        break
            if break1 == 0:
                for i in range(len(op)):
                    for j in range(len(line)):
                        if op[i] == line[j] and not repeat:
                            if op[i] == "*":
                                line = mul(line, j)
                                new_line = False
                                break
                            elif op[i] == "+":
                                line = add(line, j)
                                new_line = False
                                break
                            elif op[i] == "-":
                                reg_a = False
                                line = sub(line, j)
                                new_line = False
                                break
                            elif op[i] == "/":
                                reg_a = False
                                line = div(line, j)
                                new_line = False
                                break
                            elif op[i] == "=":
                                line = equate(line, j)
                                new_line = False
                                break
                if key in r_lines_rand_vars.keys():
                    f = open(filename, 'a')
                    f.write(f"\n\tSTA {r_lines_rand_vars[key]}")
                    f.close()
                f = open(filename, "a")
                f.write(f"\n\tTIX\n\tSTX {FOR_bound1}\n\tJ L{line_count - 1}")
                f.close()
                line_count += 1


get_vars()
get_progname()
core()
declare_vars()
