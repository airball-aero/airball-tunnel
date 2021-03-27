# Getting started

## Install Python

This step installs the basic Python programming language plus a lot of helpful utilities that come bundled with it.

Download the latest Windows (64 bit) installer from the following. Get the latest release (currently 3.9.2):

    https://www.python.org/downloads/windows/

Run the installer. Choose a straightforward "Install now" but be sure to check “Add Python to environment variables”; leave everything else as-is.

**Test:** Open a new command shell (it must be new for your newly installed programs to be recognized). Type `python`. You should get a new prompt with three carets, like, `>>>`. You are now in Python and can type Python commands. When done, type `exit()`.

## Install Scipy

Scipy is a bunch of utilities for scientific and numerical programming. Once you have Python installed, you can install additional packages using the `pip` command.

In a new command shell, type `pip install scipy`. This will install `scipy`, and the `numpy` module that it depends on.

**Test:** In Python (see above), type `import scipy`. This should work without an error. Try typing `dir(scipy)` to get a list of all the symbols that the `scipy` module gives you.

## Install Dynamixel SDK

This installs a series of utilities for interfacing to the Dynamixel servos. You will get them from their home page on Github, which is a popular place for software developers to coordinate their work.

Go to the home page of the project on Github at:

    https://github.com/ROBOTIS-GIT/DynamixelSDK

Find the green button called `Code`, click the down arrow and click `Download ZIP`.

Double click on the resulting ZIP file to extract it. Choose `Extract All` to extract to some location -- here we are assuming, for example, that if your username is `<username>`, you put it in:

    `C:\Users\<username>\Desktop\DynamixelSDK-master`

Open a Windows command shell and go to the `DynamixelSDK-master/python` folder. Type `setup.py install`.

**Test:** In Python, `import dynamixel_sdk`, and maybe also use the `dir()` trick to see the symbols you can get from that module.

## Install Git

Git is software that allows programmers to collaborate by editing various pieces of a large project independently, and merging their edits together in a controlled fashion. Github is a site that hosts Git repositories (or "repos").

Go to the home page of the project:

    https://git-scm.com/download/win

Choose `64-bit Git for Windows Setup`. Run the downloaded file and click on `Next` in all the options; there is no need to change anything.

**Test:** In a new Windows command shell, type `git`. This should run the program and give you a list of all its options.

## Clone the `airball-tunnel` project

In the Git world, to "clone" a project means to grab a copy of it from somewhere else, with all the files in their latest state, but also containing the entire history of all the changes that have ever been made. Since everyone has all the history, anyone can connect to anyone else's "clone" of the project and merge changes to the project they wish.

Open a new Windows command shell and go to some directory, for example:

    `C:\Users\user1\Desktop`

Type:

    `git clone https://github.com/airball-aero/airball-tunnel.git`

**Test:** This should succeed quickly and create a directory called `airball-tunnel`.

## Run the test program

This is a basic test that we can run the programs and deal with the output they produce.

Go to `airball-tunnel/python`. Run the program `sweep.py`.

It will ask you for a device name. Type anything at this point - e.g. `COM1`.

It will also ask you for a file name. Provide any name for the output file you wish. It will work best if your name ends in `.csv`, e.g., `condition1-50kias.csv`.

**Caution:** If you type in the name of an existing file, it will be overwritten!!

The program should give you a bunch of messages about what it’s doing--moving to various locations, reading from Scanivalve. All these are faked out with random numbers. The result should be a file with the name you chose.

Try opening that file in Excel. Try looking at its contents. Imagine how you might use it from a program yourself.