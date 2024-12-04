from Logger.BrLoggerFile import BrLoggerFile
import aiohttp
import asyncio

async def download_binary_file(ip_address: str, output_filename: str, timeout: int = 10) -> bool:
    url = f"http://{ip_address}/sdm/cgiFileLoop.cgi?type=16&scope=%3CDefault%3E&module=$versinfo&option=0"
    timeout = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(output_filename, 'wb') as file:
                        file.write(content)
                    return True
                else:
                    print(f"Failed to download file. Status code: {response.status}")
                    return False
    except aiohttp.ClientError as e:
        print(f"Client error: {e}")
        return False
    except asyncio.TimeoutError:
        print("Request timed out")
        return False
    except OSError as e:
        print(f"OS error: {e}")
        return False
    
async def download_binary_content(ip_address: str, timeout: int = 10) -> bool:
    url = f"http://{ip_address}/sdm/cgiFileLoop.cgi?type=16&scope=%3CDefault%3E&module=$versinfo&option=0"
    timeout = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    return content
                else:
                    print(f"Failed to download file. Status code: {response.status}")
                    return False
    except aiohttp.ClientError as e:
        print(f"Client error: {e}")
        return False
    except asyncio.TimeoutError:
        print("Request timed out")
        return False
    except OSError as e:
        print(f"OS error: {e}")
        return False


async def readVersion(ip):
    contentLogger = await download_binary_content(ip)
   
    if contentLogger:
        configVersionFound = False
        arVersionFound = False
        logger_file = BrLoggerFile(contentLogger)
        result = {}
        
        for entry in logger_file.entries:
            if entry.EventID == 1076898066:
                configVersionFound = True
                config_data = entry.BinaryData.decode('utf-8', errors='ignore').split('\x00')
                result['configID'] = config_data[0].lstrip('!')
                result['configVersion'] = config_data[1].lstrip('!')
            elif entry.EventID == 1076898062:
                arVersionFound = True
                ar_data = entry.BinaryData.decode('utf-8', errors='ignore').split('\x00')
                result['arVersion'] = ar_data[0].lstrip('!')
                result['serialNumber'] = ar_data[1].lstrip('!')
            
            # If both config and AR version found, return the result
            if configVersionFound and arVersionFound:
                return result
        
    return {}
    
async def main():
    # Example usage to download
    testIp = '192.168.30.206'
    testFileName = 'testLogger.br'
    await download_binary_file(testIp, testFileName)
    logger_file = BrLoggerFile(testFileName) # Access with logger_file.entries

    # Example usage readVersion
    cpuVersion = await readVersion(testIp)
    if cpuVersion:
        print(cpuVersion)
        print(cpuVersion['configID'])
        print(cpuVersion['configVersion'])
        print(cpuVersion['arVersion'])
        print(cpuVersion['serialNumber'])
    else:
        print('-------------- Error reading version --------------')


    # Access properties and methods for debugging
    #print(f"Log Data Length: {logger_file.logDataLength}")
    #print(f"Version: {logger_file.version}")
    #print(f"Offset to UTC: {logger_file.offsetUtc}")
    #print(f"Daylight Saving Time Active: {logger_file.dst}")
    #print(f"Number of Entries: {logger_file.numberOfEntries}")
    #print(f"Lowest Record ID: {logger_file.lowestRecordID}")
    #print(f"Highest Record ID: {logger_file.highestRecordID}")

    # Print all entries
    #for entry in logger_file.entries:
    #    print(entry)

if __name__ == "__main__":
    # Run as async
    asyncio.run(main())
