import math
class Solution:
    # @return an integer
    def trailingZeroes(self, n):
        res = math.factorial(n)
        znum = 0
        temp = 0
        while True:
            temp = res/10
            if temp * 10 == res:
                znum+=1
            else:
                return znum
            res = temp
if __name__ == "__main__":
    n = 10
    sol = Solution()
    p = sol.trailingZeroes(n)
    print p
