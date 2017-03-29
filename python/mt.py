''' 
   A C-program for MT19937, with initialization improved 2002/1/26.
   Coded by Takuji Nishimura and Makoto Matsumoto.

   Before using, initialize the state by using init_genrand(seed)
   or init_by_array(init_key, key_length).

   Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:

     1. Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.

     2. Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.

     3. The names of its contributors may not be used to endorse or promote
        products derived from this software without specific prior written
        permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


   Any feedback is very welcome.
   http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html
   email: m-mat @ math.sci.hiroshima-u.ac.jp (remove space)
'''
import time

class RandomGenerators:
  # period parameters
  N = 624
  M = 394
  MATRIX_A = 0x9908b0df    # constant vector a
  UPPER_MASK = 0x80000000  # most significant w-r bits
  LOWER_MASK = 0x7fffffff  # least significant r bits

  def __init__(self):
    self.mt = [None]
    self.mti = self.N + 1

  '''
  initialize by an array with array-length
  init_key is the array for initializing keys
  key_length is its length
  slight change for C++, 2004/2/26
  '''
  def init_by_array(self, init_key, key_length):
    self.init_genrand(19650218)
    i,j = 1,0
    k = self.N if self.N > key_length else key_length
    while k > 0:
      self.mt[i] = (self.mt[i] ^ ((self.mt[i-1] ^ (self.mt[i-1] >> 30)) * 1664525)) + init_key[j] + j # non linear
      self.mt[i] &= 0xFFFFFFFF # for WORDSIZE > 32 machines
      i+=1
      j+=1
      if i >= self.N:
        self.mt[0] = self.mt[self.N-1]
        i = 1
      if j >= key_length:
        j = 0
      k-=1

    k = self.N-1
    while k > 0:
      self.mt[i] = (self.mt[i] ^ ((self.mt[i-1] ^ (self.mt[i-1] >> 30)) * 1566083941)) - i # non linear
      self.mt[i] &= 0xffffffff # for WORDSIZE > 32 machines

      i += 1
      if i >= self.N:
        self.mt[0] = self.mt[self.N-1]
        i=1
      k-=1

    for i,num in enumerate(self.mt):
      if num>=2147483648: # (2**32)/2
        self.mt[i]-=4294967296 # 2**32

    self.mt[0] = 0x80000000 # MSB is 1; assuring non-zero initial array
    if self.mt[0] >= 2147483648:
        self.mt[0] -= 4294967296
    for i in self.mt:
      print(i)

  # initializes mt[N] with a seed
  def init_genrand(self,s):
    self.mt[0] = s & 0xffffffff
    self.mti = 1
    while self.mti < self.N:
      self.mt.append(1812433253 * (self.mt[self.mti-1] ^ (self.mt[self.mti - 1] >> 30)) + self.mti)
      self.mt[self.mti] &= 0xffffffff
      self.mti += 1

  # generates a random number on [0,0xffffffff]-interval
  def genrand_int32(self):
    y = 0
    mag01=[0x0, self.MATRIX_A]
    if self.mti >= self.N: # generate N words at one time
      kk = 0
      if self.mti == self.N + 1: # if init_genrand() has not been called,
        self.init_genrand(5489) # a default initial seed is used

      while kk < self.N - self.M:
        y = (self.mt[kk] & self.UPPER_MASK) | (self.mt[kk+1] & self.LOWER_MASK)
        self.mt[kk] = self.mt[kk+self.M] ^ (y >> 1) ^ mag01[y & 0x1]
        kk += 1

      while kk < self.N - 1:
        y = (self.mt[kk] & self.UPPER_MASK) | (self.mt[kk+1] & self.LOWER_MASK)
        self.mt[kk] = self.mt[kk+(self.M-self.N)] ^ (y >> 1) ^ mag01[y & 0x1]
        kk += 1

      y = (self.mt[self.N-1] & self.UPPER_MASK) | (self.mt[0] & self.LOWER_MASK)
      self.mt[self.N-1] = self.mt[self.M-1] ^ (y >> 1) ^ mag01[y & 0x1]

      self.mti = 0

    y = self.mt[self.mti]
    self.mti += 1

    # Tempering
    y ^= (y >> 11)
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)

    return y

  # generates a random number on [0,0x7fffffff]-interval
  def genrand_int31(self):
    #return (long)(genrand_int32() >> 1)
    return (self.genrand_int32() >> 1)

  # generates a random number on [0,1]-real-interval
  def genrand_real1(self):
    return self.genrand_int32() * (1.0 / 4294967295.0)
    # divided by 2^32-1

  # generates a random number on [0,1)-real-interval
  def genrand_real2(self):
    return self.genrand_int32() * (1.0 / 4294967296.0)
    # divided by 2^32

  # generates a random number on (0,1)-real-interval
  def genrand_real3(self):
    return ((self.genrand_int32()) + 0.5) * (1.0 / 4294967296.0)
    # divided by 2^32

  # generates a random number on [0,1) with 53-bit resolution
  def genrand_res53(self):
    a, b = self.genrand_int32()>>5, self.genrand_int32()>>6
    return(a * 67108864.0 + b) * (1.0 / 9007199254740992.0)

r = RandomGenerators()
init = [0x123, 0x234, 0x345, 0x456]
length = 4
r.init_by_array(init, length)
for i in range(10):
  print(str(r.genrand_int31())+' ', end="")
  if i%5==4:
    print()
print()
for i in range(10):
  print(str(r.genrand_real2())+' ', end="")
  if i%5==4:
    print()
