import subprocess
from pathlib import Path

cwd = Path.home()
libmutter_version = ""
libmutter_name = ""

def main():
    # create a temporary directory
    Path(Path.home() / "mutter").mkdir(parents=True, exist_ok=True)

    # grab latest source code
    cwd = Path(Path.home() / "mutter")
    subprocess.run("apt source mutter", shell=True, cwd=cwd)
    subprocess.run("sudo apt build-dep mutter", shell=True, cwd=cwd)

    # we need to grab a file from within the mutter source code now
    # we assume that mutter will start with `mutter-` and be the only file
    # that does in this directory. This could very easily breat.
    raw_output = subprocess.check_output("ls | grep mutter-", shell=True, cwd=cwd)
    output = raw_output.decode("utf-8").strip()

    # sets the version of libmutter we will be working with
    libmutter_version = output.split("-")[1]

    cwd = Path(Path.home() / "mutter" / output)

    # now we need to grab the source file
    lines = []
    offending_line = 0
    with open(cwd / "src/backends/x11/meta-backend-x11.c", "r+") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "case XkbNewKeyboardNotify:" in line:
            offending_line = i
            break

    # now we need to replace the offending line with the following
    lines[offending_line] = ""
    with open(cwd / "src/backends/x11/meta-backend-x11.c", "w+") as f:
        f.writelines(lines)

    # we will now build from source
    # we skip tests because they seem to fail (can't grab a wayland communication bus from the 
    # subprocess.run command)
    subprocess.run("DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -rfakeroot -uc -b", shell=True, cwd=cwd)

    # we have to figure out which file is the release .deb file now
    # we are assuming it'll be the only .deb without debug or dbg in its name
    cwd = Path(Path.home() / "mutter")
    raw_output = subprocess.check_output(f"ls | grep _{libmutter_version}-", shell=True, cwd=cwd)
    output = raw_output.decode("utf-8").split("\n")

    deb = ""
    for file in output:
        if file.endswith(".deb") and file.startswith("libmutter-") and ("dbg" not in file):
            # sets the package name we will use later
            libmutter_name = file.split("_")[0]

            deb = file
            break
    
    # now we will install the .deb file
    subprocess.run(f"sudo dpkg -i {deb}", shell=True, cwd=cwd)

    # finally we will block it from being updated by the package manager
    subprocess.run(f"sudo apt-mark hold {libmutter_name}", shell=True, cwd=cwd)

    # remove our temporary directory
    cwd = Path.home()
    subprocess.run(f"rm -rf mutter", shell=True, cwd=cwd)

if __name__ == "__main__":
    main()
