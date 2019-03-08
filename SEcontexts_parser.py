#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
value = None

def parse_fcf():
        types = (
            ('_data_file', 'data_file_type, file_type'),
            ('_file', 'file_type'),
            ('_socket', 'socket_type'),
            ("_sysfs", "fs_type, sysfs_type"),
            ("sysfs_", "fs_type, sysfs_type"),
            ("sysfs_", "fs_type, sysfs_type"),
            ("_dir", "file_type"),
            ("_debugfs", "fs_type, debugfs_type"),
            ("debugfs_", "fs_type, debugfs_type"), 
            ("_daemon", "fs_type, sysfs_type"),
            ("_exec" , "exec_type, file_type")
)

        with open('file_contexts') as input_file: 
            with open('file.te', 'w') as output_file:
                for line in input_file:
                    if len(line) > 2 and line[0] != '#':
                        try:
                            # Разбиваем строку на части по символу ':'
                            # Из полученного списка берем предпоследний элемент
                            prop = line.split(':')[-2] 
                        except IndexError:
                            continue

                        # Сначала проверяем тип data_file, потом file,
                        # потом все остальное. Если тип соответствует,
                        # то пишем в файл и прекращаем проверку строки.
                        for t in types:
                            if t[0] in prop:
                                newline = 'type {}, {};\n'.format(prop, t[1])
                                output_file.write(newline)
                                break
def parse_fcd():
        types = (('_device', 'dev_type'), ("_block_device", "dev_type"))

        with open('file_contexts') as input_file: 
            with open('device.te', 'w') as output_file:
                for line in input_file:
                    if len(line) > 2 and line[0] != '#':
                        try:
                            prop = line.split(':')[-2] 
                        except IndexError:
                            continue
                        for t in types:
                            if t[0] in prop:
                                newline = 'type {}, {};\n'.format(prop, t[1])
                                output_file.write(newline)
                                break

while value != 0:
    print (' ----------------------------')
    value = int(input(" Choose category: \n \n 0) Exit \n 1) Parsing property_contexts \n 2) Parsing file_contexts \n 3) Parsing service_contexts \n ---------------------------- \n "))
    if (value == 0):
        print('-' * 28 + '\n Thanks!\n' + '-' * 28)
    elif (value == 1):
        with open('property_contexts') as input_file: 
            with open('property.te', 'w') as output_file:
                for line in input_file:
                    if len(line) > 2 and line[0] != '#':
                        try:
                            prop = line.split(':')[-2] 
                        except IndexError:
                            continue
                        newline = 'type {}, property_type;\n'.format(prop)
                        output_file.write(newline)
    elif (value == 2):
        parse_fcf()
        parse_fcd()
    elif (value == 3):
        with open('service_contexts') as input_file: 
            with open('service.te', 'w') as output_file:
                for line in input_file:
                    if len(line) > 2 and line[0] != '#':
                        try:
                            prop = line.split(':')[-2] 
                        except IndexError:
                            continue
                        newline = 'type {}, service_manager_type;\n'.format(prop)
                        output_file.write(newline)

