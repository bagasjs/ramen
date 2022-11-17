# "install.py" is a program that will install Ramen into your device
# Do not move "install.py" anywhere or It won't work
import shutil
import os
import platform

# Dependencies

CURRENT_VERSION = "1.1.0"
TARGET_DIR = f"build/ramen-{CURRENT_VERSION}"

with open("Ramen/settings.py", "w") as settingfile:
	settings = {
		"ROOT" : os.getcwd()
	}
	writer = ""
	for key, value in settings.items():
		writer += f"{key.upper()} = \"{value}\""
	settingfile.write(writer)

if "build" in os.listdir():
	shutil.rmtree("build")

os.mkdir("build")
os.mkdir(TARGET_DIR)


nekovm = {
	"Linux" : f"dependencies/neko_linux64",
	"Windows" : f"dependencies/neko_win64",
	"Darwin" : f"dependencies/neko_osx64"
}

try:
	sys = platform.system()
	nekovm = nekovm[sys]
	shutil.copytree(nekovm, f"{TARGET_DIR}/neko")

	if sys == "Windows":
		shutil.copy("dependencies/ramen.bat", TARGET_DIR)
	else:
		shutil.copy("dependencies/ramen.sh", TARGET_DIR)
except:
	print("Could not found a NekoVM for your Platform")

shutil.copytree("dependencies/nekoramen", f"{TARGET_DIR}/nekoramen")
shutil.copytree("Ramen", f"{TARGET_DIR}/ramen")

# Creating the executables