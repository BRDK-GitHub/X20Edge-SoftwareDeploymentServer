------------------------------------------------------------------
File:          Readme.txt
Version:       1.6.1
Date:          14-Feb-2023
Description:   B&R Power Panel Field T50 system image
------------------------------------------------------------------
Language:      English
Architecture:  ARMv7
------------------------------------------------------------------

Below you will find a short description and version information 
of the package.

------------------------------------------------------------------
GENERAL INFORMATION
------------------------------------------------------------------

With this image you can upgrade a B&R Power Panel Field T50.

For more information see the B&R PP Field T50 Manual.


------------------------------------------------------------------
REQUIREMENTS
------------------------------------------------------------------

A B&R Power Panel Field T50 is required.


------------------------------------------------------------------
INSTALLATION
------------------------------------------------------------------

------------------------------------------------------------------
Version 1.6.1 / 14-Feb-2023 / JP
------------------------------------------------------------------
Features
	- Optional ignoring of server certificate errors.
	- Support for the web browser's Screen Capture API.

Changes
	- Linux Kernel upgrade to 6.1.11
	- Update Samba to 4.14.14
	- Update to Qt 6.4.1 -> QtWebEngine based on Chromium 102

------------------------------------------------------------------
Version 1.5.2 / 09-Feb-2022 / JP
------------------------------------------------------------------
Features
	- Added a VNC connection monitor

Changes
	- Linux Kernel upgrade to 5.15.15

Error corrections
	- ID400356749: FT50 | Network configuration | Service page allows to use empty space in
	              hostname, this causes issue with connection to visu

------------------------------------------------------------------
Version 1.5.0 / 09-Jun-2021 / JP
------------------------------------------------------------------
Features
	- Remote access
	- VNC background color
	- Web: Set/Override viewport settings

Changes
	- Update Samba to 4.10.18
	- Linux Kernel upgrade to 5.10.47
	- Update to Qt 5.15.2 -> QtWebEngine based on Chromium 87

Error corrections
	- ID400348503: FT50 as a mappView client | mappView vizualization restarts every ~ 5 minutes

------------------------------------------------------------------
Version 1.4.0 / 14-May-2020 / JP
------------------------------------------------------------------
Features
	- Added support for handling browser client certificates

Changes
	- Update Samba to 4.10.10
	- Linux Kernel upgrade to 5.6.13
	- Update to Qt 5.13.2 -> QtWebEngine based on Chromium 73

------------------------------------------------------------------
Version 1.3.2 / 25-Sep-2019 / JP
------------------------------------------------------------------
Features
	- Add web developer tools (Chromium remote debugging)
	- Added support to disable browser pinch gesture

Changes
	- Update Samba to 4.8.11
	- Linux Kernel upgrade to 4.14.143
	- Update to Qt 5.12.3 -> QtWebEngine based on Chromium 69
	- Added support for mp4(H264) to browser

------------------------------------------------------------------
Version 1.2.2 / 29-Apr-2019 / JP
------------------------------------------------------------------

- First version.


------------------------------------------------------------------
Copyright (c) by B&R
------------------------------------------------------------------
B&R Industrial Automation GmbH
B&R Straße 1
A - 5142 Eggelsberg 

Tel:   +43 (0)7748/6586-0
Fax:   +43 (0)7748/6586-26
Email: office@br-automation.com
Web:   http://www.br-automation.com
------------------------------------------------------------------
