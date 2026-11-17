from pathlib import Path
import shutil

files = {
    'R1_config.txt': 'hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R2_config.txt': 'hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R3_config.txt': 'hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'SW1_config.txt': 'hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
}

backup_dir = Path(__file__).resolve().parent / "backup"

if backup_dir.exists():
     raise FileExistsError("backup directory already exists") 

backup_dir.mkdir()

try:
    for filename, config in files.items():
        file_path = backup_dir / filename
        file_path.write_text(config, encoding= "utf-8")
    
    print("发现包含 shutdown 接口的设备配置文件:")

    for backup_file_path in sorted(backup_dir.glob("*.txt")):
        config = backup_file_path.read_text(encoding = "utf-8")
        for line in config.splitlines():
            if line.strip() == "shutdown":
                print(backup_file_path.name)
                break
finally:
    shutil.rmtree(backup_dir)
    print("backup/ 目录已清理")
        
        


