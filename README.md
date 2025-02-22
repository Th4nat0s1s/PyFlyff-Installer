# This is an Installer (.msi) version only!

All I have done is put ils94's amazing work into an easy to use MSI installer that should allow you to select an install location  and also apply a game shortcut for the PyFlyff.exe

All of this has been done without ils94's permission, but done in good faith and I hope to be able to continue to keep this project up to date with his changes but I will probably only make updates for larger changes.

If for whatever reason; I fall off the face of the earth or you want an update sooner than I update this installer... just download the zip from ils94's main project (https://github.com/ils94/PyFlyff) and overwrite the ".\Sob3k Installer\PyFlyff Installer\" directory with its contents. 



# PyFlyff
QtWebEngine to play Flyff Universe

# If you wish to support me :)

Bitcoin: 
1JDWqkVGeAw9a6ikUkk8q9n6vwA7pft6Ke

Ethereum: 
0x0fd9b73f25572b54de686c28e1050e25eed552e9

Dash: 
XyTGmhWzeQjNKnTeTD1UpFC3zubqurjtwt

Solana:
41hkroUbrDfYGh8Pmfd7gVAyXMTvFC8eacCyLyD1VHn7

Dogecoin: 
D6nnCqVUyUtL7FLtrmhjh9yLCcN54QjSuZ

# Client Hotkeys

Ctrl+Shift+F5 = reload client back to https://universe.flyff.com/play

Ctrl+Shift+F11 = enter/exit main window fullscreen

Ctrl+Shift+PgUp (PageUp) open a new client window

To stop the Mini Ftool loop, press the Activation Key again.

# Features

Mini Ftool: You can setup up to 3 hotkeys to automatically use a skill/item for you (good for heal spam or mage/psy/elementor 1x1). To stop it, press the same key you used to start the loop.

To setup the second hotkey and third key, separate them with a comma ","

Example: 

In-Game Hotkey(s): f1,5
Interval(s): 1,45

Note that, "f1" will always be pressed, and once the interval reaches 45 seconds, it will then press the "5" key.

"Fix Loop" is an option that will or not fix the loop sequence, because mathematically both second and third key will be pressed at the same time during the loop.
If you don't want that, set "Fix Loop" to YES, if you want the keys to keep going and be pressed once their time threshold reaches it, set it to "NO".

"YES" is good if you are using skills, "NO" is good if you are using consumables in the second and third key.

Min Interval is a way for you to have more control to when the Mini Ftool should press the first key. If you set the Min Interval to 5 and the first key to 5, it will remove the randomness offset and always press the first key exactly after every 5 seconds. If you set the Min Interval to 5 and the first key to 10, it will press the first key in a random offset between 5 and 10.

Alt Control: You can set hotkeys for the Main Client to send a direct command to the Alt Client. Good if you don't want to use the Mini Ftool, but still want to command your FS/RM without having to alt+tab. To set multiple keys (up to 20 keys) add commas between each one.

Example:

Main Client Hotkey: q,e,f1...

Alt Client Hotkey: 1,2,3...

Reset Hotkeys: Clear the variables values from Mini Ftool and Alt Control keys as well as the variable containing the value that is used to identify which window is the Main Client and which window is the Alt Client. Good in case you want to switch keys on both Mini Ftool and Alt Control without the need of completly restarting the PyFlyff Client.

User Agent: You can use this to spoof from where you are playing Flyff Universe, or, you can use it in case you are having trouble with your Google Account login / recaptcha challenge (see the "Known Issues so far" section of this README)

Community: You can access community links within the client, like Flyffipedia, Madrigal Inside, Flyffulator, Madrigal Maps, Flyff Model Viewer, Skillulator

# Disclaimer

As you can see, I added bot like features to my Client. They are simple, yet, very convenient tools to make the grind a bit more bearable, but keep in mind that using automation is against the rules and you might get banned for it. The Mini Ftool generate a random wait time for every repeatable action, but this does not prevent from a GM to identify that you are in fact botting, so try to not abuse it, you have been very much warned.

# Known Issues so far

If when you try to login wih your Google Account, and Google mark my Client as unsafe, set your User Agent by pressing the button "Set User Agent" in the toolbar and type in the input box: None

Hit save and restart the Client, it should let you login with no problem now.

Sometimes you won't be able to resolve the recaptcha challenge since it will report that PyFlyff is an outdated browser, to fix it, set your User Agent to anything really and it will bypass this check.

# How to compile it yourself

You i'll need to pip install those modules to your Python installation:

pip install pyinstaller pywin32 PyQt5 PyQtWebEngine

Then create a .BAT file with this:

IF your Python installation is ACCESSIBLE from Windows Env variables:

pyinstaller PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole
xcopy icons dist\PyFlyff\icons\

IF your Python installation is NOT accessible from Windows Env variables, then you will have to fully tell both python.exe and pyinstaller script locations in the command line:

Path/to/your/python.exe path/to/your/pyinstaller.py PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole
xcopy icons dist\PyFlyff\icons\

pyinstaller.py script is located in your Python installation folder - Scripts

Save both .BAT and put it inside the project folder and run it, wait for the compilation to finish and the resulted folder named "PyFlyff" will appear inside the dist folder created by pyinstaller inside the project folder.

After the compilation is finished, make sure the folder "icons" is inside the generated PyFlyff folder inside the dist folder, else it will give an error when opening the client.

# Android Client

I also made an Android Client that makes it easier for your to Dual Client using your Android Device.

Here is the link: https://github.com/ils94/FlyffUAndroid
