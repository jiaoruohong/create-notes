import sys
import json
from pathlib import Path


class NoteGenerator:

    newline = "\n"

    institution = ""
    id = ""
    weblink = ""

    codeDir = ""
    noteDir = ""

    codeFileName = ""
    noteFileNameDes = ""
    noteFileNameSol = ""

    def getCodeFileName(self):
        self.codeFileName = self.id

    def getNoteFileName(self):
        self.noteFileNameDes =\
            self.institution.capitalize() + "-" + self.id + "-" + "des"
        self.noteFileNameSol =\
            self.institution.capitalize() + "-" + self.id + "-" + "sol"

    def checkDirExist(self):
        if(not Path(self.codeDir).is_dir()):
            print(self.codeDir + self.getSpace() + "is not exist"
                  + self.getNewLines())
            return False
        if(not Path(self.noteDir).is_dir()):
            print(self.noteDir + self.getSpace() + "is not exist"
                  + self.getNewLines())
            return False

        return True

    def getJsonItem(self):

        with open("./assets/info.json", 'r') as loadFile:
            data = json.load(loadFile)

        self.institution = data["institution"]
        self.id = data["id"]

        self.codeDir = data["codeDir"]
        self.noteDir = data["noteDir"]
        self.weblink = data["weblink"]

        if(not self.checkDirExist()):
            sys.exit(0)

        return data["institution"], data["id"], data["codeDir"],\
            data["noteDir"]

    def getDst(self):
        institution, id, codeDir, noteDir = self.getJsonItem()

        self.getCodeFileName()
        self.getNoteFileName()

        codeDstCpp = codeDir + self.codeFileName + ".cpp"
        codeDstJava = codeDir + self.codeFileName + ".java"
        noteDstDes = noteDir + self.noteFileNameDes + ".tex"
        noteDstSol = noteDir + self.noteFileNameSol + ".tex"

        return codeDstCpp, codeDstJava, noteDstDes, noteDstSol

    def getContent(self):

        with open("./problem/problem.tex", 'r') as loadFile:
            problem = loadFile.read()
        with open("./example/example.tex", 'r') as loadFile:
            example = loadFile.read()
        with open("./codes/Solution.tex", 'r') as loadFile:
            solutionMd = loadFile.read()
        with open("./codes/Solution.cpp", 'r') as loadFile:
            codeCpp = loadFile.read()
        with open("./codes/Solution.java", 'r') as loadFile:
            codeJava = loadFile.read()

        return problem, example, solutionMd, codeCpp, codeJava

    def getNewLines(self, n=1):
        ans = ""
        for idx in range(n):
            ans += "\n"

        return ans

    def getSpace(self, n=1):
        ans = ""
        for idx in range(n):
            ans += " "

        return ans

    def getListing(self, file_t, path2file):
        ans = ""
        ans += "\\lstinputlisting[language=" + file_t + "]{"
        ans += path2file + "}"

        return ans

    def getLabel(self, problemlist=True):
        ans = ""
        if(problemlist):
            ans += "\\label{app:problemslist"
            ans += ":" + self.institution + ":" + self.id
            ans += "}"
        else:
            ans += "\\label{app:codeslist"
            ans += ":" + self.institution + ":" + self.id
            ans += "}"

        return ans

    def genLatex(self, prefix, content):
        return "\\" + prefix + "{" + content + "}"

    def getNoteDesContent(self, problem, example, solution):
        content = ""

        content += self.genLatex("subsection", self.genLatex("href", self.weblink+"}{"+self.institution.capitalize()+self.getSpace()+self.id))

        content += self.genLatex("label", "app:problemlist:"+self.institution+":"+self.id)
        content += self.getNewLines(2)

        content += "Problem Description:\\par" + self.getNewLines(2)
        content += problem
        content += self.getNewLines(2)

        content += "Sample:\\par" + self.getNewLines(2)
        content += example
        content += self.getNewLines(2)

        content += "Solution (Codes at~"
        content += self.genLatex("ref", "app:codelist:"+self.institution+":"+self.id)
        content += "):"
        content += "\\par" + self.getNewLines(2)
        content += solution
        content += self.getNewLines(2)

        return content

    def getNoteSolContent(self, codeCpp, codeJava):
        content = ""
        content += self.genLatex("subsection", self.genLatex("href", self.weblink+"}{"+self.institution.capitalize()+self.getSpace()+self.id))

        content += self.genLatex("label", "app:codelist:"+self.institution+":"+self.id)
        content += self.getNewLines()

        if(len(codeCpp) > 0):
            content += self.getNewLines()
            content += "Cpp:\\par" + self.getNewLines()

            content += "\\lstinputlisting[language=Cpp]"
            content += "{" + "path2codeCpp" + "}"
            content += self.getNewLines()

        if(len(codeJava) > 0):
            content += self.getNewLines()
            content += "Java:\\par" + self.getNewLines()

            content += "\\lstinputlisting[language=Java]"
            content += "{" + "path2codeJava}" + ""
            content += self.getNewLines()

        content += self.getNewLines()

        return content


if __name__ == "__main__":

    generator = NoteGenerator()

    codeDstCpp, codeDstJava,\
        noteDstDes, noteDstSol = generator.getDst()
    # print(codeDstCpp + ' ' + codeDstJava + ' ' + noteDst)

    problem, example, solutionMd,\
        codeCpp, codeJava = generator.getContent()
    # print(problem + example + solutionMd + codeCpp + codeJava)

    with open(codeDstCpp, 'w') as fopt:
        fopt.write(codeCpp)

    with open(codeDstJava, 'w') as fopt:
        fopt.write(codeJava)

    with open(noteDstDes, 'w') as fopt:
        fopt.write(
            generator.getNoteDesContent(problem, example, solutionMd))
    with open(noteDstSol, 'w') as fopt:
        fopt.write(
            generator.getNoteSolContent(codeCpp, codeJava))
