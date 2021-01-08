import sys
import json


class NoteGenerator:

    newline = "\n"

    institution = ""
    id = ""
    weblink = ""

    path2problem = "",
    problemDir = "",

    path2sampleipt = "",
    sampleIptDir = "",

    path2sampleopt = "",
    sampleOptDir = "",

    path2solution = "",
    solutionDir = "",

    path2cpp = "",
    path2java = "",
    codesDir = ""

    def getBasicInfo(self):

        with open("./assets/info.json", 'r') as loadFile:
            data = json.load(loadFile)

        self.institution = data["institution"]
        self.id = data["id"]
        self.weblink = data["weblink"]

        self.path2problem = data["path2problem"]
        self.problemDir = data["problemDir"]

        self.path2sampleipt = data["path2sampleipt"]
        self.sampleIptDir = data["sampleIptDir"]

        self.path2sampleopt = data["path2sampleopt"]
        
        self.sampleOptDir = data["sampleOptDir"]

        self.path2solution = data["path2solution"]
        self.solutionDir = data["solutionDir"]

        self.path2cpp = data["path2cpp"]
        self.path2java = data["path2java"]
        self.codesDir = data["codesDir"]

    def getFile(self, path2file):
        with open(path2file, 'r') as loadFile:
            content = loadFile.read()

        return content

    def cinFile(self, path2file, data):
        with open(path2file, 'w') as fopt:
            fopt.write(data)

    def copy2dir(self):
        problem = self.getFile(self.path2problem)
        sampleIpt = self.getFile(self.path2sampleipt)
        sampleOpt = self.getFile(self.path2sampleopt)
        solution = self.getFile(self.path2solution)
        codeCpp = self.getFile(self.path2cpp)
        codeJava = self.getFile(self.path2java)

        self.cinFile(self.problemDir + self.id + ".tex", problem)
        self.cinFile(self.sampleIptDir + self.id + ".tex", sampleIpt)
        self.cinFile(self.sampleOptDir + self.id + ".tex", sampleOpt)
        self.cinFile(self.solutionDir + self.id + ".tex", solution)
        self.cinFile(self.codesDir + self.id + ".cpp", codeCpp)
        self.cinFile(self.codesDir + self.id + ".java", codeJava)


if __name__ == "__main__":

    handler = NoteGenerator()

    handler.getBasicInfo()
    handler.copy2dir()

