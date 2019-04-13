#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import os
from data.config import cfg
import cv2

#WIDER_ROOT = os.path.join(cfg.HOME, 'WIDER')
# train_list_file = os.path.join(WIDER_ROOT, 'wider_face_split',
#                                'wider_face_train_bbx_gt.txt')
# val_list_file = os.path.join(WIDER_ROOT, 'wider_face_split',
#                              'wider_face_val_bbx_gt.txt')
#
# WIDER_TRAIN = os.path.join(WIDER_ROOT, 'WIDER_train', 'images')
# WIDER_VAL = os.path.join(WIDER_ROOT, 'WIDER_val', 'images')


WIDER_ROOT = os.path.join(cfg.HOME, 'DarkFace_Train')
train_list_file = os.path.join(WIDER_ROOT, 'df_wider_face_train_bbx_gt.txt')
val_list_file = os.path.join(WIDER_ROOT, 'df_wider_face_val_bbx_gt.txt')

WIDER_TRAIN = os.path.join(WIDER_ROOT, 'images')
WIDER_VAL = os.path.join(WIDER_ROOT, 'images')


# def parse_wider_file(root, file):
def parse_df_file(root, file):
    print('>>> In parse_df_file()')
    print(file)
    with open(file, 'r') as fr:
        lines = fr.readlines()
    face_count = []
    img_paths = []
    face_loc = []
    img_faces = []
    count = 0
    flag = False
    for k, line in enumerate(lines):
        line = line.strip().strip('\n')
        if count > 0:
            line = line.split(' ')
            count -= 1
            # loc = [int(line[0]), int(line[1]), int(line[2]), int(line[3])]
            x =  int(line[0])
            y =  int(line[1])
            w =  int(line[2]) - int(line[0])
            h =  int(line[3]) - int(line[1])
            loc = [x, y, w, h]
            face_loc += [loc]
        if flag:
            face_count += [int(line)]
            flag = False
            count = int(line)
        if 'png' in line:
            # if 'jpg' in line:
            img_paths += [os.path.join(root, line)]
            flag = True

    total_face = 0
    for k in face_count:
        face_ = []
        for x in range(total_face, total_face + k):
            face_.append(face_loc[x])
        img_faces += [face_]
        total_face += k
    return img_paths, img_faces


def df_data_file():
    img_paths, bbox = parse_df_file(WIDER_TRAIN, train_list_file)
    print(img_paths)
    print(bbox)
    fw = open(cfg.FACE.TRAIN_FILE, 'w')
    for index in range(len(img_paths)):
        path = img_paths[index]
        boxes = bbox[index]
        fw.write(path)
        fw.write(' {}'.format(len(boxes)))
        for box in boxes:
            data = ' {} {} {} {} {}'.format(box[0], box[1], box[2], box[3], 1)
            fw.write(data)
        fw.write('\n')
    fw.close()

    img_paths, bbox = parse_df_file(WIDER_VAL, val_list_file)
    fw = open(cfg.FACE.VAL_FILE, 'w')
    for index in range(len(img_paths)):
        path = img_paths[index]
        boxes = bbox[index]
        fw.write(path)
        fw.write(' {}'.format(len(boxes)))
        for box in boxes:
            data = ' {} {} {} {} {}'.format(box[0], box[1], box[2], box[3], 1)
            fw.write(data)
        fw.write('\n')
    fw.close()


if __name__ == '__main__':
    df_data_file()
