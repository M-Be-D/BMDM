# libraries
import os
import json

class BioMedDataManager:
    """
    # Medical data management
    * Method 'boot' for create hidden folder named '.bmdm' (start management)
    * Method 'config' to configure and store user or doctor information
    * Method 'admit' to add medical data
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
                    patient_id = parts[0]
                    return metadata, patient_id
            # for 'json' files
            elif file.endswith(".json"):
                with open(file, 'r') as f:
                    metadata = json.load(f)
                    patient_id = metadata["patient_id"]
                    return metadata, patient_id

        # if input is file
        if os.path.isfile(file_path):
            if not file_path.endswith((".txt", ".json")):
                raise TypeError("The format is invalid.")
            metadata, patient_id = extract_metadata(file_path)
            med_data = {patient_id: metadata}
            with open(self.index_file, "a") as index:
                json.dump(med_data, index)
        
        # if input is folder
        elif os.path.isdir(file_path):
            files = []
            for f in os.listdir(file_path):
                if f.endswith((".txt", ".json")):
                    metadata, patient_id = extract_metadata(f'{file_path}/{f}')
                    med_data = {patient_id: metadata}
                    with open(self.index_file, "a") as index:
                        json.dump(med_data, index)
                    files.append(f)
                
            if len(files) == 0:
                print("The specified folder does not contain a file with the correct format.")
                