import os

class SupaDupaResult:
    def __init__(self, header):
        self.header = header
        self.files = []

    def addFile(self, fileName, fileBody):
        self.files.append((fileName, fileBody))

    def writeFiles(self, outputDir):
        for fileName, fileBody in self.files:
            outfile = file(os.path.join(outputDir, fileName), 'w')
            outfile.write(self.header + '\n')
            outfile.write(fileBody + '\n')
            outfile.close()

    def writeToStdOut(self):
        print self.header
        for name, body in self.files:
            print body + '\n'
