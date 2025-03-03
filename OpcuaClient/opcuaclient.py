import asyncio
import logging
import sys
from asyncua import Client

# OPC UA Server URL
URL = "opc.tcp://192.168.30.100:4840"

# OPC UA Node to read
SoftwareNameNodeId = "ns=6;s=::PullUpdate:ArProjectGetInfo_0.ConfigurationID"
SoftwareVersionNodeId = "ns=6;s=::PullUpdate:ArProjectGetInfo_0.ConfigurationVersion"

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def monitor_opcua_node(interval=2):
    client = Client(URL)

    try:
        await client.connect()
        logging.info(f"Connected to OPC UA Server: {URL}")
        nodeName = client.get_node(SoftwareNameNodeId)
        nodeVersion = client.get_node(SoftwareVersionNodeId)

        while True:
            name = await nodeName.read_value()
            version = await nodeVersion.read_value()
            logging.info("----------------------------")
            logging.info(f"Software Name: {name}")
            logging.info(f"Software Version: {version}")
            logging.info("----------------------------")
            
            await asyncio.sleep(interval)  # Wait before reading again

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        await client.disconnect()
        logging.info("Disconnected from OPC UA Server")

if __name__ == "__main__":
    logging.info(f"Running OPC UA Client to monitor node {SoftwareNameNodeId} and {SoftwareVersionNodeId}")
    asyncio.run(monitor_opcua_node(interval=2))
