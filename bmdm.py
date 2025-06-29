# libraries
import os
import json
import hashlib
from datetime import datetime

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
    def __init__(self):
        self.bmdm_dir = ".bmdm"
        self.index_file = ".bmdm/index.json"
        self.config_file = ".bmdm/config.json"
        self.objects_dir = ".bmdm/objects"
        self.history_file = ".bmdm/history.log"

    def boot(self):
        """
        This method creates hidden folder named '.bmdm'
        """
        
        # Checking the existence of the bmdm folder
        if os.path.isdir(self.bmdm_dir):
            print("The bmdm folder exists.")
            self._log_activity("BOOT", "The bmdm folder exists.")

            if not os.path.isfile(self.index_file):
                with open(self.index_file, "w") as index:
                    json.dump([], index)     
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
                json.dump([], index)
                
        self._log_activity("BOOT", "BMDM initialized")
    
    def config(self, name: str = None, email: str = None):
        """
        to configure and store user or doctor information
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot. (python bmdm.py boot)"

        # To add name and email to config file
        with open(self.config_file, 'a') as conf:
            config = json.load(conf)
            if name != None:
                config["name"] = name
            if email != None:
                config["email"] = email
            conf.close()
        
        self._log_activity("CONFIG_UPDATE", f"Updated config: name={name}, email={email}")
    
    def admit(self, file_path: str):
        """
        To add medical data
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        if not os.path.exists(file_path):
            self._log_activity("PATH_ERROR", "Path does not exist.")
            raise "Path does not exist"
        
        def extract_metadata(file:str):
            """
            To extract metadata(patient_id, study_date, modality, decryption, path)
            """
            # for 'txt" files
            if file.endswith(".txt"):
                file = os.path.basename(file)
                parts = file.replace(".txt", "").split("_")
                if len(parts) < 4:
                    self._log_activity("TYPE_ERROR", "The input file type is incorrect.")
                    raise NameError("The file name is incorrect. the correct format is 'PATIENTID_STUDYDATE_MODALITY_DESCRIPTION.txt' ")
                else:
                    metadata = {
                        "filename": file,
                        "patient_id": parts[0],
                        "study_date": parts[1],
                        "modality": parts[2],
                        "description": parts[3:],
                        "path": file,
                        "tags": {}
                    }
                    hash = hashlib.blake2s(file.encode('utf-8')).hexdigest()
                    return metadata, hash
            # for 'json' files
            elif file.endswith(".json"):
                with open(file, 'rb') as f:
                    metadata = json.load(f)
                    metadata["filename"] = file
                    metadata["tags"] = {}
                    file = f.read()
                    hash = hashlib.blake2s(file.encode('utf-8')).hexdigest()
                    return metadata, hash

        # if input is file
        if os.path.isfile(file_path):
            if not file_path.endswith((".txt", ".json")):
                self._log_activity("FORMAT_ERROR", "The format is invalid.")
                raise TypeError("The format is invalid.")
            metadata, hash = extract_metadata(file_path)
            med_data = {hash[:8]: metadata}
            with open(self.index_file, "a") as index:
                json.dump(med_data, index)
            with open(f"{self.objects_dir}/{hash}.data", 'w') as mdate:
                json.dump(metadata, mdate)
            
            self._log_activity("ADMIT", "Information was recorded.")
        
        # if input is folder
        elif os.path.isdir(file_path):
            files = []
            for f in os.listdir(file_path):
                if f.endswith((".txt", ".json")):
                    metadata, hash = extract_metadata(f'{file_path}/{f}')
                    med_data = {hash[:8]: metadata}
                    with open(self.index_file, "a") as index:
                        json.dump(med_data, index)
                    with open(f"{self.objects_dir}/{hash}.data", 'w') as mdate:
                        json.dump(metadata, mdate)
                    files.append(f)
                
            if len(files) == 0:
                self._log_activity("ADMIT_ERROR", "The specified folder does not contain a file with the correct format.")
                print("The specified folder does not contain a file with the correct format.")

            else:
                self._log_activity("ADMIT", "Information was recorded.")
                
    def stats(self):
        """
        to display a collection of data and statical information under management and observation
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        try:
            with open(self.index_file, "r") as index:
                data = json.load(index)
                total = len(data)
                num = 0 # number of data that are not recoded
                for i in os.listdir("./"):
                    if i.endswith(".txt"):    
                        if hashlib.blake2s(i.encode('utf-8')).hexdigest()[:8] not in data.keys():
                            num +=1
                    elif i.endswith(".json"):
                        with open(i, "rb") as f:
                            file = f.read()
                            if hashlib.blake2s(file.encode('utf-8')).hexdigest()[:8] not in data.keys():
                                num += 1
                # A series of statistical information to be added later
                ...

                self._log_activity("STATS", "All data was retrieved.")

        except Exception as e:
            if "No such file or directory" in e:
                self._log_activity("BOOT_ERROR", "Boot command not executed.")
                print("You must first run 'bmdm.py boot'.")
            else:
                self._log_activity("STATS_ERROR", e)
                print(f"ERROR: {e}")
    
    def tag(self, id_filename:str, key:str, value:str=None, remove= False):
        """
        to add or remove description tags for a specific data item
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        with open(self.index_file, "a") as index:
            index_file = json.load(index)
            tags = dict(i["tags"] for i in index_file.value()["tags"])
            hashs = tuple(index_file.keys())
            id_s = [i["patient_id"] for i in dict(index_file.values())]
            name_s = [i["filename"] for i in dict(index_file.values())]
            if id_filename not in id_s or id_filename not in name_s:
                self._log_activity("TAG_ERROR", f"The {id_filename} not found.")
                raise "The entered ID does not exist."
            elif remove:
                if key not in tags:
                    self._log_activity("TAG_ERROR", "The entered key does not exist in tags list.")
                    raise "The entered key does not exist."
                else:
                    index_file.values()["tags"].pop(key)
                    json.dump(index_file, index)
                    self._log_activity("REMOVE_TAG", f"Tag with key {key} was removed from data {id_filename}.")
            else:
                if id_filename in id_s:
                    index_file[hashs[id_s.index(id_filename)]]["tags"][key] = value
                    json.dump(index_file, index)
                elif id_filename in name_s:
                    index_file[hashs[name_s.index(id_filename)]]["tags"][key] = value
                    json.dump(index_file, index)
                self._log_activity("ADD_TAG", f"The data {id_filename} was tagged with the value {key}={value}.")
    
    def find(self, filename=None, patient_id=None, study_date=None, modality=None, tag=None):
        """
        to search between data with a specific filter
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        with open(self.index_file, "r") as index:
            index_file = json.load(index)
            # filename_s = [i["filename"] for i in {index_file.values()}]
            # id_s = [i["patient_id"] for i in {index_file.values()}]
            # study_date_s = [i["study_data"] for i in {index_file.values()}]
            # modality_s = [i["modality"] for i in {index_file.values()}]
            # tags_s = [i["tags"] for i in {index_file.values()}]
        
            results = []

            for entry in index_file:
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
                    if key not in index_file[entry]['tags'].keys() and index_file[entry]['tags'][key] != value:
                        match = False
                
                if match:
                    results.append(index_file[entry])
        self._log_activity("SEARCH", f"Searched with criteria: filename={filename}, patient_id={patient_id}, modality={modality}, date={study_date}, tag={tag}")
        return results
    
    def _log_activity(self, activity_type, details):
        """Log an activity to history file"""
        with open(self.history_file, 'a') as f:
            timestamp = datetime.now().isoformat()

            with open(self.config_file, "r") as c_f:
                config_file = json.load(c_f)
                
                user = str(config_file).replace('{', '').replace('}', '')
            
            f.write(f"{timestamp}|{activity_type}: {details}|{user}\n")

    def hist(self, number=5):
        """
        To display history or logs
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        with open(self.history_file, 'r') as h_f:    
            lines = h_f.readlines()
            lines.reverse()
            for l in lines[:number+1]:
                print(f'{l}\n')
        
        self._log_activity("HIST", f"Show {number} recently performed activities")

    def export(self, id, path):
        """
        To export information
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        if not os.path.exists(path):
            self._log_activity("EXPORT_ERROR", "Target directory does not exist.")
            raise "Target directory does not exist."
        
        with open(self.index_file, "r") as i_f:
            index_file = json.load(i_f)
            metadata = dict(index_file.values())
            for entry in metadata:
                if entry["patient_id"] == id:
                    if os.path.isfile(path):
                        self._log_activity("EXPORT_ERROR", f"{os.path.basename(path)} is file and can not write to it your information.")
                        raise f"{os.path.basename(path)} is file and can not write to it your information. you should just enter the folder path."
                    else:
                        with open(rf"{path}/{metadata["filename"]}", "w") as export_file:
                            json.dump(entry, export_file)
                    self._log_activity("EXPORT", f"Extracted successfully in the file {path}/{metadata["filename"]} done.")
                    return

            # if id file not exist    
            self._log_activity("EXPORT_ERROR", "ID not found.")
            raise "ID not found."
                
    def remove(self, id_filename):
        """
        To remove information
        """
        if not os.path.isdir(self.bmdm_dir):
            self._log_activity("BOOT_ERROR", "Boot command not executed.")
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        with open(self.index_file, 'a') as i_f:
            index_file = json.load(i_f)
            
            for h, entry in enumerate(index_file):
                if entry["filename"] == id_filename or entry["patient_id"] == id_filename:
                    index_file.pop(h)
                    self._log_activity("REMOVE", f"{id_filename} was removed.")
                    return
                else:
                    self._log_activity("REMOVE_ERROR", f"{id_filename} not found.")
                    raise f"{id_filename} not found."