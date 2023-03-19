
class yaziNum():
    def __init__(self,nextNum,zNum):
        self.nextNum = nextNum #经过x村庄后的数量
        self.zNum = zNum # 经过的x村庄是正数第zNum个

    def getZNum(self):
        # 判断当前还剩几个村庄，倒数第一个村庄
        if self.zNum == 1:
            x = (self.nextNum+1)*2 #经过村庄前的数量

            print(f'经过第一个村庄前的数量为{x},经过第一个村庄后的数量为{self.nextNum}')
        else:
            x =  (self.nextNum+1)*2
            print(f'经过第{self.zNum}个村庄前的数量为{x},经过第{self.zNum}个村庄后的数量为{self.nextNum}')
            lastzNum = self.zNum-1
            return yaziNum(nextNum=x,zNum = lastzNum).getZNum()

if __name__ == '__main__':
    yaziNum(nextNum = 2,zNum = 7).getZNum()