# 依赖zip p7zip-full
import hashlib
import os
import random
import subprocess

class ZipAndRenameFilesToCBZ:
    def __init__(self, directory):
        self.directory = directory

    def zip_folder(self, folder):
        # 生成zip压缩包的名称
        zip_name = folder + ".zip"
        if os.path.exists(zip_name):
            # 如果已经存在同名的zip文件，则在名称后加上随机数
            rand = random.randint(1, 1000)
            zip_name = folder + "_" + str(rand) + ".zip"
        # 执行zip命令压缩文件夹
        cmd = ["zip", "-jr1", zip_name, folder]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print("压缩成功！[%s]" % zip_name)
            # 删除原文件夹
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
        # 重命名指定扩展名的文件
        for file in os.listdir("."):
            if file.endswith(old_ext):
                old_name = os.path.splitext(file)[0]
                new_name = old_name + "." + new_ext
                cmd = ["mv", file, new_name]
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    print("压缩包重命名失败！[%s]" % file)

    def generate_random(self):
        # 生成4位随机字符串
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
    directory = "这里是工作路径"
    zip_and_rename_files = ZipAndRenameFilesToCBZ(directory)
    zip_and_rename_files.run()
