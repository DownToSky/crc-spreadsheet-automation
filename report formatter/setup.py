from cx_Freeze import setup, Executable



base = None


executables = [Executable("formatter.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':["os", "sys", "tkinter", "openpyxl", "csv"],
    },

}

setup(
    name = "formatter.exe",
    options = options,
    version = "0.1",
    description = 'formats REDCap reports downloaded in CSV extension',
    executables = executables
)