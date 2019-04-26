#!/usr/bin/python

import sys, getopt, os

ALL_OS = ["windows", "solaris", "plan9", "openbsd", "netbsd", "linux", "freebsd", "dragonfly", "darwin", "android"]
ALL_OS_ARCH = {
	"windows": ["386", "amd64"], 
	"linux": ["386", "amd64", "arm", "arm64", "ppc64", "ppc64le", "mips" , "mipsle", "mips64", "mips64le"], 
	"android": ["arm"],
	"dragonfly": ["amd64"],
	"darwin": ["386", "amd64", "arm", "arm64"],
	"freebsd": ["386", "amd64", "arm"],
	"netbsd": ["386", "amd64", "arm"],
	"openbsd": ["386", "amd64", "arm"],
	"plan9": ["386", "amd64"],
	"solaris": ["amd64"]
}

def render(text, lbBegin, lbEnd, ret=False):
	lineBreakBegin = ""
	lineBreakEnd = ""
	if lbBegin:
		lineBreakBegin = "\n"
	if lbEnd:
		lineBreakEnd = "\n"
	print(lineBreakBegin + text + lineBreakEnd)
	return ret

def create_builds_array(builds):
	builds_dict = {}
	if builds:
		builds_array = builds.split(":")
		for build in builds_array:
			os_arch = build.split("/")

			if os_arch[1] == "*":
				builds_dict[os_arch[0]] = ["*"]

			if os_arch[0] in builds_dict:
				if builds_dict[os_arch[0]][0] != "*":
					builds_dict[os_arch[0]].append(os_arch[1])
			else:
				builds_dict[os_arch[0]] = [os_arch[1]]

	return builds_dict

def final_output_dest(output, os_type, arch):
	return_value = output + ("final_build", "")[(output and output[-1:] != '/')] + "_" + os_type + "_" + arch
	if os_type == "windows":
		return_value = return_value + ".exe"
	return return_value

def run_command(cmd_dest, os_type, arch, executable, cmd_output):
	os.environ["GOOS"] = os_type
	os.environ["GOARCH"] = arch
	os.system(cmd_dest + " && "+executable+" build -o " + cmd_output)

def builder(dest, builds, gopath, output, goroot, executable):
	cmd_dest = "cd " + dest
	if gopath:
		os.environ["GOPATH"] = gopath
	if goroot:
		os.environ["GOROOT"] = goroot
	if not executable:
		executable = "go"

	builds_array = create_builds_array(builds)

	for os_type, archs in builds_array.items():
		for arch in archs:
			if arch == "*":
				for os_arch in ALL_OS_ARCH[os_type]:
					cmd_output = final_output_dest(output, os_type, os_arch)
					run_command(cmd_dest, os_type, os_arch, executable, cmd_output)
			else:
				cmd_output = final_output_dest(output, os_type, arch)
				run_command(cmd_dest, os_type, arch, executable, cmd_output)

	render("Builds generated successfully", True, True)

def validate(dest, builds, gopath, goroot, executable):
	exit = False
	if dest:
		if not os.path.exists(dest):
			exit = render("Path of package: `"+dest+"` doesn't exist", True, False, True)
	else:
		exit = render("Path of package you want to build is empty", True, False, True)

	builds = create_builds_array(builds)
	if builds:
		for os_type, archs in builds.items():
			if not os_type in ALL_OS:
				exit = render("OS `"+os_type+"` not exist", True, False, True)

			for arch in archs:
				if os_type in ALL_OS_ARCH and not arch in ALL_OS_ARCH[os_type] and arch != "*":
					exit = render("Architecture `"+arch+"` for OS `"+os_type+"` not exist", True, False, True)
	else:
		exit = render("There are no builds exist", True, False, True)

	if gopath:
		gopath_array = gopath.split(":")
		for gp in gopath_array:
			if not os.path.exists(gp):
				exit = render("GO Path: `" + gp + "` doesn't exist", True, False, True)

	if goroot:
		if not os.path.exists(goroot):
			exit = render("GO Root: `" + goroot + "` doesn't exist", True, False, True)

	if executable:
		if not os.path.exists(executable):
			exit = render("GO Executable: `" + executable + "` doesn't exist", True, False, True)

	if exit:
		render("", False, False)
		sys.exit()


def usage():
	filename = os.path.basename(__file__)
	render("Usage: python " + filename + " [options]", True, True)
	render("options: [All options having (*) are required]", False, False)
	render("  -d, --dest(*)    Valid root path of GO package or program", False, False)
	render("                   you want to build", False, False)
	render("  -b, --builds(*)  Colon-(:) seperated OS and Architecture list", False, False)
	render("                   OS and Architecture in the list will be seperated", False, False)
	render("                   by forward-slash (/)", False, False)
	render("  -o, --output     Path where you need output builds", False, False)
	render("  -p, --gopath     Valid `GOPATH` path if you want to set it in", False, False)
	render("                   script explicitly", False, False)
	render("  -r, --goroot     Valid `GOROOT` path if you want to set it in", False, False)
	render("                   script explicitly", False, False)
	render("  -x, --exec       Valid `EXECUTABLE` path if you want to set it in", False, False)
	render("                   script explicitly. Default is `go` and will be used", False, False)
	render("                   like this is build command: `go build xxx`", False, True)

def main(argv):
	filename = os.path.basename(__file__)
	dest = ""
	builds = ""
	output = ""
	gopath = ""
	goroot = ""
	executable = ""
	try :
		opts, args = getopt.getopt(argv,"hd:b:o:p:r:x:",["help", "dest=", "builds=", "output=", "gopath=", "goroot=", "exec"])
	except getopt.GetoptError :
		render("Invalid flag found. Check help command: " + filename + " --help", True, True)
		sys.exit(2)
	for opt, arg in opts :
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-d", "--dest"):
			dest = arg
		elif opt in ("-b", "--builds"):
			builds = arg
		elif opt in ("-o", "--output"):
			output = arg
		elif opt in ("-p", "--gopath"):
			gopath = arg
		elif opt in ("-r", "--goroot"):
			goroot = arg
		elif opt in ("-x", "--exec"):
			executable = arg

	validate(dest, builds, gopath, goroot, executable)
	builder(dest, builds, gopath, output, goroot, executable)

if __name__ == "__main__":
   main(sys.argv[1:])