import os
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def readUpdateFolderName(directory_path):
    try:
        # Path to the XML file
        xml_file_path = os.path.join(directory_path, 'arnbcfg.xml')

        # Check if the XML file exists
        if not os.path.isfile(xml_file_path):
            logging.info(f"readUpdateFolderName failed: XML file not found ")
            logging.info(f"directory_path: {directory_path}")
            return ''
        
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Search for the PIPCONFIG element
        pipconfig_element = root.find(".//PIPCONFIG")
        
        if pipconfig_element is not None:
            # Extract the path attribute from PIPCONFIG
            pipconfig_path = pipconfig_element.get('Path', '')
            
            # Check if '/pipconfig.xml' is in the path and extract the folder name
            if '/pipconfig.xml' in pipconfig_path:
                folder_name = pipconfig_path.split('/')[0]
                return folder_name
        return ''
    except Exception as e:
        # In case of any error, return an empty string
        logging.info(f"readUpdateFolderName failed: {e}")
        return ''


if __name__ == "__main__":
    directory_path = "ftp_data\\cm20-2.1.20" # Use \\ to avoid escape char
    config_id, PLC_version, config_version = readUpdateInfoFromFile(directory_path)

    print(f"ConfigId: {config_id}")
    print(f"PLC_version: {PLC_version}")
    print(f"ConfigVersion: {config_version}")

    # test readUpdateFolderName
    updateUpdateFolderName = readUpdateFolderName(directory_path)
    print(f"Update Folder Name: {updateUpdateFolderName}")
