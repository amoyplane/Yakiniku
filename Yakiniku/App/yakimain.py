from . import quickstart as qs
from . import drawline as draw
from . import embeded as emb
from . import infostruct as ifs
import sys


def doall(infile, showfile, outfile):
    # f = open('ans.txt', 'w')
    # file_name='/root/pic/t3.jpg'
    file_name = infile
    # os.system("export GOOGLE_APPLICATION_CREDENTIALS=\"/root/mykey.json\"")
    rst = []
    '''
    bound = [[405, 103], [405, 278], [285, 278], [285, 103]]
    text = "もう夏休みも終わっちゃうけど…"
    trans = '暑假已经快要结束了……'
    info = ifs.Info(bound, 1, text, trans, 0)
    rst.append(info)

    bound = [[1010, 575], [1010, 732], [1091, 732], [1091, 575]]
    text = "脚本完成できそう？"
    trans = '脚本似乎还能做得完？'
    info = ifs.Info(bound, 1, text, trans, 1)
    rst.append(info)

    bound = [[1254, 1352], [1254, 1487], [1180, 1487], [1180, 1352]]
    text = "何とかする……"
    trans = '要做些什么……'
    info = ifs.Info(bound, 1, text, trans, 2)
    rst.append(info)

    bound = [[899, 1433], [899, 1616], [836, 1616], [836, 1433]]
    text = "大丈夫……？"
    trans = '你还好吗…？'
    info = ifs.Info(bound, 1, text, trans, 3)
    rst.append(info)

    bound = [[789, 1593], [789, 1733], [676, 1733], [676, 1593]]
    text = "明日家行ってもいい？"
    trans = '明天我可以去你家吗？'
    info = ifs.Info(bound, 1, text, trans, 4)
    rst.append(info)

    bound = [[1345, 399], [1345, 1917], [1297, 1917], [1297, 399]]
    text = "生徒会劇を、より面白いものに……そう決めて興奮するこよみだったけれど……？"
    trans = '让学生会的节目更加有趣——下定决心的历开始兴奋起来但……？'
    info = ifs.Info(bound, 1, text, trans, 5, True)
    rst.append(info)
    '''
    rst = qs.run_quickstart(file_name)
    #qs.drawShow(file_name, showfile, rst)

    # draw.openpic(file_name)
    # draw.writepic(showfile)
    # f.close()

    emb.Embeded(infile, outfile, rst)

    return rst


def renew(infos, infile, showfile, outfile):
    #qs.drawShow(infile, showfile, infos)
    emb.Embeded(infile, outfile, infos)


if __name__ == '__main__':
    ret = doall('/root/pic/' + sys.argv[1], 'sho_' + sys.argv[1], 'rst_' + sys.argv[1])
