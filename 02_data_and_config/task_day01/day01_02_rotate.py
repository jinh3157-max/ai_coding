from pathlib import Path
import shutil
from datetime import datetime, timedelta
import time

backup_dir_path = Path(__file__).resolve().parent / "backup"
if backup_dir_path.exists():
    raise FileExistsError("Backup already exist")
backup_dir_path.mkdir()
print("开始模拟备份；按 Ctrl+C 停止并清理")

try:
    while True:
        backup_file_list = []
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"back_{time_str}.txt"
        file_path = backup_dir_path / filename
        file_path.touch()
        print(f"[+] 创建备份: {file_path.name}")
        
        for back_file_path in backup_dir_path.glob("*.txt"):
            file_time = datetime.fromtimestamp(back_file_path.stat().st_mtime)#文件最后一次修改时间
            expire_time = file_time + timedelta(seconds=15)
            if datetime.now() > expire_time:
                back_file_path.unlink()
                print(f"[-] 删除过期备份: {file_path.name}")
        
        
        print("保留列表: ", end = "")
        for backup_file_path in sorted(backup_dir_path.glob("*.txt")):
            backup_file_list.append(backup_file_path.name)
        print(backup_file_list)
        time.sleep(3)
       
except KeyboardInterrupt:
    pass

finally:
    if backup_dir_path.exists():
        shutil.rmtree(backup_dir_path)
        print("backup/ 目录已清理")