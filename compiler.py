import tokenize


def parse(file):
    code = []
    with tokenize.open(file) as f:
        tokens = tokenize.generate_tokens(f.readline)
        comment = False
        for toknum, tokval, _, _, _ in tokens:
            if tokval == '\n':
                comment = False
                continue
            if tokval == '//':
                comment = True
                continue
            if toknum == tokenize.NUMBER and not comment:
                code.append(int(tokval))
                continue
            if not comment:
                code.append(tokval)

    return code


def separation(code):
    main_code = []
    procedure_dict = {}
    procedure_code = []
    procedure_names = []
    procedure_name = None
    procedure_mode = False
    add_name = False
    for item in code:
        if item == ':':
            procedure_code = []
            procedure_mode = True
            add_name = True
        elif item == ';':
            procedure_dict.update({procedure_name: procedure_code})
            procedure_mode = False
        elif procedure_mode:
            if add_name:
                procedure_name = item
                procedure_names.append(item)
                add_name = False
            else:
                procedure_code.append(item)
        else:
            main_code.append(item)

    new_main_code = []
    for item in main_code:
        if procedure_names.count(item) != 0:
            new_main_code.append('@address@')
        new_main_code.append(item)
    new_main_code.append('exit')
    main_code = new_main_code
    for name in procedure_dict:
        procedure_code = []
        for item in procedure_dict[name]:
            if procedure_names.count(item) != 0:
                procedure_code.append('@address@')
            procedure_code.append(item)
        procedure_code.append('return')
        procedure_dict.update({name: procedure_code})

    return main_code, procedure_dict


def compiler(file):
    main_code, procedure_dict = separation(parse(file))
    address = len(main_code)
    for name in procedure_dict:
        for i in range(len(main_code)):
            if name == main_code[i]:
                main_code[i] = 'call'
                main_code[i - 1] = address
        for key in procedure_dict:
            for j in range(len(procedure_dict[key])):
                if procedure_dict[key][j] == name:
                    procedure_dict[key][j] = 'call'
                    procedure_dict[key][j - 1] = address
        address += len(procedure_dict[name])
    for name in procedure_dict:
        main_code.extend(procedure_dict[name])
    return main_code
