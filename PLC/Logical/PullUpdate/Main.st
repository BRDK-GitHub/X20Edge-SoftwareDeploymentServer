
PROGRAM _INIT
	
	// Read current version
	WHILE NOT ArProjectGetInfo_0.Done AND NOT ArProjectGetInfo_0.Error DO
		ArProjectGetInfo_0.Execute := TRUE;
		ArProjectGetInfo_0();
	END_WHILE
	// See Current Version in: ArProjectGetInfo_0.ConfigurationVersion & ArProjectGetInfo_0.ConfigurationID
	
END_PROGRAM

PROGRAM _CYCLIC

	CASE state OF
		
		0:
			DevLink_0.enable := TRUE;
			DevLink_0.pDevice := ADR('PLCUPDATE');
			DevLink_0.pParam := ADR('/SIP=192.168.30.64 /PROTOCOL=ftp /USER=update /PASSWORD=update');
			DevLink_0();
		
			IF DevLink_0.status = ERR_OK OR DevLink_0.status = fiERR_DEVICE_ALREADY_EXIST THEN
				DevLink_0.enable := FALSE;
				DevLink_0();
				state := 10;
			ELSIF DevLink_0.status <> ERR_FUB_BUSY THEN
				state := 222;
			END_IF
		
		10:
			IF DownloadUpdate THEN
				// Will download update with name 'updateFolderName'
				DownloadUpdate := FALSE;
				state := 20;
			ELSIF CheckVersion THEN
				// Will check version of update with name 'updateFolderName' 
				CheckVersion := FALSE;
				ArProjectGetPackageInfo_0.Execute := FALSE;
				ArProjectGetPackageInfo_0();
				state := 30;
			ELSIF ExecuteUpdate THEN
				// Will Execute update with name 'updateFolderName' 
				ExecuteUpdate := FALSE;
				ArProjectInstallPackage_0.Execute := FALSE;
				ArProjectInstallPackage_0();
				state := 40;
			END_IF
		
		20:
			DirCopy_0.enable := TRUE;
			DirCopy_0.pSrcDev := ADR('PLCUPDATE');
			DirCopy_0.pSrcDir := ADR(updateFolderName);
			DirCopy_0.pDestDev := ADR('ROOT');
			DirCopy_0.option := fiOVERWRITE;
			DirCopy_0();
		
			IF DirCopy_0.status = ERR_OK THEN
				DirCopy_0.enable := FALSE;
				DirCopy_0();
				state := 10;
			ELSIF DirCopy_0.status <> ERR_FUB_BUSY THEN
				state := 222;
			END_IF
		
		30:
			ArProjectGetPackageInfo_0.Execute := TRUE;
			ArProjectGetPackageInfo_0.DeviceName := 'ROOT';
			ArProjectGetPackageInfo_0.FilePath := CONCAT(updateFolderName,'/Default_X20CP04xx/pipconfig.xml');
			ArProjectGetPackageInfo_0();
			
			IF ArProjectGetPackageInfo_0.Done THEN
				state := 10;
			ELSIF ArProjectGetPackageInfo_0.Error THEN
				state := 222;
			END_IF
			
		40:
			ArProjectInstallPackage_0.Execute := TRUE;
			ArProjectInstallPackage_0.DeviceName := 'ROOT';
			ArProjectInstallPackage_0.FilePath := CONCAT(updateFolderName,'/Default_X20CP04xx/pipconfig.xml');
			ArProjectInstallPackage_0();
			
			IF ArProjectInstallPackage_0.Done THEN
				state := 10;
			ELSIF ArProjectInstallPackage_0.Error THEN
				state := 222;
			END_IF
			
		222:
		
			IF reset THEN
				reset := FALSE;
				DirCopy_0.enable := FALSE;
				DirCopy_0();
				DevLink_0.enable := FALSE;
				DevLink_0();
				ArProjectGetPackageInfo_0.Execute := FALSE;
				ArProjectGetPackageInfo_0();
				ArProjectInstallPackage_0.Execute := FALSE;
				ArProjectInstallPackage_0();
				state := 0;
			END_IF
			
	END_CASE
	
END_PROGRAM

PROGRAM _EXIT

	 
END_PROGRAM

