import os
import json

from cudatext import *
#from cudax_lib import get_translation

#_   = get_translation(__file__)  # I18N

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_tab_rename.json')
PREFIX_KEY = 'renamed_tab_prefix'

prefix = ':'
namemap = {}

class Command:
    
  def __init__(self):
    self.load_config()
      
    menu_proc('tab', MENU_ADD, command='cuda_tab_rename.rename_current', caption='Rename tab')
      
  def config(self):
    if not os.path.exists(fn_config):
      namemap[PREFIX_KEY] = prefix
      with open(fn_config, 'w', encoding='utf-8') as f:
        json.dump(namemap, f, indent=2)
    file_open(fn_config)
      
        
  def rename_current(self):
    path = ed.get_filename()
    if path:
      start_name = ed.get_prop(PROP_TAB_TITLE)
      newname = dlg_input('New tab name for file:\n  '+path, start_name)
      if newname  and newname != start_name:
        ed.set_prop(PROP_TAB_TITLE, prefix + newname)
        namemap[path] = newname
        self.save_cfg()

  def clear_current(self):
    path = ed.get_filename()
    if path  and path in namemap:
      del namemap[path]
      ed.set_prop(PROP_TAB_TITLE, os.path.basename(path))
      self.save_cfg()
        
        
  def on_open(self, ed_self):
    path = ed_self.get_filename()
    newname = namemap.get(path)
    if newname != None:
      ed_self.set_prop(PROP_TAB_TITLE, prefix + newname)
        
  def on_save(self, ed_self):
    if ed_self.get_filename() == fn_config:
      oldmap = {**namemap}
      self.load_config()
 
      # apply new config
      for h in ed_handles():
        e = Editor(h)
        path = e.get_filename()
          
        if path in namemap: # apply new config
          e.set_prop(PROP_TAB_TITLE, prefix + namemap[path])
        elif path in oldmap: # reset name if removed from config
          e.set_prop(PROP_TAB_TITLE, os.path.basename(path))
            
 
  def save_cfg(self):
    namemap[PREFIX_KEY] = prefix
    with open(fn_config, 'w', encoding='utf-8') as f:
      json.dump(namemap, f, indent=2)

  def load_config(self):
    global prefix
      
    if os.path.exists(fn_config):
      with open(fn_config, 'r', encoding='utf-8') as f:
        j = json.load(f)

      prefix = j.get(PREFIX_KEY, prefix)

      namemap.clear()
      namemap.update(j)
