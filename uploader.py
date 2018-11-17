from utils import get_all_sub_dirs, get_all_dcms_inside_dir, read_json, print_uploading_status
from multiprocessing import Pool
from pacs import Orthanc
from time import time

def upload_folder(otc, pacs_name, dcms):
    for dcm in dcms:
        print_uploading_status(otc.uploadInstance(dcm), pacs_name, dcm)

def mp_upload_folder():
    pass
    
def mp_uploading(path):
    all_dcms = [get_all_dcms_inside_dir(dir, checking=True) for dir in get_all_sub_dirs(path)]
    pacs_dict = read_json('pacs.json')
    pacs_lis = [Orthanc(k,v) for k, v in pacs_dict.items()]
    N = len(pacs_dict.keys())
    pacs_names = ['pacs'+str(n) for n in range(N)]
    p = Pool(5)
    for i, pacs in enumerate(pacs_lis):
        t = time()
        p.apply_async(upload_folder, zip(len(all_dcms)*[pacs], len(all_dcms)*[pacs_names[i]], all_dcms)) 
        print("Takes {} secs to upload to {}".format((time()-t), pacs_names[i]))

def upload_folder_Orthanc(dcms_list):
    pacs_names, pacs_confs = get_pacs_info()
    for i, pacs in enumerate(pacs_confs):
        # upload_folder_to_Orthanc(Orthanc(*pacs), pacs_names[i], dcms_list)
        
        
        print("Takes {} secs to upload to {}".format((time()-t), pacs_names[i]))



def clear_all_pacs():
    pacs_dict = read_json('pacs.json')
    pacs_lis = [Orthanc(k,v) for k, v in pacs_dict.items()]
    N = len(pacs_dict.keys())
    pacs_names = ['pacs'+str(n) for n in range(N)]
    for i, pacs in enumerate(pacs_lis):
        pacs.delete_all_instances()

def upload_to_pacs(path, anonymize=False):
    all_dcms = [get_all_dcms_inside_dir(dir, checking=True, anonymize=True) for dir in get_all_sub_dirs(path)] if anonymize else \
               [get_all_dcms_inside_dir(dir, checking=True) for dir in get_all_sub_dirs(path)]
    pacs_dict = read_json('pacs.json')
    pacs_lis = [Orthanc(k,v) for k, v in pacs_dict.items()]
    N = len(pacs_dict.keys())
    pacs_names = ['pacs'+str(n) for n in range(N)]
    for i, pacs in enumerate(pacs_lis):
        t = time()
        for dir_dcms in all_dcms:
            upload_folder(pacs, pacs_names[i], dir_dcms) 
        print("Takes {} secs to upload to {}".format((time()-t), pacs_names[i]))

# clear_all_pacs()
# mp_uploading('/Users/Brian/Desktop/untitled folder')
