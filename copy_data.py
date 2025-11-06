import os
import argparse
from tqdm import tqdm
import shutil
from pathlib import Path

video_file_list = [
    # "avm_front",
    # "avm_left",
    # "avm_rear",
    # "avm_right",
    "bev_libflow"
]

pb_file_list = [
    "park_state_manager",
    "vehicle_signal_lowfreq",
    "vehicle_signal_highfreq",
    "sys_mode_resp",
    "Odometry",
    "parking_perception_gridmap",
    "parking_perception_slot",
    "parking_fusion_gridmap",
    "parking_fusion_slot",
    "ultrasonic_obstacle",
    "parking_fusion_object",
    "rcfusion",
    # "parking_fusion_roadmarks"
]

def get_parser():
    parser = argparse.ArgumentParser(description='拷贝CVE数据文件')
    parser.add_argument('source_path',help="源数据路径")
    parser.add_argument('--save_path', '-s', default="/home/mini/下载/codeproblem",help="数据保存路径")
    # parser.add_argument('--create_subdirs', '-c', action='store_true', 
    #                    help="是否创建子目录结构 (d4q.1, L2, test_data)")
    return parser

def copy_cve_files(source_path, save_path, create_subdirs=True):
    """
    从源路径拷贝CVE文件到目标路径
    
    Args:
        source_path: 源数据路径
        save_path: 目标保存路径
        create_subdirs: 是否创建子目录结构
    """
    # 创建目标目录
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"创建目标目录: {save_path}")
    
    # 创建子目录结构
    # if create_subdirs:
    d4q_dir = os.path.join(save_path, "d4q.1")
    l2_dir = os.path.join(save_path, "L2")
    test_data_dir = os.path.join(save_path, "test_data")
        
    for dir_path in [d4q_dir, l2_dir, test_data_dir]:
        if not os.path.exists(dir_path):
          os.makedirs(dir_path)
          print(f"创建目录: {dir_path}")
    
    # 拷贝video数据
    print("开始拷贝video数据...")
    for file in tqdm(video_file_list, desc="拷贝video数据"):
        bin_file = file + ".bin"
        index_file = "d4q.1." + file + ".index.json"
        data_file = "d4q.1." + file + ".data.json"
        
        try:
            # 拷贝.bin文件
            bin_src = os.path.join(source_path, "d4q.1", bin_file)
            bin_dst = os.path.join(save_path, "d4q.1", bin_file) if create_subdirs else os.path.join(save_path, bin_file)
            if os.path.exists(bin_src):
                shutil.copy2(bin_src, bin_dst)
            
            # 拷贝index文件
            index_src = os.path.join(source_path, "L2", index_file)
            index_dst = os.path.join(save_path, "L2", index_file) if create_subdirs else os.path.join(save_path, index_file)
            if os.path.exists(index_src):
                shutil.copy2(index_src, index_dst)
            
            # 拷贝data文件
            data_src = os.path.join(source_path, "L2", data_file)
            data_dst = os.path.join(save_path, "L2", data_file) if create_subdirs else os.path.join(save_path, data_file)
            if os.path.exists(data_src):
                shutil.copy2(data_src, data_dst)
                
        except Exception as e:
            print(f"拷贝 {file} 时发生异常: {e}")
    
    # 拷贝pb数据
    print("开始拷贝pb数据...")
    for file in tqdm(pb_file_list, desc="拷贝pb数据"):
        bin_file = file + ".bin"
        index_file = "d4q.1.ddsflow." + file + ".index.json"
        data_file = "d4q.1.ddsflow." + file + ".data.json"
        
        try:
            # 拷贝.bin文件
            bin_src = os.path.join(source_path, "d4q.1", bin_file)
            bin_dst = os.path.join(save_path, "d4q.1", bin_file) if create_subdirs else os.path.join(save_path, bin_file)
            if os.path.exists(bin_src):
                shutil.copy2(bin_src, bin_dst)
            
            # 拷贝index文件
            index_src = os.path.join(source_path, "L2", index_file)
            index_dst = os.path.join(save_path, "L2", index_file) if create_subdirs else os.path.join(save_path, index_file)
            if os.path.exists(index_src):
                shutil.copy2(index_src, index_dst)
            
            # 拷贝data文件
            data_src = os.path.join(source_path, "L2", data_file)
            data_dst = os.path.join(save_path, "L2", data_file) if create_subdirs else os.path.join(save_path, data_file)
            if os.path.exists(data_src):
                shutil.copy2(data_src, data_dst)
                
        except Exception as e:
            print(f"拷贝 {file} 时发生异常: {e}")
    
    # 拷贝calibs目录
    print("开始拷贝calibs数据...")
    try:
        calibs_src = os.path.join(source_path, "test_data", "calibs")
        calibs_dst = os.path.join(save_path, "test_data", "calibs") if create_subdirs else os.path.join(save_path, "calibs")
        
        if os.path.exists(calibs_src):
            if os.path.exists(calibs_dst):
                shutil.rmtree(calibs_dst)
            shutil.copytree(calibs_src, calibs_dst)
            print("calibs数据拷贝完成")
        else:
            print(f"警告: calibs源目录不存在: {calibs_src}")
    except Exception as e:
        print(f"拷贝calibs时发生异常: {e}")

def main():
    args = get_parser().parse_args()
    
    # 检查源路径是否存在
    if not os.path.exists(args.source_path):
        print(f"错误: 源路径不存在: {args.source_path}")
        return
    last_part = Path(args.source_path).name
    dst_path_full = os.path.join(args.save_path, last_part)
    if os.path.exists(dst_path_full):
        print(f"错误: 目标路径已存在: {dst_path_full}")
        return
    print(f"从 {args.source_path} 拷贝数据到 {dst_path_full}...")
    copy_cve_files(args.source_path, dst_path_full, create_subdirs=True)
    print("数据拷贝完成")

if __name__ == '__main__':
    main()