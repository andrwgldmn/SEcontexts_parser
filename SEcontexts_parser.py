#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import subprocess
import requests

value = None

def sepologparser_inet():
        with open('allows.te', 'w') as output_file:
            url = raw_input(' Enter the URL: ')
            r = requests.get(url)
            data = r.text

            pat = r"""avc:\s*denied\s*({\s*[^}]*\s*})\s+.*?scontext=u:r:([^:]*):s\d+.*?tcontext=.*?:(\w{2,}):s0.*?\s+tclass=([^\s:]*)\s+"""

            for what, scnt, tcnt, tc in re.findall(pat, data):
                output_file.write("allow {} {}:{} {} \n".format(scnt, tcnt, tc, what))
        os.system('cls' if os.name == 'nt' else 'clear') 

def sepologparser_local():
        with open('log.txt') as input_file, open('allows.te', 'w') as output_file:
            text = input_file.read()
            pat = r"""avc:\s*denied\s*({\s*[^}]*\s*})\s+.*?scontext=u:r:([^:]*):s\d+.*?tcontext=.*?:(\w{2,}):s0.*?\s+tclass=([^\s:]*)\s+"""
            for what, scnt, tcnt, tc in re.findall(pat, text):
                output_file.write("allow {} {}:{} {} \n".format(scnt, tcnt, tc, what))
        os.system('cls' if os.name == 'nt' else 'clear')    

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

        File = open('file.te', 'r')
        str_list = set()
        for i in File.readlines():
            if i not in str_list:
                str_list.add(i)
        File.close()
        File = open('file.te', 'w')
        for j in str_list:
            File.write(j)

        os.system('cls' if os.name == 'nt' else 'clear')

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
        os.system('cls' if os.name == 'nt' else 'clear')

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
        os.system('cls' if os.name == 'nt' else 'clear')

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
        os.system('cls' if os.name == 'nt' else 'clear')

def only_domains():
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
                    cmd = "rm -rf exec.te file.te device.te"
                    os.system(cmd)
        os.system('cls' if os.name == 'nt' else 'clear')

def property_contexts():
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
        os.system('cls' if os.name == 'nt' else 'clear')

def service_contexts():
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
        os.system('cls' if os.name == 'nt' else 'clear')

def stock_fc():
        cmd = "./sefcontext -o file_contexts file_contexts.bin"
        os.system(cmd)
        os.system('cls' if os.name == 'nt' else 'clear')

def stock_sepo():
        cmd = "./sesearch --all sepolicy > sepolicy.txt"
        os.system(cmd)
        os.system('cls' if os.name == 'nt' else 'clear')

def cleanup():
        cmd = "rm -rf file.te sepolicy.txt sepolicy log.txt allows.te file_contexts device.te file exec.te domains.te file service.te file_contexts.bin service_contexts property.te property_contexts"
        os.system(cmd)
        os.system('cls' if os.name == 'nt' else 'clear')

while value != 0:
    print (' ----------------------------')
    value = int(input(" 1) English \n 2) Русский \n 3) Українська \n ---------------------------- \n "))
    if (value != 1 and value != 2 and value != 3 ):
        print ("\n Program has been terminated. \n" )
    if (value == 1):
        while value != 0:
            print (' ----------------------------')
            value = int(input(" Choose category: \n \n 0) Exit \n 00) Cleanup \n 1) Parsing property_contexts \n 2) Parsing service_contexts \n 3) Parsing file_contexts \n 4) Parsing file_contexts with creating domains \n 5) Generating domains only \n 6) Parsing stock file_contexts binary (taken from boot.img) for getting stock policies \n 7) Parsing stock sepolicy binary (taken from boot.img) for getting stock rules \n 8) Parsing local log.txt for getting SEPolicy rules \n 9) Parsing log.txt for getting SEPolicy rules via Internet (log.txt will be given from your entered URL) \n 10) Cleanup \n  ---------------------------- \n "))
            
            if (value == 0):
                print('-' * 28 + '\n Thanks!\n' + '-' * 28)

            elif (value == 1):
                property_contexts()

            elif (value == 3):
                parse_fcf()
                parse_fcd()
                parse_fce()

            elif (value == 2):
                service_contexts()

            elif (value == 4):
                parse_fcf()
                parse_fcd()
                parse_fce_domains()       

            elif (value ==5):
                only_domains()

            elif (value == 6):
                stock_fc()

            elif (value == 7):
                stock_sepo()

            elif (value == 8):
                sepologparser_local()

            elif (value == 9):
                sepologparser_inet()

            elif (value == 00):
                cleanup()

    if (value == 2):
        while value != 0:
            print (' ----------------------------')
            value = int(input(" Выберите категорию: \n \n 0) Выход \n 00) Очистка \n 1) Анализ property_contexts \n 2) Анализ service_contexts \n 3) Анализ file_contexts \n 4) Анализ file_contexts из созданием типов \n 5) Создание ТОЛЬКО типов \n 6) Анализ стокового бинарника file_contexts (взятого из boot.img) для получения стоковых политик \n 7) Анализ стокового бинарника sepolicy (взятого из boot.img) для получения стоковых политик \n 8) Анализ локального log.txt для получения правил SEPolicy \n 9) Анализ log.txt для получения правил SEPolicy через Internet (log.txt будет скачан по ссылке, которую Вы введёте. URL) \n   ---------------------------- \n "))
            
            if (value == 0):
                print('-' * 28 + '\n Спасибо!\n' + '-' * 28)

            elif (value == 1):
                property_contexts()

            elif (value == 3):
                parse_fcf()
                parse_fcd()
                parse_fce()

            elif (value == 2):
                service_contexts()

            elif (value == 4):
                parse_fcf()
                parse_fcd()
                parse_fce_domains()       

            elif (value ==5):
                only_domains()

            elif (value == 6):
                stock_fc()

            elif (value == 7):
                stock_sepo()

            elif (value == 8):
                sepologparser_local()

            elif (value == 9):
                sepologparser_inet()

            elif (value == 00):
                cleanup()

    if (value == 3):
        while value != 0:
            print (' ----------------------------')
            value = int(input(" Оберіть категорію: \n \n 0) Вихід \n 00) Очистка \n 1) Аналіз property_contexts \n 2) Аналіз service_contexts \n 3) Аналіз file_contexts \n 4) Аналіз file_contexts зі створенням політик  \n 5) Створення ТІЛЬКИ політик \n 6) Аналіз стокового бінарника file_contexts (взятий з boot.img) для отримання стокових політик \n 7) Аналіз стокового бінарника sepolicy (взятий з boot.img) для отримання стокових політик \n 8) Аналіз локального log.txt для отримання правил SEPolicy \n 9) Аналіз log.txt для отримання правил SEPolicy через Internet (log.txt буде завантажений з URL, яку Ви введете) \n  ---------------------------- \n "))
            
            if (value == 0):
                print('-' * 28 + '\n Дякую!\n' + '-' * 28)

            elif (value == 1):
                property_contexts()

            elif (value == 3):
                parse_fcf()
                parse_fcd()
                parse_fce()

            elif (value == 2):
                service_contexts()

            elif (value == 4):
                parse_fcf()
                parse_fcd()
                parse_fce_domains()       

            elif (value ==5):
                only_domains()

            elif (value == 6):
                stock_fc()

            elif (value == 7):
                stock_sepo()

            elif (value == 8):
                sepologparser_local()

            elif (value == 9):
                sepologparser_inet()

            elif (value == 00):
                cleanup()
