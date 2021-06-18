filename = "Program Examples/prog1"

operators = ['/', '*', '+', '-', '=']
if_operators = ['<', '>', '==']
delimiters = [':', ',']
keywords = ['PROGRAM', 'END', 'INT', 'CHAR', 'BEGIN', 'READ',
            'WRITE', 'FOR', 'TO', 'DO', 'IF', 'ENDFOR', 'ENDIF']

ref_codes = {'PROGRAM': "1", 'INT': "2", 'CHAR': "3", 'BEGIN': "4", 'READ': "5", 'WRITE': "6", 'FOR': "7", 'TO': "8",
             'DO': "9", 'END': "10", 'IF': "11", ':': "12", ',': "13",
             '=': "14", '+': "15", '-': "16", '*': "17", '/': "18", 'id': "19", 'integer': "20", 'string': "21",
             'ENDFOR': "22", 'ENDIF': "23"}

ref_table = {'token': ['PROGRAM', 'INT', 'CHAR', 'BEGIN', 'READ', 'WRITE', 'FOR', 'TO', 'DO', 'END', 'IF', ':', ',',
                       '=', '+', '-', '*', '/', 'id', 'integer', 'string', 'ENDFOR' 'ENDIF'],
             'code': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                      '12', '13',
                      '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']}


def check_begin(lines, line_cnt):
    for i in range(line_cnt - 1, len(lines) - 3):
        if lines.stript().split()[0] == "BEGIN":
            return True
    return False


def check_int(line):
    if line[1].isdigit() or not line[3].isdigit():
        return False
    for i in range(1, len(line)):
        if line[i] == "=":
            if isInteger(line[i + 1]):
                return True
            return False
        return True


def check_read(line):
    if not check_comma(line):
        return False
    for i in range(len(line)):
        if line[i] == "READ" or line[i] == ",":
            continue
        if not check_declaration(line[i], filename):
            return False
    return True


def check_write(line):
    if check_comma(line):
        for i in range(len(line)):
            if line[i] == "WRITE" or line[i] == ",":
                continue
            if not check_declaration(line[i], filename):
                return False
        return True
    return False


def check_arth_op(line):
    if len(line) > 2:
        var_cnt = 0
        op_count = 0
        for i in range(0, len(line)):
            if line[i] in operators:
                op_count += 1
            else:
                var_cnt += 1
        if (var_cnt - 1) != op_count:
            return False
        return True


def check_comma(line):
    if len(line) > 2:
        var_cnt = 0
        comma_cnt = 0
        for i in range(1, len(line)):
            if line[i] == ",":
                comma_cnt += 1
            else:
                var_cnt += 1
        if (var_cnt / 2) != comma_cnt:
            return False
    if len(line) < 2 or ("," not in line and len(line) > 2):
        return False
    for i in range(1, len(line)):
        if line[i] == ",":
            continue
        if not check_str(line[i]):
            return False
    return True


def check_declaration(variable, filename):
    if not check_str(variable):
        return False
    tmp = open(filename + ".txt", "r")
    s = ""
    for string in list(tmp):
        s += string.strip()
    if variable in s.split() and s.find(variable) < s.find("BEGIN"):
        tmp.close()
        return True
    tmp.close()
    return False


def checK_loopEND(ln_cnt, file):
    tmp = open(filename + ".txt", "r")
    for i in list(tmp):
        if "ENDFOR" in i:
            tmp.close()
            return True
    tmp.close()
    return False


def check_ifEND(ln_cnt, file):
    tmp = open(filename + ".txt", "r")
    for i in list(tmp):
        if "ENDIF" in i:
            tmp.close()
            return True
    tmp.close()
    return False


def check_str(string):
    for item in operators:
        if item in string:
            return False
    for item in keywords:
        if item in string:
            return False
    for item in delimiters:
        if item in string:
            return False
    return True


def isInteger(s):
    if s[0] == "-":
        return s[1:].isdigit()
    return s.isdigit()


result = {'token_type': [], 'token_specifier': [],
          'line_no': [], 'var_values': []}
op_lines = {}
IF_lines = {}
FOR_lines = {}
f = open(filename + ".txt", "r")
ln1 = f.readline().strip().split()
if not (ln1[0] == "PROGRAM") or len(ln1) != 2:
    print("ERROR the start of the program isn't identified or ERROR in the program name")
    exit(0)
result['token_type'].append("keyword")
result['token_specifier'].append(ref_table['token'][0])
result['line_no'].append(1)
result['token_type'].append(ref_table['token'][18])
result['token_specifier'].append(ln1[1])
result['line_no'].append(1)
lines = f.readlines()
if not (lines[len(lines) - 1] == "END"):
    print("ERROR the program end isn't specified")
    exit(0)

tmp_mrk = 0
END_mrk = 0
END_IF_mrk = 0
IF_ln_cnt = 0
FOR_ln_cnt = 0
ln_cnt = 2
for i in lines:
    if i == "\n" or i.strip().split()[0] == "PROGRAM":
        ln_cnt += 1
        continue
    else:
        tmp_ln = i.strip().split()
        if tmp_ln[0] == "BEGIN" and len(tmp_ln) == 1:
            tmp_mrk = 1
            if ln_cnt == 1 and lines[ln_cnt].strip().split()[0] == "READ":
                print("Syntax Error some vairables aren't intialized or declared")
                exit(0)
            result['token_type'].append('keyword')
            result['token_specifier'].append(ref_table['token'][3])
            result['line_no'].append(ln_cnt)
            ln_cnt += 1
            continue

        if tmp_ln[0] == "INT" or tmp_ln[0] == "CHAR":
            if len(tmp_ln) != 4 or ("=" not in tmp_ln):
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if tmp_ln[0] == "INT":
                if not check_int(tmp_ln):
                    print("Syntax Error in line ", ln_cnt)
                    exit(0)
                result['token_type'].append("keyword")  # int
                result['token_specifier'].append(ref_table['token'][1])
                result['line_no'].append(ln_cnt)
                result['token_type'].append(ref_table['token'][18])  # ID
                result['token_specifier'].append(tmp_ln[1])
                result['line_no'].append(ln_cnt)
                result['token_type'].append("operator")  # = operator
                result['token_specifier'].append(ref_table['token'][13])
                result['line_no'].append(ln_cnt)
                result['token_type'].append(ref_table['token'][19])  # INTEGER
                result['var_values'].append(tmp_ln[3])
                result['token_specifier'].append(tmp_ln[3])
                result['line_no'].append(ln_cnt)
                ln_cnt += 1
                continue
            if tmp_ln[0] == "CHAR":
                if "'" in tmp_ln[3]:
                    tmp_ln[3] = tmp_ln[3].replace("'", "")
                elif '"' in tmp_ln[3]:
                    tmp_ln[3] = tmp_ln[3].replace('"', "")
                result['token_type'].append("keyword")  # char
                result['token_specifier'].append(ref_table['token'][2])
                result['line_no'].append(ln_cnt)
                result['token_type'].append(ref_table['token'][18])  # ID
                result['token_specifier'].append(tmp_ln[1])
                result['line_no'].append(ln_cnt)
                result['token_type'].append("operator")  # = operator
                result['token_specifier'].append(ref_table['token'][13])
                result['line_no'].append(ln_cnt)
                result['token_type'].append(ref_table['token'][20])  # STRING
                result['token_specifier'].append(tmp_ln[3])
                result['line_no'].append(ln_cnt)
                ln_cnt += 1
                continue

        if tmp_ln[0] not in operators and tmp_ln[0] not in delimiters and tmp_ln[0] not in keywords:
            for j in range(0, len(tmp_ln)):  # arthimetic op
                if check_declaration(tmp_ln[j], filename) and check_arth_op(tmp_ln):
                    result['token_type'].append("id")
                    result['token_specifier'].append(tmp_ln[j])
                    result['line_no'].append(ln_cnt)
                elif tmp_ln[j] in operators and check_arth_op(tmp_ln):
                    result['token_type'].append("operator")
                    result['token_specifier'].append(tmp_ln[j])
                    result['line_no'].append(ln_cnt)
                else:
                    print("Syntax Error in line: ", ln_cnt)
                    exit(0)
            if END_mrk == 1:
                if op_lines.get(FOR_ln_cnt):
                    print("Syntax Error in line: ", ln_cnt)
                    exit(0)
                op_lines[FOR_ln_cnt] = tmp_ln
            elif END_IF_mrk == 1:
                if op_lines.get(IF_ln_cnt):
                    print("Syntax Error in line: ", ln_cnt)
                    exit(0)
                op_lines[IF_ln_cnt] = tmp_ln
            else:
                op_lines[ln_cnt] = tmp_ln
            ln_cnt += 1
            continue

        # END
        if tmp_ln[0] in keywords and tmp_ln[0] == "END" and len(tmp_ln) == 1:
            result['token_type'].append("keyword")
            result['token_specifier'].append('END')
            result['line_no'].append(ln_cnt)
            ln_cnt += 1
            continue
        elif tmp_ln[0] == "ENDIF" and END_IF_mrk == 1:
            END_IF_mrk = 0
            IF_ln_cnt = 0
            result['token_type'].append("keyword")
            result['token_specifier'].append('ENDIF')
            result['line_no'].append(ln_cnt)
            ln_cnt += 1
            continue
        elif tmp_ln[0] in keywords and tmp_ln[0] == "IF" and END_mrk == 0:  ##IF
            if len(tmp_ln) != 5:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if not check_ifEND(ln_cnt, filename):
                print("Missing ENDIF in loop in line: ", ln_cnt)
                exit(0)
            else:
                END_IF_mrk = 1
            result['token_type'].append("keyword")
            result['token_specifier'].append('IF')
            result['line_no'].append(ln_cnt)
            if isInteger(tmp_ln[1]):
                result['token_type'].append(ref_table['token'][19])  # INTEGER
                result['token_specifier'].append(tmp_ln[1])
                result['line_no'].append(ln_cnt)
            elif check_declaration(tmp_ln[1], filename):
                result['token_type'].append('id')  ##id
                result['token_specifier'].append(tmp_ln[1])
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if tmp_ln[2] not in if_operators:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            else:
                result['token_type'].append('operator')  ##operator
                result['token_specifier'].append(tmp_ln[2])
                result['line_no'].append(ln_cnt)
            if isInteger(tmp_ln[3]):
                result['token_type'].append(ref_table['token'][19])  # INTEGER
                result['token_specifier'].append(tmp_ln[3])
                result['line_no'].append(ln_cnt)
            elif check_declaration(tmp_ln[3], filename):
                result['token_type'].append('id')  ##id
                result['token_specifier'].append(tmp_ln[3])
                result['line_no'].append(ln_cnt)
            if tmp_ln[4] == "DO" and END_IF_mrk == 1:
                result['token_type'].append('keyword')  ##id
                result['token_specifier'].append(tmp_ln[4])
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            IF_lines[ln_cnt] = tmp_ln[1:4]
            IF_ln_cnt = ln_cnt
            ln_cnt += 1
            continue
        elif tmp_ln[0] in keywords and tmp_ln[0] == "FOR" and END_IF_mrk == 0:
            if len(tmp_ln) < 7:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if not checK_loopEND(ln_cnt, filename):
                print("Missing ENDFOR in loop in line: ", ln_cnt)
                exit(0)
            else:
                END_mrk = 1
            result['token_type'].append("keyword")
            result['token_specifier'].append('FOR')
            result['line_no'].append(ln_cnt)
            if tmp_ln[1] not in keywords and tmp_ln[1] not in delimiters and tmp_ln[1] not in operators and not tmp_ln[
                                                                                                                    1] in \
                                                                                                                result[
                                                                                                                    'token_specifier']:  # counter variable
                result['token_type'].append("id")
                result['token_specifier'].append(tmp_ln[1])
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if tmp_ln[2] in operators:  # =
                result['token_type'].append("operator")
                result['token_specifier'].append(tmp_ln[2])
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if check_declaration(tmp_ln[3], filename) and tmp_ln[3] not in operators:
                result['token_type'].append("id")
                result['token_specifier'].append(tmp_ln[3])
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if tmp_ln[4] in keywords and tmp_ln[4] == "TO":
                result['token_type'].append("keyword")
                result['token_specifier'].append('TO')
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if check_declaration(tmp_ln[5], filename) and tmp_ln[5] not in operators:
                result['token_type'].append("id")
                result['token_specifier'].append(tmp_ln[5])
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            if tmp_ln[6] in keywords and tmp_ln[6] == "DO":
                result['token_type'].append("keyword")
                result['token_specifier'].append('DO')
                result['line_no'].append(ln_cnt)
            else:
                print("Syntax Error in line: ", ln_cnt)
                exit(0)
            FOR_lines[ln_cnt] = tmp_ln[1:6]
            FOR_ln_cnt = ln_cnt
            ln_cnt += 1
            continue
        elif tmp_ln[0] in keywords and tmp_ln[0] == "ENDFOR" and END_mrk == 1:
            result['token_type'].append("keyword")
            result['token_specifier'].append('ENDFOR')
            result['line_no'].append(ln_cnt)
            END_mrk = 0
            IF_ln_cnt = 0
            ln_cnt += 1
            continue
        else:
            print("Syntax Error in line: ", ln_cnt)
            exit(0)

if tmp_mrk == 0:
    print("Syntax Error missing 'BEGIN'")
    exit(0)

print("TOKEN TYPE\tTOKEN SPECIFIER\t\tLINE COUNT\n")
for i in range(len(result['token_type'])):
    print(str(result["token_type"][i]) + "\t\t" +
          str(result["token_specifier"][i]) + "\t\t\t" + str(result["line_no"][i]))
