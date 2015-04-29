#-*-coding:utf8-*-
class Solution:
    # @return a string
    def countAndSay(self, n):
        curstring = '1'
        for i in range(1,n):
            cursum = 0
            strlen = len(curstring)
            cursor = None
            curtemp = ''
            for j in curstring:
                if cursor is None:
                    cursor = j
                    cursum+= 1
                elif cursor is not j:
                    curtemp+= str(cursum) + cursor
                    cursum = 1
                    cursor = j
                elif j is cursor:
                    cursum+= 1
            curtemp+= str(cursum) + cursor
            curstring = curtemp
        return curstring

        
if __name__ == "__main__":
    sol = Solution()
    print sol.countAndSay(25)
                
                        
                    
            
