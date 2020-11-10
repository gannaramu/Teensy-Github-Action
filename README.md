![Build](https://github.com/gannaramu/Teensy-Github-Action/workflows/Build/badge.svg)
# A Github Action to Build a Teensy  based Arduino Project.

the default arduino-cli doesnt currently work for the teensy board as there still needs a fix for the [Pluggable Discovery issue](https://github.com/arduino/arduino-cli/issues/700) . This example uses the Ubuntu envirounment to build the project.

The Steps involved:

 1. Checkout your Repository
 2. Install Arduino IDE (Currently hardcoded to 1.8.13 version)
 3. Install Teenyduino (currently using version 1.53)
 4. Install Supported Libraries that are available on the Library's Manager
 5. Verify the Arduino Code and get the output of the operation to a text file. `build-sketches.sh`
 6. Run check-status.py to go through the error.txt file to see if the build was successful.
 
 ```
 # This is a basic workflow to help you get started with Actions

name: Build

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  runMultipleCommands:
    runs-on: ubuntu-latest
    env: 
      ARDUINO_IDE_VERSION: "1.8.13"
      DEVICE: "teensy40"
      SPEED: "600" 
    steps:
        - name: Check out repository 
          uses: actions/checkout@v1

        - name: Install-Arduino
          run: |
              wget --quiet https://downloads.arduino.cc/arduino-$ARDUINO_IDE_VERSION-linux64.tar.xz
              mkdir $HOME/arduino_ide
              tar xf arduino-$ARDUINO_IDE_VERSION-linux64.tar.xz -C $HOME/arduino_ide/
        - name: Install-Tennsyduino
          run: |  
                curl -fsSL https://www.pjrc.com/teensy/td_153/TeensyduinoInstall.linux64 -o TeensyduinoInstall.linux64
                chmod +x TeensyduinoInstall.linux64
                /sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_1.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :1 -ac -screen 0 1280x1024x16
                sleep 3
                export DISPLAY=:1.0
                ./TeensyduinoInstall.linux64 --dir=$HOME/arduino_ide/arduino-$ARDUINO_IDE_VERSION
        - name: Check-present-working-Directory 
          run: |
                pwd
                ls -r
                cd ..
                ls
        - name: Install Additional Libraries
          run: |
                cd $HOME/arduino_ide/arduino-$ARDUINO_IDE_VERSION/
                ./arduino --install-library "base64"
        - name: Verify-Code 
          run: bash build-sketches.sh
        
        - name: upload-Code 
          uses: actions/upload-artifact@v2
          with:
            name: my-artifact
            path: error.txt
        - name: Check-Status 
          run: python3 check-status.py
         
```yml
