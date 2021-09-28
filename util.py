from math import *


def compute_angle(b, a, c):
    Vbx = b[0] - a[0]
    Vby = b[1] - a[1]
    Vcx = c[0] - a[0]
    Vcy = c[1] - a[1]
    angle_line = (Vbx * Vcx + Vby * Vcy) / sqrt((Vbx * Vbx + Vby * Vby) * (Vcx * Vcx + Vcy * Vcy) + 1e-10)
    # 节点夹角
    angle = acos(angle_line) * 180.0 / pi
    return round(angle, 3)


def get_all_angle(pose_dic):
    angle_map = {}
    # 左手肘、右手肘
    l_elbow = compute_angle(pose_dic['6'], pose_dic['8'], pose_dic['10'])
    r_elbow = compute_angle(pose_dic['5'], pose_dic['7'], pose_dic['9'])
    angle_map['l_elbow'] = l_elbow
    angle_map['r_elbow'] = r_elbow
    # 左腋窝、右腋窝
    l_armpit = compute_angle(pose_dic['8'], pose_dic['6'], pose_dic['12'])
    r_armpit = compute_angle(pose_dic['7'], pose_dic['5'], pose_dic['11'])
    angle_map['l_armpit'] = l_armpit
    angle_map['r_armpit'] = r_armpit

    # 两腿张开
    two_leg = compute_angle(pose_dic['14'], pose_dic['19'], pose_dic['13'])
    angle_map['two_leg'] = two_leg

    # 左腿上抬、右腿上抬
    l_leg = compute_angle(pose_dic['6'], pose_dic['12'], pose_dic['14'])
    r_leg = compute_angle(pose_dic['5'], pose_dic['11'], pose_dic['13'])
    angle_map['l_leg'] = l_leg
    angle_map['r_leg'] = r_leg
    # 左膝盖、右膝盖
    l_knee = compute_angle(pose_dic['12'], pose_dic['14'], pose_dic['16'])
    r_knee = compute_angle(pose_dic['11'], pose_dic['13'], pose_dic['15'])
    angle_map['l_knee'] = l_elbow
    angle_map['r_knee'] = r_elbow
    # 头部左倾、右倾、低头角度
    l_head = compute_angle(pose_dic['6'], pose_dic['18'], pose_dic['17'])
    r_head = compute_angle(pose_dic['5'], pose_dic['18'], pose_dic['17'])
    bow_head = compute_angle(pose_dic['17'], pose_dic['18'], pose_dic['19'])
    angle_map['l_head'] = l_head
    angle_map['r_head'] = r_head
    angle_map['bow_head'] = bow_head

    # 左右手腕
    l_wrist = compute_angle(pose_dic['7'], pose_dic['9'], pose_dic['124'])
    r_wrist = compute_angle(pose_dic['8'], pose_dic['10'], pose_dic['103'])
    angle_map['l_wrist'] = l_wrist
    angle_map['r_wrist'] = r_wrist

    # 左右脚踝
    l_foot = compute_angle(pose_dic['14'], pose_dic['16'], pose_dic['23'])
    r_foot = compute_angle(pose_dic['13'], pose_dic['15'], pose_dic['22'])
    angle_map['l_foot'] = l_foot
    angle_map['r_foot'] = r_foot
    # 是否握拳
    l_hand = compute_angle(pose_dic['115'], pose_dic['124'], pose_dic['127'])
    r_hand = compute_angle(pose_dic['94'], pose_dic['103'], pose_dic['106'])
    angle_map['l_hand'] = l_hand
    angle_map['r_hand'] = r_hand
    return angle_map

def get_towards(bone_points):
    pass
