from . import quickstart as qs
from . import drawline as draw
from . import embeded as emb
import sys


def doall(infile, showfile, outfile):
    # f = open('ans.txt', 'w')
    # file_name='/root/pic/t3.jpg'
    file_name = infile
    # os.system("export GOOGLE_APPLICATION_CREDENTIALS=\"/root/mykey.json\"")
    rst = qs.run_quickstart(file_name)
    qs.drawShow(file_name, showfile, rst)
    # draw.openpic(file_name)
    # draw.writepic(showfile)
    # f.close()

    emb.Embeded(infile, outfile, rst)

    return rst


def renew(infos, infile, showfile, outfile):
    qs.drawShow(infile, showfile, infos)
    emb.Embeded(infile, outfile, infos)


if __name__ == '__main__':
    ret = doall('/root/pic/' + sys.argv[1], 'sho_' + sys.argv[1], 'rst_' + sys.argv[1])
