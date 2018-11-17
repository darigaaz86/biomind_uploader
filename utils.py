import os
import json
import pydicom as dicom


#Read Json
def read_json(file):
    with open(file, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def write_json(dictionary, file):
    with open(file, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile)
        
#Get Sub-Directories
def _get_sub_dirs(path):
    return [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

#Print Upload status
def print_uploading_status(response, pacs_name, dcm):
    try:
        if response['Status'] == "Success":
            print('Upload {0} to {1} Success'.format(dcm, pacs_name))
        elif response['Status'] == "AlreadyStored":
            print('{0} AlreadyStored in {1}'.format(dcm, pacs_name))
        else:
            print('Upload {0} to {1} Fail'.format(dcm, pacs_name))
    except Exception as e:
        print(e)

#Get Sub-folders list
def get_all_sub_dirs(path):
    lis = []
    def get_folder_structure(path):
        res = _get_sub_dirs(path)
        for p in res:
            if p not in lis:
                lis.append(p)
        if len(res) == 0:
            return res
        else :
            return [get_folder_structure(i) for i in res]
    get_folder_structure(path)
    lis.append(path)
    return lis


#Get a dict of all files with certain extention, enable checking to use pydiom check dicom readable
def get_all_dcms_inside_dir(path, checking=False, anonymize=False):
    files = [os.path.join(path, f) for f in os.listdir(path) if not os.path.isdir(os.path.join(path, f))]
    if anonymize:
        files = [f for f in files if f.endswith('_anonymized')]
    if checking:
        print(path, 'enable checking')
        files = [f for f in files if _check_file(f)]
    return files

#Check dicom readable 
def _check_file(path):
    try:
        # dicom.read_file(path)
        ds = dicom.dcmread(path, force=True)
        ds.PatientID
        return True
    except Exception as e:
        print('%s not a dicom file'%path)
    return False

#anonymized all dcm files under dir
def anonymize_dir(dir):
    dcms = [dcm for d in get_all_sub_dirs(dir) for dcm in get_all_dcms_inside_dir(d, checking=True)]
    anonymized_dcms = []
    for dcm in dcms:
        anonymized_dcms.append(anonymize_file(dcm))
    return anonymized_dcms

#read single dcm file and save as anonymized format
def anonymize_file(path):
    dataset = dicom.dcmread(path)
    dataset.remove_private_tags()
    #customized field to be anonymized
    data_elements = ['PatientID',
                     'PatientBirthDate']
    for de in data_elements:
        if de in dataset:
            dataset.data_element(de).value = "anonymous"
    output_file = path + '_anonymized'
    dataset.save_as(output_file)
    return output_file

