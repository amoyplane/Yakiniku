#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START vision_quickstart]
import io
import os
import sys
import copy
# import socket
# import requests
# import socks

# Imports the Google Cloud client library
# [START vision_python_migration_import]
from google.cloud import vision
from google.cloud.vision import types
# [END vision_python_migration_import]

from . import translate as trans
from . import drawline as draw
from . import infostruct as ifs


def sizefilter(vertices, v):
    minx = 999999999
    miny = 999999999
    maxx = -1
    maxy = -1
    for vertex in vertices:
        if vertex.x < minx:
            minx = vertex.x
        if vertex.x > maxx:
            maxx = vertex.x
        if vertex.y < miny:
            miny = vertex.y
        if vertex.y > maxy:
            maxy = vertex.y
    if ((maxx - minx < v) or (maxy - miny < v)):
        return True
    return False


def expand(vertices, v):
    t_vertices = copy.deepcopy(vertices)
    t_vertices[0].x = t_vertices[0].x - v
    t_vertices[1].x = t_vertices[1].x + v
    t_vertices[2].x = t_vertices[2].x + v
    t_vertices[3].x = t_vertices[3].x - v

    t_vertices[0].y = t_vertices[0].y - v
    t_vertices[1].y = t_vertices[1].y - v
    t_vertices[2].y = t_vertices[2].y + v
    t_vertices[3].y = t_vertices[3].y + v

    return t_vertices


def gettingdir(vertices):
    minx = 999999999
    miny = 999999999
    maxx = -1
    maxy = -1
    for vertex in vertices:
        if vertex.x < minx:
            minx = vertex.x
        if vertex.x > maxx:
            maxx = vertex.x
        if vertex.y < miny:
            miny = vertex.y
        if vertex.y > maxy:
            maxy = vertex.y
    dx = maxx - minx
    dy = maxy - miny
    if (dx <= dy):
        return 1
    return 0


def run_quickstart(file_name, diction):
    ret = []
    namelist1 = ['田ad中', '佐ad藤', '鈴ad木', '高ad橋', '渡ad辺', '伊ad藤', '山ad本', '中ad村', '小ad林', '加ad藤']
    namelist2 = ['田中', '佐藤', '鈴木', '高橋', '渡辺', '伊藤', '山本', '中村', '小林', '加藤']
    namelist3 = ['田中', '佐藤', '铃木', '高桥', '渡边', '伊藤', '山本', '中村', '小林', '加藤']

    # Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]

    # The name of the image file to annotate
    # file_name = os.path.join(os.path.dirname(__file__),'t3.jpg')
    # file_name = os.path.join('/root/pic/', 't3.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Performs label detection on the image file
    response = client.document_text_detection(image=image)

    blocki = 0
    infoc = 0
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            if (block.block_type != 1):
                continue
            if sizefilter(block.bounding_box.vertices, 20):
                continue
            # print('{}\n'.format(block.confidence))
            # print('{}\n'.format(block.block_type))

            # f.write('\nBlock confidence: {}\n'.format(block.confidence))

            blocki = blocki + 1
            # f.write('Block # {} :\n'.format(blocki))
            vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in block.bounding_box.vertices])

            # f.write('bounds: {} \n'.format(','.join(vertices)))

            # block.bounding_box.vertices[1].x
            '''
            draw.drawline((block.bounding_box.vertices[0].x, block.bounding_box.vertices[0].y), (block.bounding_box.vertices[1].x, block.bounding_box.vertices[1].y), (0, 255, 0))
            draw.drawline((block.bounding_box.vertices[1].x, block.bounding_box.vertices[1].y), (block.bounding_box.vertices[2].x, block.bounding_box.vertices[2].y), (0, 255, 0))
            draw.drawline((block.bounding_box.vertices[2].x, block.bounding_box.vertices[2].y), (block.bounding_box.vertices[3].x, block.bounding_box.vertices[3].y), (0, 255, 0))
            draw.drawline((block.bounding_box.vertices[3].x, block.bounding_box.vertices[3].y), (block.bounding_box.vertices[0].x, block.bounding_box.vertices[0].y), (0, 255, 0))
            '''

            tbound = expand(block.bounding_box.vertices, 20)
            '''
            draw.drawline((tbound[0].x, tbound[0].y), (tbound[1].x, tbound[1].y), (0, 255, 0))
            draw.drawline((tbound[1].x, tbound[1].y), (tbound[2].x, tbound[2].y), (0, 255, 0))
            draw.drawline((tbound[2].x, tbound[2].y), (tbound[3].x, tbound[3].y), (0, 255, 0))
            draw.drawline((tbound[3].x, tbound[3].y), (tbound[0].x, tbound[0].y), (0, 255, 0))
            '''

            for paragraph in block.paragraphs:
                # f.write('Paragraph confidence: {}'.format(
                #    paragraph.confidence))

                centence = ''

                for word in paragraph.words:
                    if sizefilter(word.bounding_box.vertices, 20):
                        continue

                    vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in word.bounding_box.vertices])
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    # f.write('Word text: {} '.format(word_text))
                    # f.write('bounds: {} \n'.format(','.join(vertices)))
                    centence = centence + word_text

                ifb = ifs.Info()
                ifb.id = infoc
                infoc = infoc + 1
                vet = []
                for vertex in paragraph.bounding_box.vertices:
                    vet.append([vertex.x, vertex.y])
                ifb.vertexs = vet
                ifb.direct = gettingdir(paragraph.bounding_box.vertices)
                # f.write('centence : {}\n'.format(centence))
                ifb.text = centence
                i = 0
                for dic in diction:
                    centence = centence.replace(dic[0], namelist1[i])
                    i = i + 1
                i = 0
                for dic in diction:
                    centence = centence.replace(namelist1[i], namelist2[i])
                    i = i + 1
                transans = trans.ask_translation('ja', centence)
                i = 0
                for dic in diction:
                    centence = centence.replace(namelist3[i], dic[1])
                    i = i + 1
                ifb.trans = transans
                ifb.user = transans
                # f.write('translation : {}\n'.format(transans))

                ifb.showInfo()
                ret.append(ifb)
    return ret


def drawShow(infile, outfile, infos):
    draw.openpic(infile)
    for item in infos:
        if (item.enable != 1):
            continue
        b = item.vertexs
        draw.drawline((b[0][0], b[0][1]), (b[1][0], b[1][1]), (0, 255, 0))
        draw.drawline((b[1][0], b[1][1]), (b[2][0], b[2][1]), (0, 255, 0))
        draw.drawline((b[2][0], b[2][1]), (b[3][0], b[3][1]), (0, 255, 0))
        draw.drawline((b[3][0], b[3][1]), (b[0][0], b[0][1]), (0, 255, 0))
    draw.writepic(outfile)


if __name__ == '__main__':

    f = open('ans.txt', 'w')

    # file_name='/root/pic/t3.jpg'
    file_name = '/root/pic/' + sys.argv[1]

    draw.openpic(file_name)

    os.system("export GOOGLE_APPLICATION_CREDENTIALS=\"/root/mykey.json\"")
    rst = run_quickstart(file_name)

    draw.writepic('pro_' + sys.argv[1])

    f.close()
