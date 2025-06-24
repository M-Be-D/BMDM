# libraries
import os
import json
import hashlib

class BioMedDataManager:
    """
    # Medical data management
    * Method 'boot' for create hidden folder named '.bmdm' (start management)
    * Method 'config' to configure and store user or doctor information
    * Method 'admit' to add medical data
    * Method 'stats' to display a collection of data and statical information under management and observation
    """
    def __init__(self):
        self.bmdm_dir = ".bmdm"
        self.index_file = ".bmdm/index.json"
        self.config_file = ".bmdm/config.json"
        self.objects_dir = ".bmdm/objects"
        self.history_dir = ".bmdm/history"

    def boot(self):
        """
        This method creates hidden folder named '.bmdm'
        """
        
        # Checking the existence of the bmdm folder
        if os.path.isdir(self.bmdm_dir):
            print("The bmdm folder exists.")
            if not os.path.isfile(self.index_file):
                with open(self.index_file, "w") as index:
                    json.dump([], index)     
            if not os.path.isfile(self.config_file):
                with open(self.config_file, "w") as conf:
                    json.dump({"manager": {"name": "", "email": ""}}, conf)
            if not os.path.isdir(self.objects_dir):
                os.mkdir(self.objects_dir)
            if not os.path.isdir(self.history_dir):
                os.mkdir(self.history_dir)
        
        # Create a folder
        else:    
            os.mkdir(self.bmdm_dir)

            # If the operating system is Windows, it hides it using this method
            if os.name == "nt":
                os.system(f"attrib +h {self.bmdm_dir}")
                
            # create object and history folders
            os.makedirs(self.objects_dir)
            os.makedirs(self.history_dir)

            # create config and index files
            with open(self.config_file, "w") as conf:
                json.dump({"manager": {"name": "", "email": ""}}, conf)
            with open(self.index_file, "w") as index:
                json.dump([], index)
    
    def config(self, name: str = None, email: str = None):
        """
        to configure and store user or doctor information
        """
        if not os.path.isdir(self.bmdm_dir):
            raise "First you need to load the boot. (python bmdm.py boot)"

        # To add name and email to config file
        with open(self.config_file, 'a') as conf:
            config = json.load(conf)
            if name != None:
                config["name"] = name
            if email != None:
                config["email"] = email
            conf.close()
    
    def admit(self, file_path: str):
        """
        To add medical data
        """
        if not os.path.isdir(self.bmdm_dir):
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        if not os.path.exists(file_path):
            raise "Path does not exist"
        
        def extract_metadata(file:str):
            """
            To extract metadata(patient_id, study_date, modality, decryption, path)
            """
            # for 'txt" files
            if file.endswith(".txt"):
                file = os.path.basename(file)
                parts = file.replace(".txt", "").split("_")
                if len(parts) != 4:
                    raise NameError("The file name is incorrect. the correct format is 'PATIENTID_STUDYDATE_MODALITY_DESCRIPTION.txt' ")
                else:
                    metadata = {
                        "patient_id": parts[0],
                        "study_date": parts[1],
                        "modality": parts[2],
                        "description": parts[3],
                        "path": file
                    }
                    hash = hashlib.blake2s(file.encode('utf-8')).hexdigest()
                    return metadata, hash
            # for 'json' files
            elif file.endswith(".json"):
                with open(file, 'r') as f:
                    metadata = json.load(f)
                    hash = hashlib.blake2s(file.encode('utf-8')).hexdigest()
                    return metadata, hash

        # if input is file
        if os.path.isfile(file_path):
            if not file_path.endswith((".txt", ".json")):
                raise TypeError("The format is invalid.")
            metadata, hash = extract_metadata(file_path)
            med_data = {hash[:8]: metadata}
            with open(self.index_file, "a") as index:
                json.dump(med_data, index)
            with open(f"{self.objects_dir}/{hash}.data", 'w') as mdate:
                json.dump(metadata, mdate)
        
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
                print("The specified folder does not contain a file with the correct format.")
                
    def stats(self):
        """
        to display a collection of data and statical information under management and observation
        """
        if not os.path.isdir(self.bmdm_dir):
            raise "First you need to load the boot, run 'python bmdm.py boot' first"
        
        try:
            with open(self.index_file, "r") as index:
                data = json.load(index)
                total = len(data)
                num = 0 # number of data that are not recoded
                for i in os.listdir("./"):
                    if hashlib.blake2s(i.encode('utf-8')).hexdigest()[:8] not in data.keys():
                        num +=1
                # A series of statistical information to be added later
                ...

        except Exception as e:
            if "No such file or directory" in e:
                print("You must first run 'bmdm.py boot'.")
            else:
                print(f"ERROR: {e}")