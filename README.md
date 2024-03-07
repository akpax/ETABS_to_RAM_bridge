# ETABS_to_RAM_bridge
![load_transfer_gif](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/262decf5-798b-4442-9943-0645f9b7bb3d)

## Project Summary
This application is a GUI wrapper between ETABS and RAM Concept. It automates the typically time-consuming task of transferring column forces from ETABS into RAM Concept. It allows the user to specify which ETABS load case, load type, and level and the RAM Concept load layer. Additionally, it provides prompting and validation during API initialization.


## Using the Software
### Configuration
Behind the scenes, the application connects to ETABS and RAM Concept via API. In order to accomplish this, the user is prompted for certain paths which are validated and saved to JSON for future use.


### ETABS Configuration
The application was developed using ETABS 20; therefore, to reduce potential errors, I highly recommend using this version of ETABS when running the application. When the user starts the application, they will be prompted for the ETABSv1.dll file.

![dll file -selection](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/a268c0c8-a272-4ba7-b9c0-f4cbb9c2ab07)


This folder is typically located at:

```
C:\Program Files\Computers and Structures\ETABS 20
```

The program will validate the path and save it for future use in config.json if validation is successful. If unsuccessful, the user will be prompted to provide a different path.

Additionally, for setup, the user must provide the path to the ETABS application executable (.exe) file. Note, this .exe is not validated because a full launch is computationally expensive. If you are having issues launching ETABS, this .exe is likely the culprit. Either edit the config.json directly or delete the .json and be prompted to provide new paths when opening, closing, and reopening the application.

![ETABS_ exe_file_screenshot](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/e6973c3f-ac8c-46ce-a8de-7a41b22b3a4d)


### RAM Concept Configuration
After ETABS is configured, the user will be asked to specify the Python directory of RAM Concept. This Python directory must be installed by the user. Per RAM Concept Documentation, this can be done as follows:


#### Installing RAM Concept API
The API is included with the RAM Concept install, but it is not installed into the Python system on the machine. Per [RAM Concept Documention](file:///C:/Program%20Files/Bentley/Engineering/RAM%20Concept%20CONNECT%20Edition/RAM%20Concept%20CONNECT%20Edition%20V8/python/docs/installing_the_api.html#installing-the-api), we can install it as follows:

* Open a command prompt

* Change the drive and directory to the python subdirectory of your RAM Concept installation.
Note: The RAM Concept directory is typically located at:

```
C:\Program Files\Bentley\Engineering\RAM Concept CONNECT Edition\RAM Concept CONNECT Edition V8
```

* Type the command
```
setup.bat
```
You can also run setup.bat by double-clicking on it, but you will not be able to see any error messages it displays.


#### Checking Installation
To check your installation, you can:

* Open a command prompt.

* Change the drive and directory to the Python subdirectory of your RAM Concept installation.
  
* Type the command:
```
check_install.bat
```
The status of the installation will be reported to the command window.

After installing, you can now select the Python folder when prompted. This folder will be validated and saved for future use.

![python folder](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/19ad76f2-4d4e-4148-a4c9-b94a3618cd52)

Python folder contents:
![RAM_dir folders (contents)](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/b3347f6a-74c5-4c45-bc62-3526d7af4d2d)


## Using Application
### Model Paths Config Tab
After configuration, the main interface will open up where the user is prompted for model paths to the ETABS file and the RAM Concept model they wish to transfer to. The application will add loads to layers so if you intend to update loads, the existing loads should be removed from the layer before the transfer. Note: the RAM Concept model provided will be saved over by the updated version with transferred loads. It is recommended to copy the models before using the application.
![tab1](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/1d850b17-86df-413b-af31-6120fd647888)

Clicking the "Access ETABS and RAM Concept Data" button will open up the ETABS model, extract data, and create the necessary ETABS and RAM objects required.
Note: Since running ETABS analysis is computationally expensive, the application tries to check whether there are existing results before it runs a new analysis. Sometimes the existing results are not seen by the model and a new analysis is run.


## Load Transfer Hub Tab
After data is accessed, the Load Transfer Hub tab is unlocked and this is where the control center of the application is.

![successfull transfer](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/315fcdcf-59ea-41f7-9935-3e63c6070ba8)

The user must specify all ETABS options. By default, the load analysis type is linear static. It can be changed, and the load cases will update accordingly; however, transfer with different load analysis types has not been thoroughly tested. Please submit a GitHub issue if it fails.

The user must choose a load case for RAM Concept or they can add a new layer. Note: when adding a new layer, it will create tables with the information but no load plans for visualization. It is recommended to create a new load layer in the RAM Concept GUI in order to visualize the transferred loads.


## Calibration
After selecting ETABS and RAM Concept options, the Transfer Loads button is still disabled. This is because we need to calibrate the ETABS coordinates to RAM Concept coordinates to ensure the loads are positioned correctly. To do this, the user must enter the coordinates of 2 points in ETABS and the coordinates of those same points in RAM Concept. It is recommended to use distinguishable features like 2 columns or 2 walls. Upon clicking calibrate, the application will calculate the rotation matrix and required displacements to align coordinate systems and use these to convert the ETABS coordinates to RAM coordinates.

![calibration window](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/7435e2b2-6191-48c8-b17c-9c541c51eb8b)

After calibration, the loads can be transferred, and messages should appear in the log box to confirm.
![nmodel with loads](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/d7efaadf-acaa-41e6-bd3d-b420d2723276)

At this point, the user can transfer other loads to different layers or exit the program. When clicking exit, the application first shuts down RAM Concept and ETABS, so there may be a delay between click and window close.


# ETABS/RAM Concept Licensing
Using the API for ETABS/RAM Concept will result in license usage just as manually using the program does. Please take this into account to prevent potential overages.


# Best Practices
Always work on copies of the ETABS and RAM Concept models. This is best practice in case a file is corrupted (has not happened yet but better safe than sorry) or you make a mistake transferring loads into RAM Concept.

Also, it is recommended to spot check RAM Concept layers post-transfer to confirm it worked as expected.


# Common Pitfalls
*License not available
* ETABS .exe file not correctly configured.

  
# Sponsors
Thank you [Mar Structural Design](https://www.marstructuraldesign.com/) for funding this project.
![MSD Full logo](https://github.com/akpax/ETABs_RAM_bridge/assets/78048703/1f5f4ba9-62f8-4e66-85c9-9bcae291d96c)
