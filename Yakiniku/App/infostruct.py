class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Info:
    def __init__(self, points=[], direction=1, text='', trans='', id=0, bold=False):
        self.vertexs = points
        self.direct = direction
        self.text = text
        self.trans = trans
        self.id = id
        self.enable = 1
        self.bold = bold

    def showInfo(self):
        print('Info id = ', end=' ')
        print(self.id)
        for vet in self.vertexs:
            print('[' + str(vet[0]) + ',' + str(vet[1]) + ']', end=' ')
        print()
        print('Direction = ', end=' ')
        print(self.direct)
        print(self.text)
        print(self.trans)
        print(self.bold)

    def expand(self, num):
        self.vertexs[0][0] = self.vertexs[0][0] - num
        self.vertexs[0][1] = self.vertexs[0][1] - num
        self.vertexs[1][0] = self.vertexs[1][0] + num
        self.vertexs[1][1] = self.vertexs[1][1] - num
        self.vertexs[2][0] = self.vertexs[2][0] + num
        self.vertexs[2][1] = self.vertexs[2][1] + num
        self.vertexs[3][0] = self.vertexs[3][0] - num
        self.vertexs[3][1] = self.vertexs[3][1] + num

    def shrink(self, num):
        self.vertexs[0][0] = self.vertexs[0][0] + num
        self.vertexs[0][1] = self.vertexs[0][1] + num
        self.vertexs[1][0] = self.vertexs[1][0] - num
        self.vertexs[1][1] = self.vertexs[1][1] + num
        self.vertexs[2][0] = self.vertexs[2][0] - num
        self.vertexs[2][1] = self.vertexs[2][1] - num
        self.vertexs[3][0] = self.vertexs[3][0] + num
        self.vertexs[3][1] = self.vertexs[3][1] - num

    def changeL(self, num):
        self.vertexs[0][0] = self.vertexs[0][0] + num
        self.vertexs[3][0] = self.vertexs[3][0] + num

    def changeR(self, num):
        self.vertexs[1][0] = self.vertexs[1][0] + num
        self.vertexs[2][0] = self.vertexs[2][0] + num

    def changeU(self, num):
        self.vertexs[0][1] = self.vertexs[0][1] + num
        self.vertexs[1][1] = self.vertexs[1][1] + num

    def changeD(self, num):
        self.vertexs[1][1] = self.vertexs[1][1] + num
        self.vertexs[2][1] = self.vertexs[2][1] + num

    def changeDir(self, gdir):
        self.direct = gdir

    def changeTrans(self, trans):
        self.trans = trans

    def changeStatus(self, sta):
        self.enable = sta


if __name__ == '__main__':
    a = Info([[11, 222], [33, 455], [15, 326], [237, 1348]], 1, 'abc', 'def', 2)
    a.showInfo()
    a.expand(5)
    a.showInfo()
    a.shrink(3)
    a.showInfo()
