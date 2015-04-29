class Solution:
    # @return an integer
    def Candy(self, ratings):
        result = 0
        size = len(ratings)
        if size <= 1:
            return size
        num = [1 for i in range(size)]
        for i in range(1,size):
            if ratings[i] > ratings[i-1]:
                num[i] = num[i-1] + 1
        for i in range(size-1,0,-1):
            if ratings[i-1] > ratings[i]:
                num[i-1] = max(num[i-1],num[i] + 1)
        for i in num:
            result+= i
        return result
                
if __name__ == "__main__":
    n = [1,2,3,4,5]
    sol = Solution()
    p = sol.Candy(n)
    print p
