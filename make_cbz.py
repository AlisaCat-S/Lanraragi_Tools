import hashlib
import os
import random
import subprocess


class ZipAndRenameFilesToCBZ:
    def __init__(self, directory):
        self.directory = directory

        cmd = ["dpkg", "-s", "zip"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        if result.returncode != 0:
            print("依赖:zip未安装，正在安装...")
            os.system("sudo apt-get install -y zip")
        else:
            print("依赖:zip已安装！")

        cmd = ["dpkg", "-s", "p7zip-full"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        if result.returncode != 0:
            print("依赖:p7zip-full未安装，正在安装...")
            os.system("sudo apt-get install -y p7zip-full")
        else:
            print("依赖:p7zip-full已安装！")

    def zip_folder(self, folder):
        zip_name = folder + ".zip"
        if os.path.exists(zip_name):
            rand = random.randint(1, 1000)
            zip_name = folder + "_" + str(rand) + ".zip"
        cmd = ["zip", "-jr1", zip_name, folder]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print("压缩成功！[%s]" % zip_name)
            cmd = ['rm', '-rf', folder]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                print("执行删除文件夹命令时出错：{}".format(err))
            else:
                print("删除文件夹命令执行成功")
        else:
            print("压缩失败！[%s]" % zip_name)

    def rename_files(self, old_ext, new_ext):
        for file in os.listdir("."):
            if file.endswith(old_ext):
                old_name = os.path.splitext(file)[0]
                new_name = old_name + "." + new_ext
                cmd = ["mv", file, new_name]
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    print("压缩包重命名失败！[%s]" % file)

    def generate_random(self):
        rand = hashlib.md5(str(random.randint(1, 1000)).encode('utf-8')).hexdigest()[:4]
        return rand

    def run(self):
        if not os.path.exists(self.directory):
            print("工作目录不存在！")
            return

        os.chdir(self.directory)

        for folder in os.listdir("."):
            if os.path.isdir(folder):
                self.zip_folder(folder)

        self.rename_files("zip", "cbz")
        self.rename_files("rar", "cbr")
        self.rename_files("7z", "cb7")


if __name__ == "__main__":
    directory = "Linux Path"
    zip_and_rename_files = ZipAndRenameFilesToCBZ(directory)
    zip_and_rename_files.run()
