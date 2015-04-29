#-*-coding:utf8-*-
class Solution:
    # @return a list of lists of integers
    def __init__(self):
        self.combin = []
        self.result = []
    def combination(self,n,k,level):
        if len(self.combin) == k:
            self.result.append(self.combin[:])
            return
        for i in range(level,n + 1):
            self.combin.append(i)
            self.combination(n,k,i + 1)
            self.combin.pop()        
    def combine(self, n, k):
        self.combination(n,k,1)
        return self.result
if __name__ == "__main__":
    sol = Solution()
    result = sol.combine(9,3)
    print result
    
        
