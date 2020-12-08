import os,os.path,subprocess
from subprocess import STDOUT,PIPE

def compile_java(java_file):
    cwd = os.getcwd()
    subprocess.check_call(['javac','-cp','"' + java_file.rsplit('/', 1)[0] + '/:' +cwd +'/utils/junit-4.13.1.jar:' +cwd +'/utils/hamcrest-2.2.jar"', java_file.rsplit('/', 1)[0] + '/Challenge.java', java_file])

def execute_java(java_file):
    java_class,ext = os.path.splitext(java_file)
    cwd = os.getcwd()
    cmd = ['java','-cp','"'+cwd +'/utils/junit-4.13.1.jar:' +cwd +'/utils/hamcrest-2.2.jar:'+ java_file.rsplit('/', 1)[0]+'/"','org.junit.runner.JUnitCore',java_class.split('/')[-1]]
    proc = subprocess.Popen(' '.join(cmd),shell=True,stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    return stdout
    