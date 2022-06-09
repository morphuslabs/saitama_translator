import base64
from saitama_util import *
import math

class Translator:
    
    def __init__(self, debug=False, basestring=''):
        if basestring == '':
            self.basestring="razupgnv2w01eos4t38h7yqidxmkljc6b9f5"
        else:
            self.basestring=basestring
        self.alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
        self.random_string=""
        self.debug=debug
        
        
    def charpos(self, c, alphabet):
        for i in range(0, len(alphabet)):
            if alphabet[i]==c:
                return i

    def stringtoint(self, value, alphabet):
        number = 0
        lenvalue=len(value)-1
        for i in value:
            number += self.charpos(i, alphabet) * pow(36, lenvalue)
            lenvalue -= 1
        return number
    
    def inttostring(self, value):
        text = ""
        length = len(self.basestring)
        while int(value) > 0:
            text = self.basestring[math.floor(value % length)] + text
            value /= length
        return text
    
    def shuffle(self, seed):
        text = self.alphabet
        length = len(text)
        text2 = ""
        randomMersenneTwister = RandomMersenneTwister(seed)

        for i in range(0, length):
            randomRange = randomMersenneTwister.GetRandomRange(0, len(text))
            text2 += str(text[randomRange])
            text = Util.remove_at(randomRange, text)
        return text2

    def get_random_string(self, count):
        return self.shuffle(count)
    
    def translate_req_array(self, req_array):
        for req in req_array:
            yield self.translate_req(req)
        
    def translate_req(self, request, count=0):
        message = request.split('.')[0]
        first_part = message[:len(message)-3]
        second_part = message[len(message)-3:]
        if count == 0:
            count = self.stringtoint(second_part, self.basestring)
        
        self.random_string = self.get_random_string(count)
        
        if len(message) == 5:
            agent_id_init_sep = 0
            agent_id_final_sep = 2
        else:
            agent_id_init_sep = 1
            agent_id_final_sep = 3
        
        msg = Message()
        msg.count = count
        msg.msg_type=self.stringtoint(first_part[0], self.random_string)
        if msg.msg_type != 0:
            msg.agent_id=self.stringtoint(first_part[agent_id_init_sep:agent_id_final_sep], self.random_string)
        else:
            msg.agent_id = 0
        
        msg.offset=self.stringtoint(first_part[4:6], self.random_string)
        msg.request=request
        
        if 'aharuto' in (self.translate_message(first_part, self.random_string)):
            msg.decoded_content = 'aharuto'
            return msg
        
        if msg.offset == 0:
            msg.datasize = self.stringtoint(first_part[7:9], self.random_string)
            msg.content = self.translate_message(first_part[9:], self.random_string)
            msg.start_packet = True
        else:
            msg.content = self.translate_message(first_part[6:], self.random_string)
        
        bstring = msg.content
        bstring += '=' * (-len(bstring) % 8)
        msg.decoded_content = base64.b32decode(bstring.upper())

        return msg
        
    def translate_message(self, message, alphabet):
        
        corresponding_alpha = dict()
        j=0
        for i in alphabet:
            corresponding_alpha[i]=self.alphabet[j]
            j+=1
        translated_msg = ""
        for i in message:
            translated_msg += corresponding_alpha[i]
        
        return translated_msg
