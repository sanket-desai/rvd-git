# Raman spectroscopy based RNA Virus Detector (RVD)

A GUI based tool to predict RNA virus positivity of a sample based on the Raman spectra files (SPC).

## About SPC data format

SPC is a binary data format to store a variety of spectral data, developed by Galactic Industries Corporation in the '90s. Popularly used Thermo Fisher/Scientific software GRAMS/AI [1]. Also used by others including Ocean Optics, Jobin Yvon Horiba. Can store a variety of spectrum including FT-IR, UV-VIS, X-ray Diffraction, Mass Spectroscopy, NMR, Raman and Fluorescence spectra.


## Requirements

```
python2.7+
Python packages:
	- numpy
	- Tkinter
R ( version > 3.5)
R-packages:
	- tidyverse
	- caret
	- MASS
```
## Installation

Download the Linux based RVD source from (link) and extract the zip. Inside the resulting folder (unzipped directory) the main start program is src/rvd-gui.py. There is no need to run any installer for this program.

## Execution

```bash
$ cd rvd-git
$ python src/rvd-gui.py
```
GUI starts up, wherein you need to provide the input directory with SPC files, project name and output directory.

## GUI usage
User is required to fill the following fields and press <i>Submit</i> to begin processing:

![RVD GUI](https://github.com/sanket-desai/rvd-git/raw/master/RVD_GUI.jpg)

## Output

The results are stored in the output directory in the file ending with "_predict.csv". For a project name, "analysis" the output file name of the prediction in the output directory would be "analysis_prediction.csv". The CSV file can be opened in any editor or spreadsheet / excel program.

The output file contains following columns:
1. Sample name (file name)
2. Prediction (virus positivity) - Yes / No

## References

[1] "Thermo Scientific SPC File Format." Thermo Fisher Scientific, Web. 20 July 2014\. <http://ftirsearch.com/features/converters/SPCFileFormat.htm>.
