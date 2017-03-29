using System;

class RandomGenerators{
  private static DateTime epoch = new DateTime(1970, 1, 1);
  // lcg
  private double lcg_prev;
  private double lcg_mod;
  private int lcg_a;
  private int lcg_c;
  // bbs
  private double bbs_mod;
  private double bbs_prev;
  // mwc
  private double mwc_prev;
  private double mwc_b;
  private int mwc_a;
  private int mwc_c;
  // xor
  private int xor_prev;
  public RandomGenerators(int seed=-1,int carry=-1){
    // lcg
    /*
    If you want to understand why having a bigger period is important, use the following
    numbers with lcg which produce a small period:
    lcg_mod = 10
    lcg_a = 2
    lcg_c = 3
    */
    lcg_mod = Math.Pow(2,31);    // modulus, usually power of 2 (2**32, 2**64, 2**31-1)
    lcg_a = 1103515245; // multiplier, arbitrary number (inventer Lehmer used 23)
    lcg_c = 12345;      // increment, usually prime (other common values are 1, 11)
    // bbs
    int p = 492876847; // large prime congruent to 3 ... (p %4==3)
    int q = 715225739; // large prime congruent to 3 ... (q %4==3)
    bbs_mod = p * q;
    bbs_prev = 920419823; // coprime with bbs_mod .... keep it prime for simplicity
    // mwc
    mwc_b = Math.Pow(2,32);
    mwc_a = 1103515245;
    // seed
    if(seed == -1){
      // seed set to number of seconds since epoch
      lcg_prev = (int)((DateTime.Now.ToUniversalTime() - epoch).TotalMilliseconds);
      mwc_prev = (int)((DateTime.Now.ToUniversalTime() - epoch).TotalMilliseconds);
      xor_prev = (int)((DateTime.Now.ToUniversalTime() - epoch).TotalMilliseconds);
    }else{
      lcg_prev = seed;
      mwc_prev = seed;
      xor_prev = seed;
    }
    // carry
    if( carry == -1){
      mwc_c = 3; // arbitrary carry
    }else{
      mwc_c = carry;
    }
  }

  public double next_LCG(){
    double rand_num = (lcg_prev * lcg_a + lcg_c) % lcg_mod;
    lcg_prev = rand_num; // update the state
    return lcg_prev / (double)(lcg_mod); // float between 0 and 1
  }

  public int next_LCG_range(int mini,int maxi){
    return mini + (int)(next_LCG() * ((maxi - mini) + 1));
  }

  public double next_BlumBlumShub(){
    double rand_num = (Math.Pow(bbs_prev,2)) % bbs_mod;
    bbs_prev = rand_num;
    return rand_num / bbs_mod;
  }

  public double next_MWC(){
    double t = mwc_a * mwc_prev + mwc_c;
    double rand_num = t % mwc_b;
    mwc_prev = rand_num;
    mwc_c = (int)(t / mwc_b);
    return rand_num / (double)(mwc_b);
  }

  public double next_xorshift(){
    int rand_num = xor_prev;
    rand_num ^= (rand_num << 21);
    rand_num ^= (rand_num >> 35);
    rand_num ^= (rand_num << 4);
    xor_prev = rand_num;
    return (rand_num & 0xFFFFFFFF) / (double)(0xFFFFFFFF);
    // (& 0xFFFFFFFF trunctates the number), divide by uint32 value for [0,1)
  }
}

class MainClass {
  public static void Main (string[] args) {
    RandomGenerators r=new RandomGenerators(125);
    for(int i=0;i<50;i++){
      Console.WriteLine("lcg: " + r.next_LCG());
      Console.WriteLine("bbs: " + r.next_BlumBlumShub());
      Console.WriteLine("mwc: " + r.next_MWC());
      Console.WriteLine("xor: " + r.next_xorshift());
      Console.WriteLine("***********");
    }
  }
}
