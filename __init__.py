bl_info = {
    "name" : "Neltulz - Symmetry",
    "author" : "Neil V. Moore",
    "description" : 'Slice, cut, or mirror a mesh object easily',
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic",
    "tracker_url": "mailto:neilvmoore@gmail.com",
    "wiki_url": "https://www.logichaos.com/neltulz_blender_addons/neltulz_symmetry/README_Neltulz_Symmetry"
}

# -----------------------------------------------------------------------------
#   Import Classes and/or functions     
# -----------------------------------------------------------------------------  

import bpy

from . properties           import NTZSYM_ignitproperties
from . main_ot              import NTZSYM_OT_ntzperformsym
from . misc_ot              import NTZSYM_OT_NtzResetAllSettings
from . addon_preferences    import NTZSYM_OT_ntzsymprefs
from . panels               import NTZSYM_PT_options
from . panels               import NTZSYM_PT_ntzsym

from . import keymaps

PendingDeprecationWarning

# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    NTZSYM_ignitproperties,
    NTZSYM_OT_ntzperformsym,
    NTZSYM_OT_ntzsymprefs,
    NTZSYM_PT_options,
    NTZSYM_PT_ntzsym,
    NTZSYM_OT_NtzResetAllSettings,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # update panel name
    addon_preferences.update_panel(None, bpy.context)

    #add keymaps from keymaps.py
    keymaps.ntzSym_regKMs(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.ntzSym = bpy.props.PointerProperty(type=NTZSYM_ignitproperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.ntzSym_unregKMs(addon_keymaps)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.ntz_sym.performsym()