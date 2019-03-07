#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
value = None

def parse_fc_one(prop, types, output_file):
    type_data, other_types = types

    is_data_file = type_data[0] in prop

    if is_data_file:
        newline = 'type {}, {}, file_type;\n'.format(prop, type_data[1])
        #print(newline)
        output_file.write(newline)
    else:
        for t in types:
            if t[0] in prop:
                newline = 'type {}, {};\n'.format(prop, t[1])
                #print(newline)
                output_file.write(newline)


def parse_fc():
    type_data = ("_data_file", "data_file_type")
    other_types = (("_file", "file_type"),
            ("_device", "dev_type"),
            ("_socket", "file_type"),
            ("_sysfs", "fs_type, sysfs_type"),
            ("sysfs_", "fs_type, sysfs_type"),
            ("sysfs_", "fs_type, sysfs_type"),
            ("_block_device", "dev_type"),
            ("_dir", "file_type"),
            ("_debugfs", "fs_type, debugfs_type"),
            ("debugfs_", "fs_type, debugfs_type"),
            ("_daemon", "fs_type, sysfs_type"),
            ("_exec" , "exec_type, file_type")
    )

    all_types = [type_data, other_types]

    is_data_file = False

    with open('file_contexts') as input_file:
        with open('file.te', 'w') as output_file:
            for line in input_file:
                if len(line) > 2 and line[0] != '#':
                    try:
                        prop = line.split(':')[-2]
                    except IndexError:
                        continue

                    parse_fc_one(prop, all_types, output_file)

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
        parse_fc()

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
