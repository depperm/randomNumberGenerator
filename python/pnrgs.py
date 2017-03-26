import time

class RandomGenerators:

  def __init__(self,seed=None,carry=None):
    # lcg
    '''
    If you want to understand why having a bigger period is important, use the following
    numbers with lcg which produce a small period:
    self.lcg_mod = 10
    self.lcg_a = 2
    self.lcg_c = 3
    '''
    self.lcg_mod = 2**31    # modulus, usually power of 2 (2**32, 2**64, 2**31-1)
    self.lcg_a = 1103515245 # multiplier, arbitrary number (inventer Lehmer used 23)
    self.lcg_c = 12345      # increment, also semi arbitrary (other common values are 1, 11)
    # bbs
    p = 492876847 # large prime congruent to 3 ... (p %4==3)
    q = 715225739 # large prime congruent to 3 ... (q %4==3)
    self.bbs_mod = p * q
    self.bbs_prev = 920419823 # coprime with bbs_mod .... keep it prime for simplicity
    # mwc
    self.mwc_b = 2**32
    self.mwc_a = 1103515245
    # seed
    if seed == None:
      # seed set to number of seconds since epoch
      self.lcg_prev = int(time.time())
      self.mwc_prev = int(time.time())
      self.xor_prev = int(time.time())
    else:
      self.lcg_prev = seed
      self.mwc_prev = seed
      self.xor_prev = seed
    # carry
    if carry == None:
      self.mwc_c = 3 # arbitrary carry
    else:
      self.mwc_c = carry

  def next_LCG(self):
    rand_num = (self.lcg_prev * self.lcg_a + self.lcg_c) % self.lcg_mod
    self.lcg_prev = rand_num # update the state
    return self.lcg_prev / float(self.lcg_mod) # float between 0 and 1

  def next_LCG_range(self,mini,maxi):
    return mini + (int)(self.next_LCG() * ((maxi - mini) + 1))

  def next_BlumBlumShub(self):
    rand_num = (self.bbs_prev**2) % self.bbs_mod
    self.bbs_prev = rand_num
    return rand_num / float(self.bbs_mod)

  def next_MWC(self):
    t = self.mwc_a * self.mwc_prev + self.mwc_c
    rand_num = t % self.mwc_b
    self.mwc_prev = rand_num
    self.mwc_c = int(t / self.mwc_b)
    return rand_num / float(self.mwc_b)

  def next_xorshift(self):
    rand_num = self.xor_prev
    rand_num ^= (rand_num << 21)
    rand_num ^= (rand_num >> 35)
    rand_num ^= (rand_num << 4)
    self.xor_prev = rand_num
    return (rand_num & 0xFFFFFFFF) / float(0xFFFFFFFF)
    # (& 0xFFFFFFFF trunctates the number), divide by uint32 value for [0,1)

r=RandomGenerators()
for i in range(50):
  print('lcg: ' + str(r.next_LCG()))
  print('bbs: ' + str(r.next_BlumBlumShub()))
  print('mwc: ' + str(r.next_MWC()))
  print('xor: ' + str(r.next_xorshift()))
  print('***********')
