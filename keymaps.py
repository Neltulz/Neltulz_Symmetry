import bpy

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def ntzSym_regKMs(addon_keymaps):

    wm = bpy.context.window_manager

    #------------------------------ 3D View Generic ----------------------------------------------------------------------------
    
    '''
    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="3D View Generic", space_type="VIEW_3D")
    
    kmi = km.keymap_items.new("ntz_sym.performsym", type = "F", ctrl=False, shift=False, alt=False, value = "PRESS")

    #add list of keymaps
    addon_keymaps.append(km)
    '''

def ntzSym_unregKMs(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()