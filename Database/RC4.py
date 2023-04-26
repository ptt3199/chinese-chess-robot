# RC4 algorithm
class RC4:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = []
        self.RC4_key([0])

    def swap(self, i, j):
        t = self.state[i]
        self.state[i] = self.state[j]
        self.state[j] = t

    def RC4_key(self, key):
        for i in range(0, 256):
            self.state.append(i)
        j = 0
        for i in range(0, 256):
            j = (j + self.state[i] + key[i % len(key)]) & 0xff
            self.swap(i, j)

    def nextByte(self):
        self.x = (self.x + 1) & 0xff
        self.y = (self.y + self.state[self.x]) & 0xff
        self.swap(self.x, self.y)
        t = (self.state[self.x] + self.state[self.y]) & 0xff
        return self.state[t]

    def nextLong(self):
        n0 = self.nextByte()
        n1 = self.nextByte()
        n2 = self.nextByte()
        n3 = self.nextByte()
        return n0 + (n1 << 8) + (n2 << 16) + ((n3 << 24) & 0xffffffff)
