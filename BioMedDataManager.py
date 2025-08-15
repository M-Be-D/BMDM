# libraries
import os
import json
import hashlib
from datetime import datetime
from tkinter import messagebox
import re

class BioMedDataManager:
    """
    # Medical data management
    * Method 'boot': for create hidden folder named '.bmdm' (start management)
    * Method 'config': to configure and store user or doctor information
    * Method 'admit': to add medical data
    * Method 'stats': to display a collection of data and statical information under management and observation
    * Method 'tag': to add or remove description tags for a specific data item
    * Method 'find': to search between data with a specific filter
    * Method 'hist': to display history or logs
    * Method 'export': to export information
    * Method 'remove': to remove information
    """
    config_file = ".bmdm/config.json"
    history_file = ".bmdm/history.log"
    def __init__(self):
        self.bmdm_dir = ".bmdm"
        self.index_file = ".bmdm/index.json"
        self.objects_dir = ".bmdm/objects"

    def boot(self):
        """
        This method creates hidden folder named '.bmdm'
        """
        
        # Checking the existence of the bmdm folder
        if os.path.isdir(self.bmdm_dir):
            print("The bmdm folder exists.")
            self._log_activity('boot', "BOOT", "The bmdm folder exists.")

            if not os.path.isfile(self.index_file):
                with open(self.index_file, "w") as index:
                    json.dump({}, index)     
            if not os.path.isfile(self.config_file):
                with open(self.config_file, "w") as conf:
                    json.dump({"manager": {"name": "", "email": ""}}, conf)
            if not os.path.isdir(self.objects_dir):
                os.mkdir(self.objects_dir)
            if not os.path.isfile(self.history_file):
                with open(self.history_file, "w") as h_f:
                    h_f.close()
        
        # Create a folder
        else:    
            os.mkdir(self.bmdm_dir)

            # If the operating system is Windows, it hides it using this method
            if os.name == "nt":
                os.system(f"attrib +h {self.bmdm_dir}")
                
            # create object and history folders
            os.makedirs(self.objects_dir)
            with open(self.history_file, "w") as h_f:
                h_f.close()

            # create config and index files
            with open(self.config_file, "w") as conf:
                json.dump({"manager": {"name": "", "email": ""}}, conf)
            with open(self.index_file, "w") as index:
                json.dump({}, index)
                
        self._log_activity('boot', "BOOT", "BMDM initialized")
    
    def config(self, name: str = None, email: str = None):
        """
        to configure and store user or doctor information
        """
        if not os.path.isdir(self.bmdm_dir):

            raise RuntimeError("First you need to load the boot. (python bmdm.py boot)")

        # format email --> user@example.com 
        pattern = re.compile(r'^[^@]+@[^@]+\.com$')
        if not bool(pattern.fullmatch(email)):
            raise RuntimeError("The email must be in the format 'user@example.com'")
        # To add name and email to config file
        with open(self.config_file, 'r') as conf:
            config = json.load(conf)
            if name != None:
                config["manager"]["name"] = name
            if email != None:
                config["manager"]["email"] = email
            with open(self.config_file, "w") as conf:    
                json.dump(config, conf)
        
        self._log_activity('config', "CONFIG_UPDATE", f"Updated config: name={name}, email={email}")
    
    def admit(self, file_path: str):
        """
        To add medical data
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        
        if not os.path.exists(file_path):
            self._log_activity('admit', "PATH_ERROR", "Path does not exist.")
            raise RuntimeError("Path does not exist")
        
        def extract_metadata(file:str):
            """
            To extract metadata(patient_id, study_date, modality, decryption, path)
            """
            # for 'txt" files
            if file.endswith(".txt"):
                file = os.path.basename(file)
                parts = file.replace(".txt", "").split("_")
                if len(parts) < 4:
                    self._log_activity('admit', "TYPE_ERROR", "The input file type is incorrect.")
                    raise NameError("The file name is incorrect. the correct format is 'PATIENTID_STUDYDATE_MODALITY_DESCRIPTION.txt' ")
                else:
                    metadata = {
                        "filename": file,
                        "patient_id": parts[0],
                        "study_date": parts[1],
                        "modality": parts[2],
                        "description": parts[3:],
                        "path": file_path,
                        "tags": {}
                    }
                    hash = hashlib.blake2s(file.encode('utf-8')).hexdigest()
                    return metadata, hash
            # for 'json' files
            elif file.endswith(".json"):
                with open(file, 'rb') as f:
                    metadata = json.load(f)
                    hash = hashlib.blake2s(str(metadata).encode()).hexdigest()
                    metadata["filename"] = os.path.basename(file)
                    metadata["tags"] = {}
                    return metadata, hash

        # if input is file
        if os.path.isfile(file_path):
            if not file_path.endswith((".txt", ".json")):
                self._log_activity('admit', "FORMAT_ERROR", "The format is invalid.")
                raise TypeError("The format is invalid.")
            metadata, hash = extract_metadata(file_path)
            med_data = {hash[:8]: metadata}
            with open(self.index_file, 'r') as index:
                index_data = json.load(index)
                index_data.update(med_data)
            with open(self.index_file, "w") as index:
                json.dump(index_data, index, indent=4)
            with open(f"{self.objects_dir}/{hash}.data", 'w') as mdate:
                json.dump(metadata, mdate, indent=4)
            
            self._log_activity('admit', "ADMIT", "Information was recorded.")
        
        # if input is folder
        elif os.path.isdir(file_path):
            files = []
            for f in os.listdir(file_path):
                if f.endswith((".txt", ".json")):
                    metadata, hash = extract_metadata(f'{file_path}/{f}')
                    med_data = {hash[:8]: metadata}
                    with open(self.index_file, "r") as index:
                        index_data = json.load(index)
                    index_data.update(med_data)
                    with open(self.index_file, "w") as index:
                        json.dump(index_data, index, indent=4)
                    with open(f"{self.objects_dir}/{hash}.data", 'w') as mdate:
                        json.dump(metadata, mdate, indent=4)
                    files.append(f)
                
            if len(files) == 0:
                self._log_activity('admit', "ADMIT_ERROR", "The specified folder does not contain a file with the correct format.")
                raise RuntimeError("The specified folder does not contain a file with the correct format.")

            else:
                self._log_activity('admit', "ADMIT", "Information was recorded.")
                
    def stats(self):
        """
        to display a collection of data and statical information under management and observation
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        
        with open(self.index_file, "r") as index:
            data = json.load(index)
            total = len(data)
            unmanaged = []
            patients = []
            modalities = []
            tags = []
            for i in os.listdir("./"):
                if i.endswith(".txt"):    
                    if hashlib.blake2s(i.encode('utf-8')).hexdigest()[:8] not in list(data.keys()):
                        unmanaged.append(i)
                elif i.endswith(".json"):
                    with open(i, "rb") as f:
                        file = json.load(f) # have problem
                        if hashlib.blake2s(str(file).encode()).hexdigest()[:8] not in list(data.keys()):
                            unmanaged.append(i)

            for h in list(data.keys()):
                patients.append(data[h]['patient_id'])
                modalities.append(data[h]['modality'])
                tags.append(str(data[h]['tags']))

            stats = {
                "total_entries": total,
                "unmanaged_files": unmanaged,
                "patients": patients,
                "modalities": list(set(modalities)),
                "tags": list(set(tags))
            }

            self._log_activity('stats', "STATS", "All data was retrieved.")
            return stats
    
    def tag(self, id_filename:str, key:str, value:str, remove:bool, is_gui=False):
        """
        to add or remove description tags for a specific data item
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        
        with open(self.index_file, "r") as index:
            index_file = json.load(index)
            hashs = tuple(index_file.keys())
            id_s = [index_file[i]["patient_id"] for i in hashs]
            name_s = [index_file[i]["filename"] for i in hashs]
            if id_filename in id_s:
                tags = list(index_file[hashs[id_s.index(id_filename)]]["tags"])
            if id_filename in name_s:
                tags = list(index_file[hashs[name_s.index(id_filename)]]["tags"])
            if id_filename not in id_s and id_filename not in name_s:
                self._log_activity('tag', "TAG_ERROR", f"The {id_filename} not found.")
                raise RuntimeError("The entered 'ID' or 'filename' does not exist.")
            elif remove:
                if key not in tags:
                    self._log_activity('tag', "TAG_ERROR", "The entered key does not exist in tags list.")
                    raise RuntimeError("The entered key does not exist.")
                else:
                    if id_filename in id_s:
                        del index_file[hashs[id_s.index(id_filename)]]["tags"][key]
                    elif id_filename in name_s:
                        del index_file[hashs[name_s.index(id_filename)]]["tags"][key]
                    with open(self.index_file, "w") as index:    
                        json.dump(index_file, index, indent=4)
                    self._log_activity('tag', "REMOVE_TAG", f"Tag with key {key} was removed from data {id_filename}.")
            else:
                if id_filename in id_s:
                    if key not in list(index_file[hashs[id_s.index(id_filename)]]["tags"].keys()):
                        index_file[hashs[id_s.index(id_filename)]]["tags"][key] = value
                    else:
                        if not is_gui:    
                            if input("A tag with this key already exists.\nAre you sure you want to change it(yes,no)? ").lower() in ('y', "yes"):
                                index_file[hashs[id_s.index(id_filename)]]["tags"][key] = value
                            else:
                                print('No changes were made.')
                                self._log_activity('tag', "ADD_TAG", "Not new tags have been added")
                                return
                        else:
                            answer = messagebox.askyesno('تگ تکراری', "A tag with this key already exists.\nAre you sure you want to change it?")
                            if answer:
                                index_file[hashs[id_s.index(id_filename)]]["tags"][key] = value
                            else:
                                messagebox.showwarning('تگ تکراری', 'No changes were made.')
                                self._log_activity('tag', "ADD_TAG", "Not new tags have been added")
                    with open(self.index_file, "w") as index:    
                        json.dump(index_file, index, indent=4)
                elif id_filename in name_s:
                    if key not in list(index_file[hashs[name_s.index(id_filename)]]["tags"].keys()):    
                        index_file[hashs[name_s.index(id_filename)]]["tags"][key] = value
                    else:
                        if input("A tag with this key already exists.\nAre you sure you want to change it(yes,no)? ").lower() in ('y', "yes"):
                            index_file[hashs[name_s.index(id_filename)]]["tags"][key] = value
                        else:
                            print('No changes were made.')
                            self._log_activity('tag', "ADD_TAG", "Not new tags have been added")
                            return
                    with open(self.index_file, "w") as index:    
                        json.dump(index_file, index, indent=4)
                self._log_activity('tag', "ADD_TAG", f"The data '{id_filename}' was tagged with the value '{key}={value}'.")
    
    def find(self, filename=None, patient_id=None, study_date=None, modality=None, tag=None):
        """
        to search between data with a specific filter
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        
        with open(self.index_file, "r") as index:
            index_file = json.load(index)
            # filename_s = [i["filename"] for i in {index_file.values()}]
            # id_s = [i["patient_id"] for i in {index_file.values()}]
            # study_date_s = [i["study_data"] for i in {index_file.values()}]
            # modality_s = [i["modality"] for i in {index_file.values()}]
            # tags_s = [i["tags"] for i in {index_file.values()}]
        
            results = []

            for entry in index_file:
                match = True
                if filename and index_file[entry]["filename"] != filename:
                    match = False
                if patient_id and index_file[entry]["patient_id"] != patient_id:
                    match = False
                if study_date and index_file[entry]["study_date"] != study_date:
                    match = False
                if modality and index_file[entry]["modality"] != modality:
                    match = False
                if tag:
                    key, value = tag.split('=')
                    if key not in index_file[entry]['tags'].keys() or index_file[entry]['tags'][key] != value:
                        match = False
                
                if match:
                    results.append(index_file[entry])
        self._log_activity('find', "SEARCH", f"Searched with criteria: filename='{filename}', patient_id='{patient_id}', modality='{modality}', date='{study_date}', tag='{tag}'")
        return results
    @classmethod
    def _log_activity(cls, method, activity_type, details):
        """Log an activity to history file"""
        with open(cls.history_file, 'a') as f:
            timestamp = datetime.now().isoformat()

            with open(cls.config_file, "r") as c_f:
                config_file = json.load(c_f)
                
                user = str(config_file).replace('{', '').replace('}', '').replace("'manager':", '')
            
            f.write(f"{timestamp}|command: {method}|{activity_type}: {details}|{user}\n")

    def hist(self, number:int):
        """
        To display history or logs
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        with open(self.history_file, 'r') as h_f:    
            lines = h_f.readlines()
            lines.reverse()
            #
            if number == 'all':
                number = len(lines)
            hist = []
            for l in lines[:number]:
                print(f'{l}', end="")
                hist.append(l)
        
        self._log_activity('hist', "HIST", f"Show {number} recently performed activities")
        return hist
    
    def export(self, id, path):
        """
        To export information
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        
        if not os.path.exists(path):
            self._log_activity('export', "EXPORT_ERROR", "Target directory does not exist.")
            raise RuntimeError("Target directory does not exist.")
        
        files = self.find(patient_id=id)
        if not files:
            # if id file not exist    
            self._log_activity('export', "EXPORT_ERROR", "ID not found.")
            raise RuntimeError("ID not found.")
        for entry in files:
            if os.path.isfile(path):
                self._log_activity('export', "EXPORT_ERROR", f"{os.path.basename(path)} is file and can not write to it your information.")
                raise RuntimeError(f"{os.path.basename(path)} is file and can not write to it your information. you should just enter the folder path.")
            else:
                with open(rf"{path}\{entry['filename']}", "w") as export_file:
                    json.dump(entry, export_file, indent=4)
            self._log_activity('export', "EXPORT", f"Extracted successfully in the file {path}/{entry['filename']} done.")

                
    def remove(self, id_filename):
        """
        To remove information
        """
        if not os.path.isdir(self.bmdm_dir):
            
            raise RuntimeError("First you need to load the boot, run 'python bmdm.py boot' first")
        
        with open(self.index_file, 'r') as i_f:
            index_file = json.load(i_f)
            hashs = list(index_file.keys())
            for h, key in enumerate(index_file):
                entry = index_file[key]
                if entry["filename"] == id_filename or entry["patient_id"] == id_filename:
                    del index_file[hashs[h]]
                    self._log_activity('remove', "REMOVE", f"{id_filename} was removed.")
                    with open(self.index_file, "w") as i_f:
                        json.dump(index_file, i_f, indent=4)
                    return
                else:
                    self._log_activity('remove', "REMOVE_ERROR", f"{id_filename} not found.")
                    raise RuntimeError(f"{id_filename} not found.")
            
            self._log_activity('remove', "REMOVE_ERROR", "The index file is empty.")
            raise RuntimeError('The index file is empty.')