"""Hook per PyInstaller - assicura che tkinter venga incluso correttamente."""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all tkinter data files
datas = collect_data_files('tkinter')
datas += collect_data_files('customtkinter')
datas += collect_data_files('tkinterdnd2')

# Collect all submodules
hiddenimports = collect_submodules('tkinter')
hiddenimports += collect_submodules('customtkinter')
hiddenimports += ['tkinterdnd2.TkinterDnD']
