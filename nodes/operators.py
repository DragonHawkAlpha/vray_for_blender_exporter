#
# V-Ray For Blender
#
# http://vray.cgdo.ru
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import bpy


class VRAY_OT_open_image(bpy.types.Operator):
    bl_idname      = "vray.open_image"
    bl_label       = "Open Image File"
    bl_description = "Open image file"

    def execute(self, context):
        return {'FINISHED'}


class VRAY_OT_add_nodetree_light(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_light"
    bl_label       = "Add Light Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayLight = context.object.data.vray

        return {'FINISHED'}


class VRAY_OT_add_nodetree_scene(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_scene"
    bl_label       = "Add Scene Nodetree"
    bl_description = ""

    def execute(self, context):
        return {'FINISHED'}


class VRAY_OT_add_nodetree_object(bpy.types.Operator):
    bl_idname      = "vray.add_nodetree_object"
    bl_label       = "Add Object Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayObject = context.object.vray

        nt = bpy.data.node_groups.new(context.object.name, type='VRayNodeTreeObject')

        outputNode = nt.nodes.new('VRayNodeObjectOutput')

        blenderOut = nt.nodes.new('VRayNodeBlenderOutput')
        blenderOut.location.x  = outputNode.location.x - 200

        nt.links.new(blenderOut.outputs['Material'], outputNode.inputs['Material'])
        nt.links.new(blenderOut.outputs['Geometry'], outputNode.inputs['Geometry'])

        VRayObject.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_world_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_world_nodetree"
    bl_label       = "Add World Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayWorld = context.world.vray

        nt = bpy.data.node_groups.new("World", type='VRayNodeTreeWorld')

        outputNode = nt.nodes.new('VRayNodeWorldOutput')

        VRayWorld.ntree = nt

        return {'FINISHED'}


class VRAY_OT_add_material_nodetree(bpy.types.Operator):
    bl_idname      = "vray.add_material_nodetree"
    bl_label       = "Use Nodes"
    bl_description = ""

    def execute(self, context):
        VRayMaterial = context.material.vray

        nt = bpy.data.node_groups.new(context.material.name, type='VRayShaderTreeType')

        outputNode = nt.nodes.new('VRayNodeOutputMaterial')

        singleMaterial = nt.nodes.new('VRayNodeMtlSingleBRDF')
        singleMaterial.location.x  = outputNode.location.x - 250
        singleMaterial.location.y += 50

        brdfVRayMtl = nt.nodes.new('VRayNodeBRDFVRayMtl')
        brdfVRayMtl.location.x  = singleMaterial.location.x - 250
        brdfVRayMtl.location.y += 100

        nt.links.new(brdfVRayMtl.outputs['BRDF'], singleMaterial.inputs['BRDF'])

        nt.links.new(singleMaterial.outputs['Material'], outputNode.inputs['Material'])

        VRayMaterial.ntree = nt

        return {'FINISHED'}




########  ########  ######   ####  ######  ######## ########     ###    ######## ####  #######  ##    ##
##     ## ##       ##    ##   ##  ##    ##    ##    ##     ##   ## ##      ##     ##  ##     ## ###   ##
##     ## ##       ##         ##  ##          ##    ##     ##  ##   ##     ##     ##  ##     ## ####  ##
########  ######   ##   ####  ##   ######     ##    ########  ##     ##    ##     ##  ##     ## ## ## ##
##   ##   ##       ##    ##   ##        ##    ##    ##   ##   #########    ##     ##  ##     ## ##  ####
##    ##  ##       ##    ##   ##  ##    ##    ##    ##    ##  ##     ##    ##     ##  ##     ## ##   ###
##     ## ########  ######   ####  ######     ##    ##     ## ##     ##    ##    ####  #######  ##    ##

def GetRegClasses():
    return (
        VRAY_OT_open_image,

        VRAY_OT_add_nodetree_scene,
        VRAY_OT_add_nodetree_light,
        VRAY_OT_add_nodetree_object,
        VRAY_OT_add_material_nodetree,
        VRAY_OT_add_world_nodetree,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)