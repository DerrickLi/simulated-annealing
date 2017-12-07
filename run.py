import sys
import os, subprocess

def main(argv):
	if len(argv) != 1:
		print("invalid arg length")
		return
	rootdir = argv[0]
	for f in os.listdir(rootdir):
		if f.endswith(".in"):
			filepath = os.path.join(rootdir, f)
			outpath = os.path.join(rootdir, os.path.splitext(f)[0] + ".out")
			subprocess.call(["python", "solver.py", filepath, outpath])

if __name__=="__main__":
	main(sys.argv[1:])