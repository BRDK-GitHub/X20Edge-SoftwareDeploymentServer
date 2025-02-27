import os
import xml.etree.ElementTree as ET

def readUpdateInfoFromFile(directory):
    # Recursively search for pipconfig.xml which contains the info
    for root, dirs, files in os.walk(directory):
        if 'pipconfig.xml' in files:
            # Construct the full file path
            file_path = os.path.join(root, 'pipconfig.xml')
            
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract required values
            config_id = root.find('.//ConfigId').text
            PLC_version = root.find('.//OrderNo').text # OrderNo = PLC_version
            config_version = root.find('.//ConfigVersion').text
            
            return config_id, PLC_version, config_version
    
    return None, None, None

if __name__ == "__main__":
    directory_path = "ftp_data\\cm20-v.2.1.21" # Use \\ to avoid escape char
    config_id, PLC_version, config_version = readUpdateInfoFromFile(directory_path)

    print(f"ConfigId: {config_id}")
    print(f"PLC_version: {PLC_version}")
    print(f"ConfigVersion: {config_version}")
