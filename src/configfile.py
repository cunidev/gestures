from subprocess import call, Popen
from os.path import expanduser
from shutil import copyfile
from gesture import Gesture
import re

class ConfigFileHandler:
	def __init__(self):
     		self.openFile()

       	def openFile(self):
        	self.validSupportedRegex = re.compile("^\s*(#D:\s)?gesture\s((swipe)\s(up|down|left|right)|(pinch\s(in|out|clockwise|anticlockwise)))\s([2-4]\s)?(.+)")
     		self.validUnsupportedRegex = re.compile("^\s*device\s")

		self.filePath = expanduser("~") + "/.config/libinput-gestures.conf"
        	self.backupPath = expanduser("~") + "/.config/libinput-gestures.conf.bak"

     		try:
           		try:

				self.file = open(self.filePath, "r+")
    			except IOError:
           			self.file = open(self.filePath, 'w+')
  		except:
        		raise Exception("err_file_open");

        	self.rawLines = list(self.file)

		for n in range(len(self.rawLines)):
  			if(self.rawLines[n][-1:] == '\n'):
                  		self.rawLines[n] = self.rawLines[n][:-1]

         	self.fileLines = ["# Generated by Gestures 0.1", "# Manual editing might result in data loss!"]
         	self.validUnsupportedLines = ["# Unsupported lines"]
         	self.invalidLines = ["# Invalid lines"]
		self.gestures = []

         	for line in self.rawLines:
              		validLine = self.validSupportedRegex.match(line)
         		if(validLine):
				line = line.split(' ')
    				filter(None, line)

        			enabled = True
        			if(line[0] == "#D:"):
               				enabled = False
               				line.pop(0)

              			type = line[1]
              			direction = line[2]

           			if(unicode(line[3], 'utf-8').isnumeric()):
              				fingers = line[3]
              				command = ' '.join(line[4:])

              			else:
                     			fingers = 0
                     			command = ' '.join(line[3:])


           			curGesture = Gesture(type, direction, command, fingers, enabled)
              			self.gestures.append(curGesture)
           		elif(self.validUnsupportedRegex.match(line)):
                  		self.validUnsupportedLines.append(line)
                	elif((line[:1] == "#") and not ("#I: " in line)) or (line == ""):
                     		pass
                	else:
                     		if ("#I: " in line):
	                     		self.invalidLines.append(line)
                        	else:
                             		self.invalidLines.append("#I: "+line)
        def reloadFile(self):
            	self.file.close()
             	self.openFile()
        def reloadProcess(self):
            	try:
                 	print "Restarting process (in background)..."
	        	Popen(["libinput-gestures-setup", "restart"], shell=False)
          		print "Process restarted!"
             	except Exception as e:
                  	raise Exception("err_exec")
        def save(self):
        	self.fileLines.append('\n')
         	self.fileLines.extend(self.invalidLines)
          	self.fileLines.append('\n')
          	self.fileLines.extend(self.validUnsupportedLines)
           	self.fileLines.append('\n#Gestures')

           	for curGesture in self.gestures:
                	self.fileLines.append(curGesture.make())
		self.file.seek(0)
           	self.file.write('\n'.join(self.fileLines))
            	self.file.truncate()
             	self.reloadFile()

  	def backup(self):
       		try:
             		copyfile(self.filePath, self.backupPath)
               		return True
        	except:
             		return False
	def restore(self):
     		try:
             		copyfile(self.backupPath, self.filePath)
               		return True
        	except:
             		return False
	def isValid(self):
     		return "# Generated by Gestures " in self.rawLines[0];