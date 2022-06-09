import zlib
import ctypes


class RandomMersenneTwister:
    def __init__(self, seed):
        self.state = []
        self.f = 1812433253
        self.m = 397
        self.u = 11
        self.s = 7
        self.b = 2636928640
        self.t = 15
        self.c = 4022730752
        self.l = 18
        self.index = 624
        self.lower_mask = 2147483647
        self.upper_mask = 2147483648
        self.state.append(seed)
        for i in range (1, 624):
            self.state.append(Util.myint32((self.f * (self.state[i - 1] ^ self.state[i - 1] >> 30)) + i))

    
    def twist(self):
        for num in range(0, 624):
            num2 = int(((self.state[int(num)] & self.upper_mask) + (self.state[int(((num + 1) % 624))] & self.lower_mask)))
            num3 = num2 >> 1
            if (num2 % 2 != 0):
                num3 = int(((num3 ^ 2567483615)))
        
            self.state[int(num)] = (self.state[int(((num + self.m) % 624))] ^ num3)
        self.index = 0
    
    def GetRandomNumber(self):
    
        if (self.index >= 624):
            self.twist()
    
        num = self.state[int(self.index)]
        num ^= num >> int(self.u)
        num ^= (num << int(self.s) & self.b)
        num ^= (num << int(self.t) & self.c)
        num ^= num >> int(self.l)
        self.index += 1
        return int(num)

    def GetRandomRange(self, min, max):
        num = max - min;
        randomNumber = self.GetRandomNumber()
        return int((min + randomNumber % num));

class Message:
    
    def __init__(self):
        self.msg_type = None
        self.agent_id = None
        self.content = None
        self.offset = None
        self.datasize = None
        self.start_packet = False
        self.request = None
        self.decoded_content=None
        self.count=None

    def __str__(self):
        return ("agent_id: %s,\tmsg_type: %s,\tmsg_offset:%s,\tmsg_size:%s,\tmsg_content:%s,\trequest:%s,\tcount:%s" % (self.agent_id, self.msg_type, self.offset, self.datasize,self.decoded_content,self.request,self.count))


class Util:

    def myint32(num):
        return ctypes.c_uint32(num).value

    def remove_at(i, s):
        return s[:i] + s[i+1:]
    
    def deflate(content):
        try:
            inflated = zlib.decompress(content , -15)
            return inflated
        except:
            return content
