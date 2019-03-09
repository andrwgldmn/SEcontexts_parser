#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import subprocess
value = None

def parse_fcf():
        types = (
            ('_data_file', 'data_file_type, file_type'),
            ('_file', 'file_type'),
            ('_socket', 'socket_type'),
            ("_sysfs", "fs_type, sysfs_type"),
            ("sysfs_", "fs_type, sysfs_type"),
            ("_dir", "file_type"),
            ("_debugfs", "fs_type, debugfs_type"),
            ("debugfs_", "fs_type, debugfs_type"), 
            ("_daemon", "fs_type, sysfs_type")
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

        lines = []
        with open('file.te') as fh:
            lines = fh.readlines()

        with open('file.te', 'w') as fh:
            fh.writelines(i for i in lines if '_exec' not in i)



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

def parse_fce():
        with open('file_contexts') as source, open('output.txt', 'w') as destination:
            for line in source:
                if line.strip().endswith('_exec:s0'):
                    destination.write(line)
        with open('output.txt') as input_file, open('exec.te', 'w') as output_file:
            for line in input_file:
                if len(line) > 2 and line[0] != '#':
                    try:
                        prop = line.split(':')[-2] 
                    except IndexError:
                        continue
                    newline = 'type {}, exec_type;\n'.format(prop)
                    output_file.write(newline)
                    subprocess.call(["rm", "-rf", "output.txt"])

def parse_fce_domains():
        with open('file_contexts') as source, open('output.txt', 'w') as destination:
            for line in source:
                if line.strip().endswith('_exec:s0'):
                    destination.write(line)
        with open('output.txt') as input_file, open('exec.te', 'w') as output_file:
            for line in input_file:
                if len(line) > 2 and line[0] != '#':
                    try:
                        prop = line.split(':')[-2] 
                    except IndexError:
                        continue
                    newline = 'type {}, exec_type;\n'.format(prop)
                    output_file.write(newline)
                    subprocess.call(["rm", "-rf", "output.txt"])
        with open('exec.te') as input_file, open('domains.te', 'w') as output_file:
            for line in input_file:
                if len(line) > 2 and line[0] != '#':
                    try:
                        prop = line.split(' ')[-2]
                    except IndexError:
                        continue
                    remove_exec = prop.replace('_exec,','')
                    domain = 'type {}, domain;\n'.format(remove_exec)
                    domain_type = 'type {}_exec, exec_type, file_type;\n'.format(remove_exec)
                    init_daemon = 'init_daemon_domain({})\n\n'.format(remove_exec)
                    output_file.write(domain)
                    output_file.write(domain_type)
                    output_file.write(init_daemon)
                    subprocess.call(["rm", "-rf", "exec.te"])

while value != 0:
    print (' ----------------------------')
    value = int(input(" Choose category: \n \n 0) Exit \n 1) Parsing property_contexts \n 2) Parsing service_contexts \n 3) Parsing file_contexts \n 4) Parsing file_contexts with creating domains \n  ---------------------------- \n "))
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
    elif (value == 3):
        parse_fcf()
        parse_fcd()
        parse_fce()

    elif (value == 2):
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
    elif (value == 4):
        parse_fcf()
        parse_fcd()
        parse_fce_domains()       

