import base64
import codecs

def decode(coded_string):
    try:
        coded_string = coded_string.replace("FREDC", "==")
        coded_string = coded_string.replace("GHJKL", "=")
        coded_string = base64.b64decode(coded_string).decode('utf-8')
        coded_string = codecs.encode(coded_string, 'rot13')
        coded_string = coded_string[::-1]
        coded_string = base64.b64decode(coded_string).decode('utf-8')
        return coded_string
    except: return '-1'

def encode(string):
    try:
        string = string.encode('ascii')
        string = base64.b64encode(string)
        string = string.decode('utf-8')
        string = string[::-1]
        string = codecs.encode(string, 'rot13')
        string = string.encode('ascii')
        string = base64.b64encode(string)
        string = string.decode('utf-8')
        if '==' in string: string = string.replace("==", "FREDC")
        elif '=' in string: string = string.replace("=", "GHJKL")
        return string
    except: return '-1'