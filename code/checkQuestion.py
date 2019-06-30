import json
import os


class Compile:
    def compile(self, code):
        pass


class CppCompile(Compile):
    def compile(self, code):
        with open("tmp.cpp", "w+") as file:
            file.write(code)
        os.system("g++ tmp.cpp -o exe -std=c++11")
        os.remove("tmp.cpp")
        return "exe"


class JavaCompile(Compile):
    def compile(self, code):
        with open("Main.java", "w+") as file:
            file.write(code)
        os.system("javac Main.java")
        os.remove("Main.java")
        return "Main.class"


class PythonCompile(Compile):
    def compile(self, code):
        with open("tmp.py", "w+") as file:
            file.write(code)
        return "tmp.py"


class CheckAnswer:
    def __init__(self):
        self.compiles = {"cpp": CppCompile(), "java": JavaCompile(), "python": PythonCompile()}

    #testlist是json文件中的Test属性,compiletype为cpp, java, python
    def check(self, code, testlist, compiletype):
        totlenum = len(testlist)
        count = 0
        for test in testlist:
            with open("testcontext.txt", "w+") as file:
                file.write(test['Context'])
            rstfile = self.compiles[compiletype].compile(code)
            checkstatement = ""
            if compiletype == "cpp":
                checkstatement = "./%s < testcontext.txt > rst.txt" % rstfile
            if compiletype == "java":
                checkstatement = "java %s < testcontext.txt > rst.txt" % rstfile.split('.')[0]
            if compiletype == 'python':
                checkstatement = "python3 %s < testcontext.txt > rst.txt" % rstfile
            os.system(checkstatement)
            global result
            with open("rst.txt", "r+") as file:
                result = file.read()
            if result.strip() == test['Answer'].strip():
                count += 1
            os.remove("rst.txt")
            print(rstfile)
            os.remove(rstfile)
        if count == totlenum:
            return True
        return False


if __name__ == '__main__':
    print("这个模块是给代码编译和自动化与测试用例测试的模块。下面会运行它的单元测试")
    pythoncode = '''
if __name__ == '__main__':
    print("hello world")    
'''
    pythoncompile = PythonCompile()
    pythoncompile.compile(pythoncode)

    cppcode = '''
#include <iostream>
using namespace std;

int main(int argc, char** argv){
    int a, b;
    cin>>a>>b;
    cout<<a + b<<endl;
    return 0;
}
    '''
    cppcompile = CppCompile()
    cppcompile.compile(cppcode)

    javacode='''
import java.util.*;

public class Main{
    public static void main(String[] argc){
        Scanner scaner = new Scanner(System.in);
        int a=scaner.nextInt(), b=scaner.nextInt();
        System.out.println(a + b);
    }
}    
'''
    javacompile = JavaCompile()
    javacompile.compile(javacode)

    file = open("./static/questions/numplusnum.json")
    context = json.load(file)
    file.close()
    check = CheckAnswer()
    if check.check(javacode, context['Test'], "java"):
        print(True)
    else:
        print(False)