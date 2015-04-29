#-*-coding:utf8-*-
class Solution:
    # @param s, a string
    # @return a boolean
    def isPalindrome(self, s):
        length = len(s)
        rev = length - 1
        s = s.lower()
        if s == None or s == "":
            return True
        for i,j in enumerate(s):
            if rev <= i:
                return True
            if j.isalnum():
                while (s[rev].isalnum() == False) and rev > i:
                    rev = rev - 1
                if j != s[rev]:
                    return False
                rev = rev - 1

if __name__ == "__main__":
    s = raw_input('Input:')
    sol = Solution()
    p = sol.isPalindrome(s)
    print p
                     
                        
                
            

            
            
        
        
        
