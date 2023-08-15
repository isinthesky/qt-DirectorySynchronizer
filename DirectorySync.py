
import os
import shutil


class DirectorySync:
    def __init__(self, srcPath, dstPath):
        self.srcPath = srcPath
        self.dstPath = dstPath

    def syncDirectories(self):
        src_dir = self.srcPath
        dst_dir = self.dstPath

        for dirpath, dirnames, filenames in os.walk(src_dir):
            for dirname in dirnames:
                src_sub_dir = os.path.join(dirpath, dirname)
                dst_sub_dir = src_sub_dir.replace(src_dir, dst_dir, 1)
                if not os.path.exists(dst_sub_dir):
                    os.makedirs(dst_sub_dir)

            for filename in filenames:
                src_file = os.path.join(dirpath, filename)
                dst_file = src_file.replace(src_dir, dst_dir, 1)
                if not os.path.exists(dst_file) or os.stat(src_file).st_mtime - os.stat(dst_file).st_mtime > 1:
                    shutil.copy2(src_file, dst_file)
