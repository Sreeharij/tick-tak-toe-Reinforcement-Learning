import subprocess
import sys

try:
	import pygame
except ImportError:
	subprocess.check_call([sys.executable,"-m","pip","install","pygame"])
import pygame
