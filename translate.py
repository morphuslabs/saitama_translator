from saitama_translator import *
import sys

# python .\translate.py vy5xxxxvzz650coacbsf03f2jkviwui9.joexpediagroup.com oxn009lc7n5887k96c4zfckes6uif.joexpediagroup.com pqxwwk9cyl1upnxwyqwinn0wgzui5.uber-asia.com w7irwrisb5lxwkow81udr.uber-asia.com

if len(sys.argv) < 2:
    print (f'Please, inform the Saitama request to translate. Ex: python {sys.argv[0]} u6uosfnz3s.joexpediagroup.com')
    sys.exit(1)


t = Translator()
for req in sys.argv[1:]:
    translated = t.translate_req(req)
    print (translated)
