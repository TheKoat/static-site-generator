import os
import shutil


def copy_from_static_to_public(dest, src):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    os.mkdir(dest)

    items = os.listdir(src)

    for item in items:
        from_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest)
        else:   
            copy_from_static_to_public(dest_path, from_path)