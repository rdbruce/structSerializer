
        # if not optional:
        #     self.classContent += "\t" + dtype + ' ' + name + ";\n"
        # elif optional:
        #     self.classContent += "\t" + "optional<" + dtype + "> " + name + ";\n"
        




# def structInC(name, members, serializeMethod, deserializeMethod):
#     return "struct " + name + " {\n" + members + "\n"+ serializeMethod + "\n" + deserializeMethod + "\n" + "};\n\n"

# for structName, struct in sch.items():
#     members = ""
#     serializeMethod = "\tvector<uint8_t> serialize() {\n\t\tjson j;\n" 
#     deserializeMethod = "\tvoid deserialize() {\n"
#     numEle = 0
#     for ele in struct:
#         if ele["type"] == "uint" or ele["type"] == "int" or ele["type"] == "string":
#             members += simpleTypeInC(ele["name"], ele["type"], ele["optional"])
#             serializeMethod += "\t\tj[" + str(numEle) + "] = " + ele["name"] + ";\n"
#             deserializeMethod += "\t\t// Hi\n"
#         numEle += 1
#     serializeMethod += "\t\treturn json::to_cbor(j);\n\t}\n"
#     deserializeMethod += "\t}\n"
#     body += structInC(structName, members, serializeMethod, deserializeMethod)