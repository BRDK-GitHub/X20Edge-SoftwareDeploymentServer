import asyncio
import logging
import sys
import json
from asyncua import Client

# Load configuration from JSON file
def load_config(file_path="config.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        sys.exit(1)

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def monitor_opcua_node(config, interval=2):
    client = Client(config["server_url"])
    
    try:
        await client.connect()
        logging.info(f"Connected to OPC UA Server: {config['server_url']}")
        
        nodes = {}
        for key, node_id in config["nodes"].items():
            nodes[key] = client.get_node(node_id)
        
        while True:
            logging.info("----------------------------")
            for key, node in nodes.items():
                value = await node.read_value()
                logging.info(f"{key}: {value}")
            logging.info("----------------------------")
            
            await asyncio.sleep(interval)  # Wait before reading again
    
    except Exception as e:
        logging.error(f"Error: {e}")
    
    finally:
        await client.disconnect()
        logging.info("Disconnected from OPC UA Server")

if __name__ == "__main__":
    config = load_config("nodesToRead.json")
    asyncio.run(monitor_opcua_node(config, interval=2))
