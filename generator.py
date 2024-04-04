#!/usr/bin/env python3

from dataclasses import fields, is_dataclass
from typing import *
from typing import get_origin, get_args
from enum import Enum

def legitimateType(checkType):
    if get_origin(checkType) is None:
        if get_origin(checkType) is None and checkType == bool or checkType == int or checkType == float or checkType == str or is_dataclass(checkType) or issubclass(checkType, Enum):
            return True
        else:
            return False
    else:
        return False

class structInCpp:
    structWhole = ''
    structMembers = ''
    toJsonMethod = '\tjson toJson() {\n\t\tjson j;\n'
    fromJsonMethod = '\tvoid fromJson(json j) {\n'
    serializeMethod = '\tvector<uint8_t> serialize() {\n' 
    deserializeMethod = '\tvoid deserialize(vector<uint8_t> ourCbor) {\n'
    def __init__(self, structObj):
        self.structWhole += f'struct {structObj.__name__} {{\n'

        for index, field in enumerate(fields(structObj)):
            if get_origin(field.type) is None:
                if legitimateType(field.type):
                    print(f'## {field.type.__name__} {field.name}')
                    self.__addUnconType(field.name, field.type, index)

                else:
                    print(f'## {field.type} {field.name} ERROR: UNSUPPORTED TYPE')
                    quit()
            else:
                self.__addConType(field.name, field.type, index)

    def __returnCType(self, dtype):
        if dtype == str:
            return 'string'
        else:
            return dtype.__name__

    def __recurse(self, root, depth = 1):
        pad = '##' * depth + ' '
        origin = get_origin(root)
        #STD MAP
        if origin is dict:
            args = get_args(root)
            print(f'{pad}dict key={args[0]} value={args[1]}')
            self.structMembers += f'map<{self.__returnCType(args[0])}, '
            if legitimateType(args[1]):
                self.structMembers += f'{self.__returnCType(args[1])}>'
            else:
                self.__recurse(args[1], depth=depth+1)
                self.structMembers += f'>'
        #STD Array
        elif origin is Annotated:
            args = get_args(root)
            print(f'{pad}annotated type={args[0]} length={args[1]}')
            self.structMembers += f'array<'
            if legitimateType(get_args(args[0])[0]):
                self.structMembers += f'{self.__returnCType(get_args(args[0])[0])}, {args[1]}>'
            else:
                self.__recurse(args[0], depth=depth+1)
                self.structMembers += f', {args[1]}>'
        #STD Vector
        elif origin is list:
            args = get_args(root)
            print(f'{pad}list value={args[0]}')
            self.structMembers += f'vector<'
            if legitimateType(args[0]):
                self.structMembers += f'{self.__returnCType(args[0])}>'
            else:
                self.__recurse(args[0], depth=depth+1)
                self.structMembers += f'>'
        #Error
        else:
            print(f'{type(root)} ERROR: UNSUPPORTED TYPE')
            print('ERROR: UNSUPPORTED TYPE')
            quit()

    def __addUnconType(self, fieldName, dtype, index):
        self.structMembers += f'\t{self.__returnCType(dtype)} {fieldName};\n'
        if is_dataclass(dtype):
            self.toJsonMethod += f'\t\tj[{index}] = {fieldName}.toJson();\n'
            self.fromJsonMethod += f'\t\t{fieldName}.fromJson(j[{index}]);\n'
        elif not issubclass(dtype, Enum):
            self.toJsonMethod += f'\t\tj[{index}] = {fieldName};\n'
            self.fromJsonMethod += f'\t\t{fieldName} = j[{index}];\n'

    def __addConType(self, fieldName, root, index):
        self.structMembers += f'\t'
        self.__recurse(root)
        self.structMembers += f' {fieldName};\n'
        self.toJsonMethod += f'\t\tj[{index}] = {fieldName};\n'
        self.fromJsonMethod += f'\t\t{fieldName} = j[{index}];\n'

    def returnCpp(self):
        self.structMembers += '\n'
        self.toJsonMethod += '\t\treturn j;\n\t}\n\n'
        self.fromJsonMethod += '\t}\n\n'
        self.serializeMethod += '\t\treturn json::to_cbor(toJson());\n\t}\n\n'
        self.deserializeMethod += '\t\tfromJson(json::from_cbor(ourCbor));\n\t}\n\n'
        self.structWhole += self.structMembers + self.toJsonMethod + self.serializeMethod + self.fromJsonMethod + self.deserializeMethod + f'}};\n\n'
        return self.structWhole
    
class enumInCpp:
    structMembers = ""
    def __init__(self, enumObj):
        self.structMembers += f'enum {enumObj.__name__} {{\n'
        for num in enumObj:
            print(f'## {num.name} and {num.value}')
            self.structMembers += f'\t{num.name} = {num.value},\n'

    def returnCpp(self):
        self.structMembers += f'}};\n\n'
        return self.structMembers

def generateCPP(*args):
    head = """#include <iostream>
#include <map>
#include <array>
#include <list>
#include <optional>
#include <stdlib.h>
#include <nlohmann/json.hpp>
#include <boost/core/demangle.hpp>

using json = nlohmann::json;
using boost::core::demangle;
using namespace std;

"""

    body = ''

    for obj in args:
        # If obj is dataclass
        if is_dataclass(obj):
            print(f'dataclass {obj.__name__}')
            sIC = structInCpp(obj)
            body += sIC.returnCpp()
        # If obj is enum
        elif issubclass(obj, Enum):
            print(f'enum {obj.__name__}')
            eIC = enumInCpp(obj)
            body += eIC.returnCpp()
        # If obj is unrecognized
        else:
            print(f'{type(obj)} {obj.__name__} ERROR: UNSUPPORTED TYPE')
            quit()
 
    with open("generated.h", 'w') as f:
        f.write(head + body)

