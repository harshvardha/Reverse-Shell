import cx_Freeze as cx
import platform
import os

if platform.system()=="Windows":
    PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))

target_name = None
base = None
if platform.system()=="Windows":
    base = "Win32GUI"
    target_name = 'Doc Manager.exe'

shortcut_data = [
    ('DesktopShortcut','DesktopFolder','Doc Manager','TARGETDIR',
        '[TARGETDIR]'+target_name,None,'Data Entry application for hospitals/clinics',None,None,None,None,'TARGETDIR'
        ),(
            'MenuShortcut','ProgramMenuFolder','Doc Manager','TARGETDIR','[TARGETDIR]'+target_name,None,
            'Data Entry application for hospitals/clinics',None,None,None,None,'TARGETDIR'
        )
]

cx.setup(name = "Doc Manager",
         version = "1.0",
         author = "Harshvardhan Singh",
         author_email = "harshvardhansingh458@gmail.com",
         description = "Patient Data Entry Application medical clinic",
         options = {'build_exe':{'packages':["os","socket","subprocess"]},
                    'bdist_msi':{
                        'upgrade_code':'{83A4FBB5-5727-4195-ADA6-2765FB571421}','data':{'Shortcut':shortcut_data}
                    }},
         executables = [cx.Executable("client.py",base = base,targetName=target_name)])
