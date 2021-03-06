#
# V-Ray For Blender
#
# http://chaosgroup.com
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

import os

import bpy

from vb30.nodes import export as NodesExport

from vb30.lib import BlenderUtils, PathUtils, LibUtils
from vb30.lib import VRayStream

from vb30 import debug

import _vray_for_blender


class VRAY_OT_export_nodetree(bpy.types.Operator):
    bl_idname      = "vray.export_nodetree"
    bl_label       = "Export Nodetree"
    bl_description = ""

    def execute(self, context):
        VRayExporter = context.scene.vray.Exporter

        selectedNodeTree = VRayExporter.ntreeListIndex
        if selectedNodeTree == -1:
            return {'CANCELLED'}

        ntree = bpy.data.node_groups[selectedNodeTree]

        outputNode = NodesExport.GetOutputNode(ntree)
        if not outputNode:
            return {'CANCELLED'}

        exportPath = BlenderUtils.GetFullFilepath(VRayExporter.ntreeExportDirectory)
        exportPath = PathUtils.CreateDirectory(exportPath)

        fileName = "%s.vrscene" % LibUtils.CleanString(ntree.name)

        outputFilepath = os.path.normpath(os.path.join(exportPath, fileName))

        debug.PrintInfo('Exporting "%s" to: "%s"' % (ntree.name, outputFilepath))

        o = VRayStream.VRaySimplePluginExporter(outputFilepath)

        exporter = _vray_for_blender.init(
            engine  = 0,
            context = bpy.context.as_pointer(),
            scene   = bpy.context.scene.as_pointer(),
            data    = bpy.data.as_pointer(),

            mainFile     = o.output,
            objectFile   = o.output,
            envFile      = o.output,
            geometryFile = o.output,
            lightsFile   = o.output,
            materialFile = o.output,
            textureFile  = o.output,

            drSharePath = "",
        )

        for sock in outputNode.inputs:
            conNode = NodesExport.GetConnectedNode(ntree, sock)
            if conNode:
                _vray_for_blender.exportNode(
                    ntree.as_pointer(),
                    conNode.as_pointer(),
                    sock.as_pointer()
                )

        _vray_for_blender.exit(exporter)

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
        VRAY_OT_export_nodetree,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)
