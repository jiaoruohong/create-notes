import sys
import json
from pathlib import Path
import time


class BlogGenerator:

    codeBlock = "```"
    newline = "\n"

    institution = ""
    id = ""

    codeDir = ""
    noteDir = ""
    blogDir = ""

    blogDescription = ""
    blogTags = ""

    codeFileName = ""
    noteFileName = ""
    blogFileName = ""

    codeTitle = ""
    noteTitle = ""
    blogTitle = ""

    def getCodeTitle(self):
        self.codeTitle = self.id
        self.codeFileName = self.id

    def getNoteTitle(self):
        self.noteTitle = self.id
        self.noteFileName = self.id

    def getBlogTitle(self):
        self.blogTitle = self.institution + ' ' + self.id
        self.blogFileName = time.strftime("%Y-%m-%d-", time.localtime())\
            + self.institution + '-' + self.id

    def checkDirExist(self):
        if(not Path(self.codeDir).is_dir()):
            print(self.codeDir + self.getSpace() + "is not exist"
                  + self.getNewLines())
            return False
        if(not Path(self.noteDir).is_dir()):
            print(self.noteDir + self.getSpace() + "is not exist"
                  + self.getNewLines())
            return False
        if(not Path(self.blogDir).is_dir()):
            print(self.blogDir + self.getSpace() + "is not exist"
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
        self.blogDir = data["blogDir"]

        if(not self.checkDirExist()):
            sys.exit(0)

        self.blogDescription = data["blogDescription"]
        self.blogTags = data["blogTags"]

        return data["institution"], data["id"], data["codeDir"],\
            data["noteDir"], data["blogDir"]

    def getDst(self):
        institution, id, codeDir, noteDir, blogDir = self.getJsonItem()

        self.getCodeTitle()
        self.getNoteTitle()
        self.getBlogTitle()

        codeDstCpp = codeDir + self.codeFileName + ".cpp"
        codeDstJava = codeDir + self.codeFileName + ".java"
        noteDst = noteDir + self.noteFileName + ".md"
        blogDst = blogDir + self.blogFileName + ".md"

        return codeDstCpp, codeDstJava, noteDst, blogDst

    def getContent(self):

        with open("./problem/problem.txt", 'r') as loadFile:
            problem = loadFile.read()
        with open("./example/example.txt", 'r') as loadFile:
            example = loadFile.read()
        with open("./codes/solution.cpp", 'r') as loadFile:
            codeCpp = loadFile.read()
        with open("./codes/solution.java", 'r') as loadFile:
            codeJava = loadFile.read()

        return problem, example, codeCpp, codeJava

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

    def getPaperContent(self, title, problem, example, codeCpp, codeJava):
        content = "# " + title + self.getNewLines(2)

        content += "## " + "Problem" + self.getNewLines(2)
        content += problem + self.getNewLines(2)

        content += "## " + "Example" + self.getNewLines(2)
        content += self.codeBlock + self.getNewLines()
        content += example + self.getNewLines()
        content += self.codeBlock + self.getNewLines(2)

        content += "## " + "Codes" + self.getNewLines(2)
        if(len(codeCpp) > 0):
            content += "> cpp" + self.getNewLines(2)
            content += self.codeBlock + self.getNewLines(1)
            content += codeCpp + self.getNewLines()
            content += self.codeBlock + self.getNewLines()
        if(len(codeJava) > 0):
            content += self.getNewLines()
            content += "> java" + self.getNewLines(2)
            content += self.codeBlock + self.getNewLines(1)
            content += codeJava + self.getNewLines()
            content += self.codeBlock + self.getNewLines()

        return content

    def getNoteContent(self, problem, example, codeCpp, codeJava):
        head = ""
        content = self.getPaperContent(
                        self.noteTitle,
                        problem, example, codeCpp, codeJava
                    )
        foot = ""
        noteContent = head + content + foot
        return noteContent

    def getBlogContent(self, problem, example, codeCpp, codeJava):
        head = ""
        head += "---" + self.getNewLines()
        head += "layout: post" + self.getNewLines()
        head += "title: " + self.blogTitle + self.getNewLines()
        head += "description: >" + self.getNewLines()\
                + self.getSpace(2)\
                + self.blogDescription\
                + self.getNewLines()
        head += "tags: ["\
                + self.blogTags\
                + "]"\
                + self.getNewLines()
        head += "---" + self.getNewLines(2)
        content = self.getPaperContent(
                        self.blogTitle,
                        problem, example, codeCpp, codeJava
                    )
        foot = ""
        blogContent = head + content + foot
        return blogContent


if __name__ == "__main__":

    generator = BlogGenerator()

    codeDstCpp, codeDstJava,\
        noteDst, blogDst = generator.getDst()
    print(codeDstCpp + ' ' + codeDstJava + ' ' + noteDst + ' ' + blogDst)

    problem, example,\
        codeCpp, codeJava = generator.getContent()
    print(problem + example + codeCpp + codeJava)

    with open(codeDstCpp, 'w') as fopt:
        fopt.write(codeCpp)

    with open(codeDstJava, 'w') as fopt:
        fopt.write(codeJava)

    with open(noteDst, 'w') as fopt:
        fopt.write(
            generator.getNoteContent(problem, example, codeCpp, codeJava))

    with open(blogDst, 'w') as fopt:
        fopt.write(
            generator.getBlogContent(problem, example, codeCpp, codeJava))
