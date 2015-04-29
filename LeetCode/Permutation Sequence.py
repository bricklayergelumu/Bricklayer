import math
class Solution:
    def __init__(self):    
        self.psequence = ''
        self.sample = []
        self.seqlen = None
    # @return a string
    def numsearch(self,n,k,digit_count):
        factor = math.factorial(n)
        print 'factor:'+str(factor)
        batch = factor / n
        print 'batch:' + str(batch)
        off_count = k % batch if k % batch is not 0 else batch
        print 'off_count:' + str(off_count)
        offset = self.sample.pop(int(math.ceil(float(k) / batch - 1)))
        print 'offset:' + str(offset)
        self.psequence+= str(offset)
        if digit_count is not self.seqlen:
            self.numsearch(n-1,off_count,digit_count + 1)           
    def getPermutation(self, n, k):
        digit_count = 1
        self.seqlen = n
        for i in range(1,n+1):
            self.sample.append(str(i))
        self.numsearch(n,k,1)
if __name__ == "__main__":
    sol = Solution()
    sol.getPermutation(1,1)
    print sol.psequence
                
        
        
        
