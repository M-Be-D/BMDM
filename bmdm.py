# libraries
import os
import json

class BioMedDataManager:
    """
    # Medical data management
    * Method 'boot' for create hidden folder named '.bmdm' (start management)

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