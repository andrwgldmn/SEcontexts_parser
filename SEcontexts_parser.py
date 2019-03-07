#! /usr/bin/env python
# -*- coding: utf-8 -*-
value = None
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
        print ("Not working for now. Will be implemented later.")
#        with open('file_contexts') as input_file: 
#            with open('file.te', 'w') as output_file:
#                for line in input_file:
#                    if len(line) > 2 and line[0] != '#':
#                        try:
#                            prop = line.split(':')[-2] 
#                        except IndexError:
#                            continue
#                        newline = 'type {}, property_type;\n'.format(prop)
#                        output_file.write(newline)
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
