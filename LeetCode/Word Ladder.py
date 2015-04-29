#-*-coding:utf8-*-
import collections
class Solution:
    # @param start, a string
    # @param end, a string
    # @param dict, a set of string
    # @return an integer
    def __init__(self):
        self.mark = dict()
        self.rmark = dict()
    def compare(self,str1,str2):
        length = len(str1)
        mark = False
        for i in range(length):
            if str1[i] is not str2[i]:
                if mark is False:
                    mark = True
                else:
                    return False
        return True
    def charfind(self,step,ladder):
        begin = ord('a')
        end = ord('z')
        steplen = len(step)
        outcome = set()
        for i in range(steplen):
            part1 = step[:i]
            part2 = step[i+1:]
            for j in range(begin,end+1):
                nextstep = part1 + chr(j) + part2
                if nextstep in ladder:
                    outcome.add(nextstep)
        return outcome
                    
    def ladderLength(self, start, end, dict):
        length = 1
        rlength = 1
        queue = collections.deque([(start,1)])
        rqueue = collections.deque([(end,1)])
        if self.compare(start,end):
            return 2
        for i in dict:
            self.mark[i] = False
            self.rmark[i] = False
        while queue and rqueue:
            if len(queue) < len(rqueue):
                rcurr = rqueue[-1]
                curr = queue[0]
                while queue and curr[1] is length:
                    result = self.charfind(curr[0],dict)
                    for key in result:
                        if self.mark[key] is False:
                            self.mark[key] = True
                            if self.rmark[key] is True:
                                return curr[1] + rcurr[1]
                            queue.append((key,curr[1]+1))
                    queue.popleft()
                    if queue:
                        curr = queue[0]
                length+= 1
            else:
                rcurr = rqueue[0]
                curr = queue[-1]
                while rqueue and rcurr[1] is rlength:
                    result = self.charfind(rcurr[0],dict)
                    for key in result:
                        if self.rmark[key] is False:
                            self.rmark[key] = True
                            if self.mark[key] is True:
                                return rcurr[1] + curr[1]
                            rqueue.append((key,rcurr[1]+1))
                    rqueue.popleft()
                    if rqueue:
                        rcurr = rqueue[0]
                rlength+= 1
        return 0
        

if __name__ == "__main__":
    s = set(["hot","dog","dot"])
    sol = Solution()
    p = sol.ladderLength("hot","dog",s)
    print p
