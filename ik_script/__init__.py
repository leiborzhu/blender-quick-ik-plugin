bl_info = {
    "name": "bvh ik_Tool",
    "author": "leibor",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Tools > bvh输出",
    "description": "bvh关键帧顺滑",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
import os
import sys
import json
path = r'D:\\light-project\\blenderIK\\ik_script'

def bvh_smip_write(input_path, output_path):

    # 将带IK的骨骼进行后处理
    with open(input_path) as f:
        key = 0
        lines = f.readlines()

    # 骨骼文本分类
    skel_line = []
    motion_line = []
    divide_key = 0

    for i, line in enumerate(lines):
        if divide_key == 0:
            if 'MOTION' in line:
                divide_key = 1
                motion_line.append(line)
            else:
                skel_line.append(line)
        else:
            motion_line.append(line)
    print(skel_line[0])
    print(skel_line[1])
    if  'HIERARCHY' in skel_line[0] and 'ROOT pelvis' in skel_line[1]:
        skel_line_new = skel_line
        motion_line_new = motion_line
        # 将动作原样输出
    else:
        
        pelvis_label = 0
        HIERARCHY_label = 0
        bone_labels = []
        extra_motion_num = 0 # 末尾去除的通道数量

        for i, line in enumerate(skel_line):
            if 'HIERARCHY' in line:
                HIERARCHY_label = i
            elif 'JOINT pelvis' in line:
                pelvis_label = i
            elif 'Bone' in line:
                bone_labels.append(i)
                if 'CHANNELS' in skel_line[i + 3]:
                    extra_motion_num += int(skel_line[i + 3].split(' ')[1])
        print('extra_motion_num: ' + str(extra_motion_num))

        gap_line = []
        for j in range(HIERARCHY_label + 1, pelvis_label):
            gap_line.append(j)
            
        for label in bone_labels:
            for j in range(label, label + 9):
                gap_line.append(j)
                
        gap_line.append(len(skel_line) - 1)

        skel_line_new = []

        for i, line in enumerate(skel_line):
            if i in gap_line:
                continue
            if 'JOINT pelvis' in line:
                
                line = line.replace('JOINT pelvis', 'ROOT pelvis')

            if line.startswith('\t'):
                skel_line_new.append(line[1:]) # 去除一个'\t'
            else:
                skel_line_new.append(line)
            # print(lines)
            
            
        # motion 简化
        motion_line_new = []
        for i, line in enumerate(motion_line):    
            if len(line.split(' ')) > 10:
                motion_line_data = line.strip('\n').split(' ')
                while motion_line_data[-1] == '':
                    motion_line_data.pop()
                motion_line_data = motion_line_data[:len(motion_line_data) - extra_motion_num]
                new_line = ' '.join(motion_line_data) + '\n'
                motion_line_new.append(new_line)
            else:
                motion_line_new.append(line)
            
        
    with open(output_path, 'w') as f:
        f.writelines(skel_line_new + motion_line_new)

# 导出驱动ue的json
def bvh2json(input_path, output_path):
    hierarchy = {
                "joint_name": "pelvis",
                "offset": [
                    0.000181,
                    87.757401,
                    0.32101
                ],
                "channel_names": [
                    "Xposition",
                    "Yposition",
                    "Zposition",
                    "Zrotation",
                    "Xrotation",
                    "Yrotation"
                ],
                "children": [
                    {
                        "joint_name": "spine_01",
                        "offset": [
                            2.3033,
                            0.0,
                            0.0
                        ],
                        "channel_names": [
                            "Zrotation",
                            "Xrotation",
                            "Yrotation"
                        ],
                        "children": [
                            {
                                "joint_name": "spine_02",
                                "offset": [
                                    4.87826,
                                    0.0,
                                    0.0
                                ],
                                "channel_names": [
                                    "Zrotation",
                                    "Xrotation",
                                    "Yrotation"
                                ],
                                "children": [
                                    {
                                        "joint_name": "spine_03",
                                        "offset": [
                                            7.15211,
                                            0.0,
                                            0.0
                                        ],
                                        "channel_names": [
                                            "Zrotation",
                                            "Xrotation",
                                            "Yrotation"
                                        ],
                                        "children": [
                                            {
                                                "joint_name": "spine_04",
                                                "offset": [
                                                    7.13269,
                                                    0.0,
                                                    0.0
                                                ],
                                                "channel_names": [
                                                    "Zrotation",
                                                    "Xrotation",
                                                    "Yrotation"
                                                ],
                                                "children": [
                                                    {
                                                        "joint_name": "spine_05",
                                                        "offset": [
                                                            14.868401,
                                                            0.0,
                                                            0.0
                                                        ],
                                                        "channel_names": [
                                                            "Zrotation",
                                                            "Xrotation",
                                                            "Yrotation"
                                                        ],
                                                        "children": [
                                                            {
                                                                "joint_name": "neck_01",
                                                                "offset": [
                                                                    9.91843,
                                                                    2.3e-05,
                                                                    0.0
                                                                ],
                                                                "channel_names": [
                                                                    "Zrotation",
                                                                    "Xrotation",
                                                                    "Yrotation"
                                                                ],
                                                                "children": [
                                                                    {
                                                                        "joint_name": "neck_02",
                                                                        "offset": [
                                                                            5.377701,
                                                                            -2.3e-05,
                                                                            0.0
                                                                        ],
                                                                        "channel_names": [
                                                                            "Zrotation",
                                                                            "Xrotation",
                                                                            "Yrotation"
                                                                        ],
                                                                        "children": [
                                                                            {
                                                                                "joint_name": "head",
                                                                                "offset": [
                                                                                    4.900848,
                                                                                    0.0,
                                                                                    0.0
                                                                                ],
                                                                                "channel_names": [
                                                                                    "Zrotation",
                                                                                    "Xrotation",
                                                                                    "Yrotation"
                                                                                ],
                                                                                "children": [
                                                                                    {
                                                                                        "joint_name": "End Site",
                                                                                        "offset": [
                                                                                            0.0,
                                                                                            0.0,
                                                                                            0.0
                                                                                        ]
                                                                                    }
                                                                                ]
                                                                            }
                                                                        ]
                                                                    }
                                                                ]
                                                            },
                                                            {
                                                                "joint_name": "clavicle_l",
                                                                "offset": [
                                                                    3.878208,
                                                                    0.87455,
                                                                    -0.776979
                                                                ],
                                                                "channel_names": [
                                                                    "Zrotation",
                                                                    "Xrotation",
                                                                    "Yrotation"
                                                                ],
                                                                "children": [
                                                                    {
                                                                        "joint_name": "upperarm_l",
                                                                        "offset": [
                                                                            12.244202,
                                                                            0.0,
                                                                            0.0
                                                                        ],
                                                                        "channel_names": [
                                                                            "Zrotation",
                                                                            "Xrotation",
                                                                            "Yrotation"
                                                                        ],
                                                                        "children": [
                                                                            {
                                                                                "joint_name": "lowerarm_l",
                                                                                "offset": [
                                                                                    24.766403,
                                                                                    4.6e-05,
                                                                                    -6.1e-05
                                                                                ],
                                                                                "channel_names": [
                                                                                    "Zrotation",
                                                                                    "Xrotation",
                                                                                    "Yrotation"
                                                                                ],
                                                                                "children": [
                                                                                    {
                                                                                        "joint_name": "hand_l",
                                                                                        "offset": [
                                                                                            23.068901,
                                                                                            0.0,
                                                                                            0.0
                                                                                        ],
                                                                                        "channel_names": [
                                                                                            "Zrotation",
                                                                                            "Xrotation",
                                                                                            "Yrotation"
                                                                                        ],
                                                                                        "children": [
                                                                                            {
                                                                                                "joint_name": "thumb_01_l",
                                                                                                "offset": [
                                                                                                    2.143562,
                                                                                                    1.340202,
                                                                                                    -2.17669
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "thumb_02_l",
                                                                                                        "offset": [
                                                                                                            4.083206,
                                                                                                            0.0,
                                                                                                            0.0
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "thumb_03_l",
                                                                                                                "offset": [
                                                                                                                    2.399323,
                                                                                                                    0.0,
                                                                                                                    0.0
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "End Site",
                                                                                                                        "offset": [
                                                                                                                            0.0,
                                                                                                                            0.0,
                                                                                                                            0.0
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "ring_metacarpal_l",
                                                                                                "offset": [
                                                                                                    2.753036,
                                                                                                    0.089897,
                                                                                                    0.704202
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "ring_01_l",
                                                                                                        "offset": [
                                                                                                            4.416107,
                                                                                                            0.0,
                                                                                                            0.0
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "ring_02_l",
                                                                                                                "offset": [
                                                                                                                    3.746841,
                                                                                                                    0.0,
                                                                                                                    0.0
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "ring_03_l",
                                                                                                                        "offset": [
                                                                                                                            2.857948,
                                                                                                                            0.0,
                                                                                                                            0.0
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "pinky_metacarpal_l",
                                                                                                "offset": [
                                                                                                    2.638687,
                                                                                                    0.209846,
                                                                                                    1.69411
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "pinky_01_l",
                                                                                                        "offset": [
                                                                                                            4.166641,
                                                                                                            0.0,
                                                                                                            0.0
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "pinky_02_l",
                                                                                                                "offset": [
                                                                                                                    2.559578,
                                                                                                                    0.0,
                                                                                                                    0.0
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "pinky_03_l",
                                                                                                                        "offset": [
                                                                                                                            1.538979,
                                                                                                                            0.0,
                                                                                                                            0.0
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "middle_metacarpal_l",
                                                                                                "offset": [
                                                                                                    2.774834,
                                                                                                    0.002121,
                                                                                                    -0.307822
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "middle_01_l",
                                                                                                        "offset": [
                                                                                                            4.925629,
                                                                                                            0.0,
                                                                                                            0.0
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "middle_02_l",
                                                                                                                "offset": [
                                                                                                                    4.338493,
                                                                                                                    0.0,
                                                                                                                    0.0
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "middle_03_l",
                                                                                                                        "offset": [
                                                                                                                            2.564789,
                                                                                                                            0.0,
                                                                                                                            0.0
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "index_metacarpal_l",
                                                                                                "offset": [
                                                                                                    3.100029,
                                                                                                    0.173431,
                                                                                                    -1.76641
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "index_01_l",
                                                                                                        "offset": [
                                                                                                            4.774261,
                                                                                                            0.0,
                                                                                                            0.0
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "index_02_l",
                                                                                                                "offset": [
                                                                                                                    4.005173,
                                                                                                                    0.0,
                                                                                                                    0.0
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "index_03_l",
                                                                                                                        "offset": [
                                                                                                                            1.970001,
                                                                                                                            0.0,
                                                                                                                            0.0
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            }
                                                                                        ]
                                                                                    }
                                                                                ]
                                                                            }
                                                                        ]
                                                                    }
                                                                ]
                                                            },
                                                            {
                                                                "joint_name": "clavicle_r",
                                                                "offset": [
                                                                    3.87788,
                                                                    0.874458,
                                                                    0.777135
                                                                ],
                                                                "channel_names": [
                                                                    "Zrotation",
                                                                    "Xrotation",
                                                                    "Yrotation"
                                                                ],
                                                                "children": [
                                                                    {
                                                                        "joint_name": "upperarm_r",
                                                                        "offset": [
                                                                            -12.2442,
                                                                            0.0,
                                                                            -0.000645
                                                                        ],
                                                                        "channel_names": [
                                                                            "Zrotation",
                                                                            "Xrotation",
                                                                            "Yrotation"
                                                                        ],
                                                                        "children": [
                                                                            {
                                                                                "joint_name": "lowerarm_r",
                                                                                "offset": [
                                                                                    -24.7666,
                                                                                    6.9e-05,
                                                                                    0.0
                                                                                ],
                                                                                "channel_names": [
                                                                                    "Zrotation",
                                                                                    "Xrotation",
                                                                                    "Yrotation"
                                                                                ],
                                                                                "children": [
                                                                                    {
                                                                                        "joint_name": "hand_r",
                                                                                        "offset": [
                                                                                            -23.0688,
                                                                                            0.0,
                                                                                            -1.1e-05
                                                                                        ],
                                                                                        "channel_names": [
                                                                                            "Zrotation",
                                                                                            "Xrotation",
                                                                                            "Yrotation"
                                                                                        ],
                                                                                        "children": [
                                                                                            {
                                                                                                "joint_name": "ring_metacarpal_r",
                                                                                                "offset": [
                                                                                                    -2.753149,
                                                                                                    -0.090225,
                                                                                                    -0.704308
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "ring_01_r",
                                                                                                        "offset": [
                                                                                                            -4.41614,
                                                                                                            0.0,
                                                                                                            4.9e-05
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "ring_02_r",
                                                                                                                "offset": [
                                                                                                                    -3.74684,
                                                                                                                    -3.1e-05,
                                                                                                                    -6.1e-05
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "ring_03_r",
                                                                                                                        "offset": [
                                                                                                                            -2.857922,
                                                                                                                            -7.6e-05,
                                                                                                                            1.8e-05
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "pinky_metacarpal_r",
                                                                                                "offset": [
                                                                                                    -2.638849,
                                                                                                    -0.210251,
                                                                                                    -1.69415
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "pinky_01_r",
                                                                                                        "offset": [
                                                                                                            -4.16667,
                                                                                                            5.3e-05,
                                                                                                            -2e-05
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "pinky_02_r",
                                                                                                                "offset": [
                                                                                                                    -2.55953,
                                                                                                                    -1.5e-05,
                                                                                                                    2.6e-05
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "pinky_03_r",
                                                                                                                        "offset": [
                                                                                                                            -1.538931,
                                                                                                                            3.1e-05,
                                                                                                                            -3.3e-05
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "middle_metacarpal_r",
                                                                                                "offset": [
                                                                                                    -2.77491,
                                                                                                    -0.002449,
                                                                                                    0.307706
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "middle_01_r",
                                                                                                        "offset": [
                                                                                                            -4.92564,
                                                                                                            -3.1e-05,
                                                                                                            8.7e-05
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "middle_02_r",
                                                                                                                "offset": [
                                                                                                                    -4.338499,
                                                                                                                    5.3e-05,
                                                                                                                    -6.8e-05
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "middle_03_r",
                                                                                                                        "offset": [
                                                                                                                            -2.564861,
                                                                                                                            0.0,
                                                                                                                            2.1e-05
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "thumb_01_r",
                                                                                                "offset": [
                                                                                                    -2.143721,
                                                                                                    -1.340569,
                                                                                                    2.17656
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "thumb_02_r",
                                                                                                        "offset": [
                                                                                                            -4.083229,
                                                                                                            0.000114,
                                                                                                            -2.1e-05
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "thumb_03_r",
                                                                                                                "offset": [
                                                                                                                    -2.399281,
                                                                                                                    -3.1e-05,
                                                                                                                    2.9e-05
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "End Site",
                                                                                                                        "offset": [
                                                                                                                            0.0,
                                                                                                                            0.0,
                                                                                                                            0.0
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "joint_name": "index_metacarpal_r",
                                                                                                "offset": [
                                                                                                    -3.100189,
                                                                                                    -0.173843,
                                                                                                    1.76635
                                                                                                ],
                                                                                                "channel_names": [
                                                                                                    "Zrotation",
                                                                                                    "Xrotation",
                                                                                                    "Yrotation"
                                                                                                ],
                                                                                                "children": [
                                                                                                    {
                                                                                                        "joint_name": "index_01_r",
                                                                                                        "offset": [
                                                                                                            -4.7743,
                                                                                                            4.6e-05,
                                                                                                            -4.7e-05
                                                                                                        ],
                                                                                                        "channel_names": [
                                                                                                            "Zrotation",
                                                                                                            "Xrotation",
                                                                                                            "Yrotation"
                                                                                                        ],
                                                                                                        "children": [
                                                                                                            {
                                                                                                                "joint_name": "index_02_r",
                                                                                                                "offset": [
                                                                                                                    -4.00515,
                                                                                                                    0.0,
                                                                                                                    0.0
                                                                                                                ],
                                                                                                                "channel_names": [
                                                                                                                    "Zrotation",
                                                                                                                    "Xrotation",
                                                                                                                    "Yrotation"
                                                                                                                ],
                                                                                                                "children": [
                                                                                                                    {
                                                                                                                        "joint_name": "index_03_r",
                                                                                                                        "offset": [
                                                                                                                            -1.969999,
                                                                                                                            -1.5e-05,
                                                                                                                            3.1e-05
                                                                                                                        ],
                                                                                                                        "channel_names": [
                                                                                                                            "Zrotation",
                                                                                                                            "Xrotation",
                                                                                                                            "Yrotation"
                                                                                                                        ],
                                                                                                                        "children": [
                                                                                                                            {
                                                                                                                                "joint_name": "End Site",
                                                                                                                                "offset": [
                                                                                                                                    0.0,
                                                                                                                                    0.0,
                                                                                                                                    0.0
                                                                                                                                ]
                                                                                                                            }
                                                                                                                        ]
                                                                                                                    }
                                                                                                                ]
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            }
                                                                                        ]
                                                                                    }
                                                                                ]
                                                                            }
                                                                        ]
                                                                    }
                                                                ]
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "joint_name": "thigh_r",
                        "offset": [
                            -2.34508,
                            -0.852013,
                            8.00902
                        ],
                        "channel_names": [
                            "Zrotation",
                            "Xrotation",
                            "Yrotation"
                        ],
                        "children": [
                            {
                                "joint_name": "calf_r",
                                "offset": [
                                    41.266998,
                                    -1.5e-05,
                                    0.0
                                ],
                                "channel_names": [
                                    "Zrotation",
                                    "Xrotation",
                                    "Yrotation"
                                ],
                                "children": [
                                    {
                                        "joint_name": "foot_r",
                                        "offset": [
                                            37.067204,
                                            0.0,
                                            0.0
                                        ],
                                        "channel_names": [
                                            "Zrotation",
                                            "Xrotation",
                                            "Yrotation"
                                        ],
                                        "children": [
                                            {
                                                "joint_name": "End Site",
                                                "offset": [
                                                    0.0,
                                                    0.0,
                                                    0.0
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "joint_name": "thigh_l",
                        "offset": [
                            -2.34509,
                            -0.855392,
                            -8.00866
                        ],
                        "channel_names": [
                            "Zrotation",
                            "Xrotation",
                            "Yrotation"
                        ],
                        "children": [
                            {
                                "joint_name": "calf_l",
                                "offset": [
                                    -41.266998,
                                    2.3e-05,
                                    0.0
                                ],
                                "channel_names": [
                                    "Zrotation",
                                    "Xrotation",
                                    "Yrotation"
                                ],
                                "children": [
                                    {
                                        "joint_name": "foot_l",
                                        "offset": [
                                            -37.067299,
                                            0.0,
                                            0.0
                                        ],
                                        "channel_names": [
                                            "Zrotation",
                                            "Xrotation",
                                            "Yrotation"
                                        ],
                                        "children": [
                                            {
                                                "joint_name": "End Site",
                                                "offset": [
                                                    0.0,
                                                    0.0,
                                                    0.0
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
    blendshape_base = [
                    0.030956467613577843,
                    0.030956467613577843,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.026918664574623108,
                    0.0282646045088768,
                    0.0,
                    0.0,
                    0.014805268496274948,
                    0.016151200979948044,
                    0.013459332287311554,
                    0.0,
                    0.0,
                    0.006729666143655777,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0013459335314109921,
                    0.004037800244987011,
                    0.0,
                    0.0,
                    0.0,
                    0.029610536992549896,
                    0.03364833816885948,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0013459335314109921,
                    0.005383734125643969,
                    0.004037800244987011,
                    0.004037800244987011,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.010767468251287937,
                    0.005383734125643969,
                    0.09556126594543457,
                    0.09959907829761505,
                    0.0,
                    0.0,
                    0.004037800244987011,
                    0.004037800244987011,
                    0.016151200979948044,
                    0.016151200979948044,
                    0.0
                ]
    blendshape_names_base = [
                "browDownLeft",
                "browDownRight",
                "browInnerUp",
                "browOuterUpLeft",
                "browOuterUpRight",
                "cheekPuff",
                "cheekSquintLeft",
                "cheekSquintRight",
                "eyeBlinkLeft",
                "eyeBlinkRight",
                "eyeLookDownLeft",
                "eyeLookDownRight",
                "eyeLookInLeft",
                "eyeLookInRight",
                "eyeLookOutLeft",
                "eyeLookOutRight",
                "eyeLookUpLeft",
                "eyeLookUpRight",
                "eyeSquintLeft",
                "eyeSquintRight",
                "eyeWideLeft",
                "eyeWideRight",
                "jawForward",
                "jawLeft",
                "jawOpen",
                "jawRight",
                "mouthClose",
                "mouthDimpleLeft",
                "mouthDimpleRight",
                "mouthFrownLeft",
                "mouthFrownRight",
                "mouthFunnel",
                "mouthLeft",
                "mouthLowerDownLeft",
                "mouthLowerDownRight",
                "mouthPressLeft",
                "mouthPressRight",
                "mouthPucker",
                "mouthRight",
                "mouthRollLower",
                "mouthRollUpper",
                "mouthShrugLower",
                "mouthShrugUpper",
                "mouthSmileLeft",
                "mouthSmileRight",
                "mouthStretchLeft",
                "mouthStretchRight",
                "mouthUpperUpLeft",
                "mouthUpperUpRight",
                "noseSneerLeft",
                "noseSneerRight",
                "tongueOut"
            ]
    
    with open(input_path) as f:

        bvh_line = f.readlines()

    motion = []
    motionKey = 0
    t_poseKey = 1
    for line in bvh_line:
        if 'Frame Time: ' in line:
            fps = 1 / float(line.strip('Frame Time: '))
            motionKey = 1 
            continue

        if motionKey:

            tmp_group = [float(x) for x in line.split(' ')]
            if t_poseKey:
                t_pose = tmp_group
                t_poseKey = 0
            else:
                motion.append(tmp_group)

    num_frame = len(motion)
    open_header = {
        "info": "",
        "standard": "metahuman",
        "fps": fps,
        "total_frames": num_frame,
        "t_pose": t_pose
    }
    open_motion = [
        {
            "header": open_header,
            "hierarchy": hierarchy,
            "motion": motion
        }
    ]

    open_facial_header = {"info": '', "standard": "arkit", "fps": fps, "total_frames": num_frame}
    open_facial_data = {"blendshape_names": blendshape_names_base, 'blendshape_sequence': [blendshape_base for _ in range(num_frame)]}
    open_facial = {"header": open_facial_header, "data": open_facial_data}
    open_header = {"info": ""}
    open_sign_language = {"OpenFacialAction": open_facial,
                          "header": open_header,
                          "OpenMotion": open_motion
                          }
    
    # write json
    with open(output_path, 'w', encoding="utf-8") as f:
        json.dump(open_sign_language, f, ensure_ascii=False, indent=4)

# 导出bvh并后处理
def deal_bvh(self, context, uiProperty):
    
    bpy.context.area.ui_type = 'VIEW_3D'

    for obj in bpy.data.objects:
        if 'refer' not in obj.name:
            target_name = obj.name
            break
    ob = bpy.data.objects[target_name]
    bpy.context.view_layer.objects.active = ob
    
    num_name = uiProperty.file_name.strip().strip('.bvh')
    
    last_frame = int(bpy.data.actions[0].frame_range[1])

    print(locals())
    tmp_name = num_name + '_tmp.bvh'
    tmp_path = os.path.join(uiProperty.output_path.strip(), tmp_name)
    bpy.ops.export_anim.bvh(filepath=tmp_path,
                            check_existing=True,
                            filter_glob='*.bvh',
                            global_scale=1.0,
                            frame_start=1,
                            frame_end=last_frame,
                            rotate_mode='ZXY', 
                            root_transform_only=True)
    simp_name = num_name + '.bvh'
    simp_path = os.path.join(uiProperty.output_path.strip(), simp_name)
    
    if uiProperty.bvh_simp:
        bvh_smip_write(input_path=tmp_path, 
                        output_path=simp_path)
        if uiProperty.json_tran:
            json_path = os.path.join(uiProperty.output_path.strip(), 'cpy.json')
            bvh2json(simp_path, json_path)

# 导入bvh        
def load_bvh(self, context, uiProperty):
    
    # 设置帧数为60
    bpy.context.scene.render.fps = 60
    # 清空所有骨架
    for arm in bpy.data.armatures:
        bpy.data.armatures.remove(arm)
    
    # 清空所有动作
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)
        
    load_path_dis = uiProperty.input_path.strip()
    
    load_path = os.path.join(load_path_dis, uiProperty.file_name.strip().strip('.bvh') + '.bvh')
    bpy.ops.import_anim.bvh(filepath=load_path, rotate_mode='ZXY', axis_forward='Y', axis_up='Z')
    
    # 转向世界正向
    bpy.context.object.rotation_euler[0] = 1.5708
    bpy.context.scene.frame_current = 1
    ob_name = uiProperty.file_name.strip().strip('.bvh')
    ob = bpy.data.objects[ob_name]
    
    # 选定该物体
    bpy.context.view_layer.objects.active = ob
    
    # 复制一个参考
    bpy.ops.view3d.copybuffer()
    bpy.ops.view3d.pastebuffer()
    
    bpy.data.objects[ob_name + '.001'].name = ob_name + 'refer'

    bpy.data.actions[ob_name + '.001'].name = ob_name + 'refer'
    bpy.data.armatures[ob_name + '.001'].name = ob_name + 'refer'
    
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式

    # 调节时间轴
    last_frame = int(bpy.data.actions[0].frame_range[1])
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = last_frame



# 绑定ik手柄
def add_ik_Hand(self, context, baseBone, uiProperty):
    
    ob_name = uiProperty.file_name.strip().strip('.bvh')
    ob = bpy.data.objects[ob_name]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    
    if 'Bone_handle_' + baseBone in bpy.data.objects[ob_name].pose.bones:
        return 
    
    if baseBone in bpy.data.objects[ob_name].pose.bones:
        bone_hand = bpy.data.objects[ob_name].pose.bones[baseBone].bone
        
        bpy.ops.pose.select_all(action='DESELECT')

        bpy.data.objects[ob_name].data.bones.active = bone_hand
        bpy.data.objects[ob_name].data.bones.active = bpy.context.active_bone

        bpy.ops.view3d.snap_cursor_to_active()

        bpy.ops.object.editmode_toggle()
        bpy.ops.armature.bone_primitive_add()
        offset = 10
        # 添加骨骼

        bpy.ops.transform.translate(value=(0, -0, 20), 
                                    orient_axis_ortho='X', 
                                    orient_type='GLOBAL', 
                                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                                    orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), 
                                    mirror=False, snap=False, snap_elements={'INCREMENT'}, 
                                    use_snap_project=False, snap_target='CLOSEST', 
                                    use_snap_self=True, 
                                    use_snap_edit=True, 
                                    use_snap_nonedit=True, 
                                    use_snap_selectable=False)
        # 重命名
        bpy.ops.object.posemode_toggle()
        bone_leftHand_ik = bpy.data.objects[ob_name].pose.bones['Bone'].bone
        bone_leftHand_ik.name = 'Bone_handle_' + baseBone
        
        # 选择父节点
        bone_hand_r = bpy.data.objects[ob_name].pose.bones[baseBone].bone
        bpy.data.objects[ob_name].data.bones.active = bone_hand_r
        
        
        bone_parent = bone_hand_r.parent
        bpy.data.objects[ob_name].data.bones.active = bone_parent
        
        parent_name = bone_parent.name
        bpy.ops.pose.constraint_add(type='IK')
        bpy.context.object.pose.bones[parent_name].constraints["IK"].chain_count = 2
        bpy.context.object.pose.bones[parent_name].constraints["IK"].target = bpy.data.objects[ob_name]
        bpy.context.object.pose.bones[parent_name].constraints["IK"].subtarget = bone_leftHand_ik.name
        
        bpy.ops.pose.select_all(action='DESELECT')
        
        # 激活关键帧
        bpy.context.scene.frame_current = 1
        bpy.data.objects[ob_name].data.bones.active = bone_leftHand_ik
        bone = bpy.data.objects[ob_name].pose.bones[bone_leftHand_ik.name]
        bone.keyframe_insert(data_path="location")
        
        # 添加动画资产
        # bpy.context.area.ui_type = 'TIMELINE'
        # bpy.ops.poselib.create_pose_asset(activate_new_action=True)
        # bpy.context.area.ui_type = 'VIEW_3D'

        
# ik手柄移动至原动作参考处
def move_handle_refer(self, context, uiProperty):

    # 检查所需objects是否完整
    index_name = uiProperty.file_name
    refer_name = index_name + 'refer'
    if index_name not in bpy.data.objects.keys() or refer_name not in bpy.data.objects.keys():
        return

    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    ob_name = index_name
    
    if bpy.data.objects[ob_name].data.bones.active != None:
        ik_bone = bpy.data.objects[ob_name].data.bones.active
    else:
        return
    
    
    bpy.ops.pose.select_all(action='DESELECT')
    refer_name = ob_name + 'refer'
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    print(ik_bone.name)
    
    targetname = ik_bone.name[len('Bone_handle_'):]

    # 确定参考骨骼坐标
    targetbone = bpy.data.objects[refer_name].data.bones[targetname]
    print(targetbone.name)
    bpy.ops.object.mode_set(mode='OBJECT') #切换为OBJECT更改模式

    ob = bpy.data.objects[refer_name]
    bpy.context.view_layer.objects.active = ob

    bpy.ops.object.posemode_toggle() #切换为pose更改模式
    bpy.ops.pose.select_all(action='DESELECT')
    
    bpy.ops.object.select_pattern(pattern=targetbone.name)
    
    bpy.ops.view3d.snap_cursor_to_selected()
    
    
    # 再选回原骨骼
    targetbone = bpy.data.objects[ob_name].data.bones['Bone_handle_' + targetname]
    bpy.ops.object.mode_set(mode='OBJECT') #切换为OBJECT更改模式
    
    ob = bpy.data.objects[ob_name]
    bpy.context.view_layer.objects.active = ob
    
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    bpy.ops.pose.select_all(action='DESELECT')
    
    bpy.ops.object.select_pattern(pattern=targetbone.name)
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
    
    # k帧
    bpy.context.area.ui_type = 'TIMELINE'
    bpy.ops.action.keyframe_insert(type='SEL')
    bpy.context.area.ui_type = 'VIEW_3D'
    
    
# 每隔若干帧对齐动作
def auto_aline(self, context, uiProperty):

    # 检查所需objects是否完整
    index_name = uiProperty.file_name
    refer_name = index_name + 'refer'
    if index_name not in bpy.data.objects.keys() or refer_name not in bpy.data.objects.keys():
        return

    last_frame = int(bpy.data.actions[index_name].frame_range[1])
    frame_note = list(range(1, last_frame, uiProperty.gap_frame))
    frame_note += [1, 2, 3]
    for note in frame_note:
        bpy.context.scene.frame_current = note
        bpy.ops.obj.ikmove()

    bpy.context.scene.frame_current = 1

    



class bvhInput(bpy.types.Operator):
    # import bvh
    bl_label='bvh-ik工具导入'
    bl_idname = 'obj.ikbvhin' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        load_bvh(self, context, uiProperty)
        return {'FINISHED'}

class bvhOutput(bpy.types.Operator):
    # output bvh
    bl_label='bvh-ik工具导出'
    bl_idname = 'obj.ikbvhout' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    mStr: bpy.props.StringProperty(name="mString", default="blender")
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        deal_bvh(self, context, uiProperty)
        return {'FINISHED'}
    
class ikHandleLH(bpy.types.Operator):
    # add left hand ik handle
    bl_label='添加左手ik控制骨骼'
    bl_idname = 'obj.ikaddlh' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        add_ik_Hand(self, context, 'hand_r', uiProperty)
        return {'FINISHED'}

class ikHandleRH(bpy.types.Operator):
    # add hand ik handle
    bl_label='添加右手ik控制骨骼'
    bl_idname = 'obj.ikaddrh' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        add_ik_Hand(self, context, 'hand_l', uiProperty)
        return {'FINISHED'}
    
class ikReferMove(bpy.types.Operator):
    # move hand ik handle
    bl_label='迁移操作杆到参考位置'
    bl_idname = 'obj.ikmove' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        move_handle_refer(self, context, uiProperty)
        return {'FINISHED'}

class ikReferAuto(bpy.types.Operator):
    # auto aline keyframe
    bl_label='批量添加对齐关键帧'
    bl_idname = 'obj.ikauto' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        auto_aline(self, context, uiProperty)
        return {'FINISHED'}
 
    
class PT_view3d_IK(bpy.types.Panel):
    bl_idname = "PT_view3d_IK"
    bl_label = "ik导出bvh"

    # 标签分类
    bl_category = "Tool"

    # ui_type
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_context = ["objectmode", 'posemode']

    def draw(self, context):
        layout = self.layout
        layout.label(text="bvh导入", icon="ARMATURE_DATA")

        col = layout.column()
        scene = context.scene.uiProperty
        
        # 生成按钮
        col.prop(scene, 'file_name', text="文件名称")
        col.prop(scene, 'input_path', text="导入文件路径")
        col.operator("obj.ikbvhin", text="导入",icon="IMPORT")
        row = layout.row()
        
        col.label(text="ik操作", icon="CONSTRAINT_BONE")
        split = layout.split(factor=0.75)
        col = split.column()
        col.operator("obj.ikaddlh", text="添加右手ik控制骨骼",icon="BONE_DATA")
        col.operator("obj.ikaddrh", text="添加左手ik控制骨骼",icon="BONE_DATA")
        col.operator("obj.ikmove", text="对齐参考动作",icon="TRACKING_REFINE_FORWARDS")
        
        col.label(text="关键帧工具", icon="TIME")
        col.prop(scene, 'gap_frame', text="间隔帧数")
        col.operator("obj.ikauto", text="批量生成对齐关键帧",icon="TRACKER")
        col = layout.column()
    
        col.label(text="bvh导出", icon="ARMATURE_DATA")

        col.prop(scene, 'output_path', text="输出路径")
        col.prop(scene, 'bvh_simp', text="bvh自动精简")
        col.prop(scene, 'json_tran', text="json生成")

        # 生成按钮
        col.operator("obj.ikbvhout", text="输出",icon="EXPORT").mStr = '开始'

class bvhSmooth(bpy.types.Header):
    
    bl_space_type = 'INFO'
    
    def draw(self, context):
        self.layout.operator('bl_idname')

# RNA属性
class uiProperty(bpy.types.PropertyGroup):
    
    input_path: bpy.props.StringProperty(name='input_path')
    output_path: bpy.props.StringProperty(name='output_path')
    file_name: bpy.props.StringProperty(name='file_name')
    bvh_simp: bpy.props.BoolProperty(name='bvh_simp')
    gap_frame: bpy.props.IntProperty(name='gap_frame')
    json_tran: bpy.props.BoolProperty(name='json_tran')
    

classGroup = [uiProperty,
            bvhOutput,
            bvhSmooth,
            PT_view3d_IK,
            bvhInput,
            ikHandleLH,
            ikHandleRH,
            ikReferMove,
            ikReferAuto
]

def register():
    for item in classGroup:
        # print(1)
        bpy.utils.register_class(item)
    bpy.types.Scene.uiProperty = bpy.props.PointerProperty(type=uiProperty)
def unregister():
    for item in classGroup:
        bpy.utils.unregister_class(item)


if __name__== '__main__':
    register()
