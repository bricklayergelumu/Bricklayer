#-*-coding:utf8-*-
import collections
class Solution:
    # @param start, a string
    # @param end, a string
    # @param dict, a set of string
    # @return an integer
    def __init__(self):
        self.res = []
        self.mp = collections.defaultdict(set)
        self.next_lev = set([])
        self.path = []
    def charfind(self,step,ladder,):
        begin = ord('a')
        end = ord('z')
        steplen = len(step)
        for i in range(steplen):
            part1 = step[:i]
            part2 = step[i+1:]
            for j in range(begin,end+1):
                nextstep = part1 + chr(j) + part2
                if nextstep in ladder:
                    self.mp[nextstep].add(step)
                    self.next_lev.add(nextstep)

    def output(self,start,end):
        if start == end:
            self.path.reverse()
            self.res.append(self.path[:])
            self.path.reverse()
        else:
            for i in self.mp[end]:
                self.path.append(i)
                self.output(start,i)
                self.path.pop()
                
    def findLadders(self, start, end, dict):
        dict.add(end)
        cur_lev = set([start])
        self.path.append(end)
        while True:
            for i in cur_lev:
                dict.discard(i)
            for i in cur_lev:
                self.charfind(i,dict)
            if not self.next_lev:
                return []
            if end in self.next_lev:
                self.output(start,end)
                return list(self.res)
            cur_lev.clear()
            cur_lev.update(self.next_lev)
            self.next_lev.clear()
            
if __name__ == "__main__":
    s = set(["hot","dot","dog","lot","log"])
    sol = Solution()
    p = sol.findLadders("hit","cog",s)
    print p
