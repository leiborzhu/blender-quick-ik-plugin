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
path = r'D:\\light-project\\blenderIK\\ik_script'

if path not in sys.path:
    sys.path.append(path)
try:
    from bvh_process import bvh_smip_write
except:
    from . import bvh_process
    from bvh_process import *

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


# 导入bvh        
def load_bvh(self, context, uiProperty):
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
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    for obj in bpy.data.objects:
        if 'refer' not in obj.name:
            ob_name = obj.name
    
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
    bpy.ops.object.mode_set(mode='OBJECT') #切换为OBJECT更改模式

    ob = bpy.data.objects[refer_name]
    bpy.context.view_layer.objects.active = ob
    
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    bpy.ops.pose.select_all(action='DESELECT')

    bpy.data.objects[refer_name].data.bones.active = targetbone
    bpy.ops.view3d.snap_cursor_to_selected()
    
    
    # 再选回原骨骼
    targetbone = bpy.data.objects[ob_name].data.bones['Bone_handle_' + targetname]
    bpy.ops.object.mode_set(mode='OBJECT') #切换为OBJECT更改模式
    
    ob = bpy.data.objects[ob_name]
    bpy.context.view_layer.objects.active = ob
    
    bpy.ops.object.mode_set(mode='POSE') #切换为pose更改模式
    bpy.ops.pose.select_all(action='DESELECT')
    
    bpy.data.objects[ob_name].data.bones.active = targetbone
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
    
    # k
    bpy.context.area.ui_type = 'TIMELINE'
    bpy.ops.action.keyframe_insert(type='SEL')
    bpy.context.area.ui_type = 'VIEW_3D'

    
# 每隔若干帧对齐动作
def auto_aline(self, context, uiProperty):
    pass


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
    bl_label='添加'
    bl_idname = 'obj.ikmove' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        uiProperty = context.scene.uiProperty
        move_handle_refer(self, context, uiProperty)
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
        col.operator("obj.ikaddlh", text="添加左手ik控制骨骼",icon="BONE_DATA")
        col.operator("obj.ikaddrh", text="添加右手ik控制骨骼",icon="BONE_DATA")
        col.operator("obj.ikmove", text="对齐参考动作",icon="TRACKING_REFINE_FORWARDS")
        
        col.label(text="关键帧工具", icon="TIME")
        
        col.label(text="bvh导出", icon="ARMATURE_DATA")
        col = layout.column()
        
        col.prop(scene, 'output_path', text="输出路径")
        col.prop(scene, 'bvh_simp', text="bvh自动精简")

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
    

classGroup = [uiProperty,
            bvhOutput,
            bvhSmooth,
            PT_view3d_IK,
            bvhInput,
            ikHandleLH,
            ikHandleRH,
            ikReferMove
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
