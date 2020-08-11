import json


class BlogGenerator:

    codeBlock = "```"

    def getCodeTitle(self, institution, id):
        codeTitle = id

        return codeTitle

    def getNoteTitle(self, institution, id):
        noteTitle = id

        return noteTitle

    def getBlogTitle(self, institution, id):
        blogTitle = institution + '-' + id

        return blogTitle

    def getJsonItem(self):

        with open("./assets/info.json", 'r') as loadFile:
            data = json.load(loadFile)

        return data["institution"], data["id"], data["codeDir"],\
            data["noteDir"], data["blogDir"]

    def getDst(self):
        institution, id, codeDir, noteDir, blogDir = self.getJsonItem()

        codeTitle = self.getCodeTitle(institution, id)
        noteTitle = self.getNoteTitle(institution, id)
        blogTitle = self.getBlogTitle(institution, id)

        codeDstCpp = codeDir + codeTitle + ".cpp"
        codeDstJava = codeDir + codeTitle + ".java"
        noteDst = noteDir + noteTitle + ".md"
        blogDst = blogDir + blogTitle + ".md"

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


if __name__ == "__main__":

    generator = BlogGenerator()

    codeDstCpp, codeDstJava, noteDst, blogDst = generator.getDst()
    print(codeDstCpp + ' ' + codeDstJava + ' ' + noteDst + ' ' + blogDst)

    problem, example, codeCpp, codeJava = generator.getContent()
    print(problem + example + codeCpp + codeJava)

    print(generator.codeBlock)
    print(generator.codeBlock)

    with open(codeDstCpp, 'w') as fopt:
        fopt.write(codeCpp)

    with open(codeDstJava, 'w') as fopt:
        fopt.write(codeJava)

    with open(noteDst, 'w') as fopt:
        fopt.write(problem)
        fopt.write(example)
        if(len(codeCpp) > 0):
            fopt.write('\n' + generator.codeBlock + "cpp" + '\n')
            fopt.write(codeCpp)
            fopt.write(generator.codeBlock)
        if(len(codeJava) > 0):
            fopt.write('\n' + generator.codeBlock + "java" + '\n')
            fopt.write(codeJava)
            fopt.write(generator.codeBlock)

    with open(blogDst, 'w') as fopt:
        fopt.write(problem)
        fopt.write(example)
        if(len(codeCpp) > 0):
            fopt.write('\n' + generator.codeBlock + "cpp" + '\n')
            fopt.write(codeCpp)
            fopt.write(generator.codeBlock)
        if(len(codeJava) > 0):
            fopt.write('\n' + generator.codeBlock + "java" + '\n')
            fopt.write(codeJava)
            fopt.write(generator.codeBlock)
