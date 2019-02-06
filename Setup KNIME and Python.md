# How to set up KNIME and Python
## Install KNIME
Download KNIME [here](https://www.knime.com/downloads/download-knime) and install it. This requires administrative rights.

## Install Python (Anaconda)
1. Download Anaconda [here](https://www.anaconda.com/distribution/#download-section). Select your operating system, 64-bit version and Python 3+.
1. Run the installer and select the following options during the installation:
    * Install as current user.
    * Don't add to path.
    * Make this Python version the default.

## Setup Python
1. Open an Anaconda Prompt.
1. You are now in the `base` virtual environment. See the prompt `(base) C:\>`.
1. Check your Python version with `python --version`.
1. Create a new [virtual environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) with
```(base) C:\> conda create -n py37_knime python=3.7 jedi pandas geopandas```
    * See this [blog](https://www.knime.com/blog/setting-up-the-knime-python-extension-revisited-for-python-30-and-20) for more information.
    * It's not necessary to supply the third Python version number. Those are bugfixes and it will always use the latest.

You can activate and deactivate this environment with `activate py37_knime` and `deactivate` respectively. But for this setup, activation is not needed.

Create a .bat file which KNIME can use to address Python based on this example:
```
@REM Adapt the directory in the PATH to your system    
@SET PATH=<path/to/anaconda>;%PATH%  
@CALL activate py37_knime || ECHO Activating py37_knime failed  
@python %*
```
Replace `<path/to/anaconda>` with your path to Anaconda. You can find this by running `where python` in an Anaconda Prompt, removing `python.exe` and adding `\Scripts`. For me it was `C:\Users\abos\AppData\Local\Continuum\anaconda3\Scripts`.

Save the file as `py37_knime.bat` and put it in your home directory.

## Setup KNIME
1. Open KNIME.
1. Install KNIME Python Integration:
    1. Go to File > Install KNIME extensions,
    1. Search for "Python",
    1. Select "KNIME Python Integration",
    1. Follow the wizard until finished and restart KNIME if prompted.
1. Go to File > Preferences > KNIME > Python.
1. Change the path to Python 3 executable:
    1. Browse to your home directory,
    1. Select `py37_knime.bat`.
1. If all went well, it shows "Python version: 3.7".    
    
    