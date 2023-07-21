import os


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
            

    