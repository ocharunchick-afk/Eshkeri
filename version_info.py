# -*- coding: utf-8 -*-
# PyInstaller version info resource for Eshkeri_Setup.exe
# This embeds publisher/company metadata into the EXE so Windows shows it
# in SmartScreen dialogs and file Properties -> Details.

VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(2, 7, 0, 0),
        prodvers=(2, 7, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'smuggi_san'),
                        StringStruct('FileDescription', 'Eshkeri Setup — Installer by smuggi_san'),
                        StringStruct('FileVersion', '2.7.0.0'),
                        StringStruct('InternalName', 'Eshkeri_Setup'),
                        StringStruct('LegalCopyright', '© 2026 smuggi_san. All rights reserved.'),
                        StringStruct('OriginalFilename', 'Eshkeri_Setup.exe'),
                        StringStruct('ProductName', 'Eshkeri Protocol'),
                        StringStruct('ProductVersion', '2.7.0.0'),
                    ],
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [0x0409, 1200])]),
    ],
)
