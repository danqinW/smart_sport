import json

import cv2

# from Actions import SimpleAction
from action_recognizer import ActionRecognizer
from video_source import VideoSource
from AlphaPose.AlphaDetector import AlphaDetector
from frame import Frame
import time_limiter

output = []
reasons = []

cfg_path = './data/210925/annotation.json'
data = {}
with open(cfg_path, 'r', encoding='utf8') as f:
    cfg = json.load(f)
    for k in cfg:
        action = ActionRecognizer(k, cfg[k], output, reasons)
        data[k] = action


detector = AlphaDetector()


def match(name, video_path, webcam=False, time_limit=None):
    video = VideoSource(video_path, webcam=webcam)
    recognizer = data[name]
    recognizer.clear()
    output = []
    recognizer.set_output(output)
    limiter = None
    if time_limit:
        limiter = time_limiter.TimeLimiter(time_limit)
        recognizer.set_time_limiter(limiter)

    for ori, frame_idx in video:
        cv2.imshow('frame', ori)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # if frame_idx == 248:
        #     cv2.imwrite('./2.png', ori)

        if limiter is not None and not limiter.if_continue(frame_idx):
            break
        pose_dic, angle_map = detector.pre_one_and_angle(ori)
        if pose_dic is None:
            continue
        frame = Frame(frame_idx, pose_dic, angle_map)
        recognizer.match(frame)

    output, reasons = recognizer.report()
    return output, reasons


# 评分
def judge(name, video_path, webcam=False):
    output, reasons = match(name, video_path, webcam)
    score, reason = (output[0], reasons[0]) if len(output) > 0 else (0, None)
    return score, reason


# 计数
def count(name, video_path, webcam=False, time_limit=None):
    output, reasons = match(name, video_path, webcam, time_limit)
    return len(output)



def classify_and_judge(video_path, webcam=False):
    video = VideoSource(video_path, webcam=webcam)
    global output, reasons
    output.clear()
    reasons.clear()

    for ori, frame_idx in video:
        cv2.imshow('frame', ori)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # if frame_idx == 248:
        #     cv2.imwrite('./2.png', ori)

        pose_dic, angle_map = detector.pre_one_and_angle(ori)
        if pose_dic is None:
            continue
        frame = Frame(frame_idx, pose_dic, angle_map)
        for name in data:
            action: ActionRecognizer = data[name]
            action.match(frame)
    print(output)
    print(reasons)
    for name in data:
        action = data[name]
        action.clear()

if __name__ == '__main__':
    video_path = r'E:\graduate\项目\智慧体育\2021-06-22 141419-计数.mov'
    classify_and_judge(video_path)
    print(output)
    # img_path = r'.\data\210919\2021-06-22 163051\front\248.png'
    # # img_path = './2.jpg'
    # img = cv2.imread(img_path)
    # print(img)
    # pose_dic, angle_map = detector.pre_one_and_angle(img)
    # print(pose_dic)