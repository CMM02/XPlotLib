# XPlotLib
This is a libary to analyze and plot experimental and calculated XES and XAS data. 

## Requirements
You will need Python 3.10 or newer and jupyter notebook installation.

## Installation
Install the package using the following command:
```
$ pip install XPlotLib
```

## Running
Launch your jupyter installation, f.e.:
```
$ jupyter notebook
```

## Setup
Make sure `matplotlib` widgets are enabled
```py
# %matplotlib widget
```



## Example

### DOSAnalyzer
Import module and enable matplotlib widgets
```py
# %matplotlib widget
# import DOSAnalyzer
from XPlotLib.DOSAnalyzer import DOSAnalyzer
```
Load data
```py
# create new instance of DOSAnalyzer
dosAnalyzer = DOSAnalyzer()
#load GS data with directory, filename without extension, site names and site binding energies
dosAnalyzer.load_dos(dir, 'Ti3O5_DOS_O_GS', {'1': 'O1_ES', '2': 'O2_ES'}, {'O1_ES': 10.0, 'O2_ES': 11.0})
#load ES data with directory, filename without extension, site name and site binding energie
dosAnalyzer.load_single_dos(dir, 'Ti3O5_DOS_O1_ES', 'O1_ES', 10.0)
dosAnalyzer.load_single_dos(dir, 'Ti3O5_DOS_O2_ES', 'O2_ES', 11.0)
# load broadened spectra with path and name to display
dosAnalyzer.load_spectrum(dir + 'Ti3O5-brd_O_XES.csv', name='Ti3O5 calc XES', spec_type='XES')
dosAnalyzer.load_spectrum(dir + 'Ti3O5-brd_O_XANES.csv', name='Ti3O5 calc XAS', spec_type='XAS')
# load measured spectra with path and name to display
dosAnalyzer.load_spectrum(dir + 'Ti3O5_O_XES.csv', name=f'Ti3O5 exp XES', spec_type='XES', skiprows=2)
dosAnalyzer.load_spectrum(dir + 'Ti3O5_O_XAS.csv', name=f'Ti3O5 exp XAS', spec_type='XAS', skiprows=2)
```

Print available DOS to plot
```py
dosAnalyzer.print_dos_options()
```

Configure plot and show
```py
# set DOS to display
dosAnalyzer.set_active_dos(xes_names=['O1_GS_p', 'O2_GS_p'], xas_names=['O1_ES_p', 'O2_ES_p'])
# set scale of DOS
dosAnalyzer.set_custom_dos_scale(1.5, 1.5)
# set title
dosAnalyzer.set_title('Ti3O5 DOS Analysis')
# plot with staggered option on
dosAnalyzer.plot_dos(staggered=True)
```

Export DOS
```py
# export DOS target path and file name
dosAnalyzer.export_dos(dir, 'Ti3O5_DOS_Analysis')
```

### BandgapAnalyzer
Import module and enable matplotlib widgets
```py
# %matplotlib widget
# import BandgapAnalyzer
from XPlotLib.BandgapAnalyzer import BandgapAnalyzer
```
Load data
```py
# create new instance of BandgapAnalyzer
bandgapAnalyzer = BandgapAnalyzer()
# load experimental spectra with path to file, spectra type and name of measurement
bandgapAnalyzer.load_exp_spectra(dir + '/data/Ti3O5_O_XES.csv', 'xes', ['XES'])
bandgapAnalyzer.load_exp_spectra(dir + '/data/Ti3O5_O_XAS.csv', 'xas', ['TEY', 'PFY'])
# load calculated spectra with path to file, spectra type and name of calculation
bandgapAnalyzer.load_calc_spectra(dir + '/Ti3O5-brd_O_XES.csv', 'xes', 'XES calc')
bandgapAnalyzer.load_calc_spectra(dir + '/data/Ti3O5-brd_O_XAS.csv', 'xas' , 'XAS calc')
bandgapAnalyzer.load_calc_spectra(dir + '/data/Ti3O5-brd_O_XANES.csv', 'xas', 'XANES calc')
```

Smoothen XES and XAS
```py
# smoothen XES using a SavGol-filter with spectra type, window size, polynomial, onset_region and option to display graph with smoothening
bandgapAnalyzer.smoothen('xes', 'XES', 15, 2, [526, 533], show=True)
```
```py
# smoothen XAS using a SavGol-filter with spectra type, window size, polynomial, onset_region and option to display graph with smoothening
bandgapAnalyzer.smoothen('xas', 'PFY', 15, 2, [528, 530], show=False)
```

Configure plot and show
```py
# set title
bandgapAnalyzer.set_title('Ti3O5')
# set xlims for xes and xas
bandgapAnalyzer.set_xlims([515, 535], [520, 540])
# add lines indicating the onset position with spectra type and energy
bandgapAnalyzer.add_line('xes', 528.8)
bandgapAnalyzer.add_line('xas', 529.1)
# plot data with name of experimental and calculated XES graphs, and of experimental and calculated XAS graphs
bandgapAnalyzer.plot(['XES'], ['XES calc'], ['PFY'], ['XANES calc'])
```

Caclulate core hole shift through mathematical onset (!Warning: Might not be accurate!)
```py
# load undbroadend spectra for all sites using path, GS file, ES file, GS binding energy, GS and ES Fermi energy
bandgapAnalyzer.load_unbroadened(dir, 'Ti3O5_O1_GS_XAS.txspec', 'Ti3O5_O1_ES_XAS.txspec', 10, 3, 4)
bandgapAnalyzer.load_unbroadened(dir, 'Ti3O5_O2_GS_XAS.txspec', 'Ti3O5_O2_ES_XAS.txspec', 10, 3, 4)
bandgapAnalyzer.calc_core_hole_shift()
```


## Documentation

### DOSAnalyzer
Import the module
```py
# import DOSAnalyzer
from XPlotLib.DOSAnalyzer import DOSAnalyzer
```

#### load_dos
```py
"""
Load DOS of multiple atom files from directory with given regex and name (this can include multiple files .dos1, .dos2, ...)

Parameters
----------
dir : str
    Directory where DOS files are located
file_name : str
    File name without extension (this make loading dos from multiple files possible)
name : dict (string -> string)
    Name of the atoms and states (f.e. {'1': 'O1_ES', '2': 'O2_ES', ...})
binding_energies : dict (string -> float)
    Binding energies of each site in Ry (f.e. {'O1_ES': 10.0, 'O2_ES': 11.0, ...})
"""
load_dos(dir, file_name, names, binding_energies)
```

#### load_single_dos 
```py
"""
Load DOS of the same atom from directory with given regex and name (this can include multiple files .dos1, .dos2, ...)

Parameters
----------
dir : str
    Directory where DOS files are located
file_name : str
    File name without extension (this make loading dos from multiple files possible)
name : str
    Name of the atom and state (e.g. 'O1_ES')
E_Fermi : float
    Fermi energy in Ry
binding_Energy : float
    Binding energy in Ry
"""
load_single_dos(dir, file_name, name, binding_Energy)
```

#### load_spectrum
```py
"""
Load XES or XAS spectrum from file

Parameters
----------
path : str
    Path to the spectrum file
name : str
    Name of the spectrum
spec_type : str
    Type of the spectrum ("XES" or "XAS")
skiprows : int, optional
    Number of rows to skip in the file
delim : str, optional
    Delimiter of the file
shift : float, optional
    Energy shift of the spectrum in eV
"""
load_spectrum(path, name, spec_type, skiprows=1, delim=',', shift=0)
```


#### set_shift
```py
"""
Set energy shift for XES and XAS DOS (use same values used for broadening of the spectra)

Parameters
----------
xes_shift : float
    Energy shift for XES DOS in eV
xas_shift : float
    Energy shift for XAS DOS in eV
"""
set_shift(xes_shift, xas_shift)
```

#### set_title
```py
"""
Set title of the plot

Parameters
----------
title : str
    Title of the plot
"""
set_title(title)
```

#### set_figsize
```py
"""
Set figure size of the plot

Parameters
----------
width : int
    Width of the plot
"""
set_figsize(width, height):
```

#### set_custom_dos_scale
```py
"""
Set custom DOS scaling for XES and XAS

Parameters
----------
xes_scale : float
    Custom scaling for XES DOS
xas_scale : float
    Custom scaling for XAS DOS
"""
set_custom_dos_scale(xes_scale, xas_scale)
```

#### print_dos_options
```py
"""
Print all available DOS to choose from    
"""
print_dos_options()
```

#### set_active_dos
```py
"""
Set active DOS for plotting

Parameters
----------
xes_names : list of str, optional
    List of XES DOS names to plot
xas_names : list of str, optional
    List of XAS DOS names to plot
"""
set_active_dos(xes_names=[], xas_names=[])
```

#### set_staggered_spacing
```py
"""
Set staggered spacing between DOS

Parameters
----------
spacing : float
    Spacing between DOS
"""
set_staggered_spacing(spacing)
```

#### set_x_limits
```py
"""
Set x limits for XES and XAS DOS

Parameters
----------
xes_x_limits : tuple of float, optional
    X limits for XES DOS
xas_x_limits : tuple of float, optional
    X limits for XAS DOS
"""
set_x_limits(xes_x_limits=None, xas_x_limits=None)
```

#### plot_dos
```py
"""
Plot DOS with XES and XAS spectra

Parameters
----------
staggered : bool
    Staggered DOS
show_spectra : list of str, optional
    List of spectra to show ("XES" or "XAS"), default shows both
"""
plot_dos(staggered=False, show_spectra=['XES', 'XAS'])
```

#### export_dos
```py
 """
Export selected DOS to csv (individual files for XES and XAS)

Parameters
----------
path : str
    Path to the directory where to save the DOS
name : str
    Name of the DOS file
export_spectra : list of str, optional
    List of spectra to export ("XES" or "XAS"), default exports both
"""
export_dos( path, name, export_spectra=['XES', 'XAS'])
```

### BandgapAnalyzer
Import the module
```py
# import BandgapAnalyzer
from XPlotLib.BandgapAnalyzer import BandgapAnalyzer
```

#### load_exp_spectra
```py
"""
Load experimental spectra

Parameters
----------
path : str
    Path to the file containing the spectra
type : str
    Type of the spectra. Must be either 'xes' or 'xas'
names : list of str
    Names of the spectra
skiprows : int, optional
    Number of rows to skip in the beginning of the file
sep : str, optional
    Separator used in the file
"""
load_exp_spectra(path, type, names, skiprows=2, sep=',')
```

#### load_calc_spectra
```py
"""
Load calculated spectra

Parameters
----------
path : str
    Path to the file containing the spectra
type : str
    Type of the spectra. Must be either 'xes' or 'xas'
name : str
    Name of the spectra
skiprows : int
    Number of rows to skip in the beginning of the file
sep : str
    Separator used in the file
"""
load_calc_spectra(path, type, name, skiprows=1, sep=',')
```

#### smoothen
```py
"""
Smoothen the experimental spectra using a Savitzky-Golay filter. The smoothed data will shown in a plot with the option to show the onset region. The parameters set here will be used in the plot method.

Parameters
----------  
type : str
    Type of the spectra. Must be either 'xes' or 'xas'
name : str
    Name of the spectra
window : int
    Window length of datapoints. Must be odd and smaller than x
poly : int
    The order of polynom used. Must be smaller than the window size
onset_region : tuple of float, optional
    Tuple containing the start and end of the onset region
show : bool, optional 
    If True, the smoothed data will be plotted
"""
smoothen(type, name, window, poly, onset_region = None, show = True)
```

#### set_title
```py
"""
Set the title of the plot

Parameters
----------
title : str
    Title of the plot
"""
set_title(title)
```

#### set_figsize
```py
"""
Set the figure size of the plot

Parameters
----------
figsize : tuple of float
    Tuple containing the width and height of the figure
"""
set_figsize(figsize)
```

#### set_xlims
```py
"""
Set the x limits of the plot

Parameters
----------
xes_xlims : tuple of float
    Tuple containing the start and end of the x-axis for the XES spectra
xas_xlims : tuple of float
    Tuple containing the start and end of the x-axis for the XAS spectra
"""
set_xlims(xes_xlims, xas_xlims)
```

#### add_arrow
```py
"""
Add an arrow to annotate the last/first peak of the 2nd derivative of XES/XAS spectra

Parameters
----------
type : str
    Type of the spectra. Must be either 'xes' or 'xas'
xy : tuple of float
    Tuple containing the x and y coordinates of the peak
xytext : tuple of float
    Tuple containing the x and y coordinates of the text
text : str
    Text to be shown
text_rot : float, optional
    Rotation of the text
"""
add_arrow(type, xy, xytext, text, text_rot = 0)
```

#### add_line
```py
"""
Add a vertical line to the plot with energy label

Parameters
----------
type : str
    Type of the spectra. Must be either 'xes' or 'xas'
energy : float
    Energy of the line
linestyle : str, optional
    Linestyle of the line
color : str, optional
    Color of the line
linewidth : float, optional
    Width of the line
label : bool, optional
    If True, the energy will be shown as a label
xytext : tuple of float, optional
    Tuple containing the x and y coordinates of the label
"""

add_line(type, energy, linestyle='--', color='black', linewidth=1, label=True, xytext=None)
```

#### plot
```py
"""
Plot the spectra in four plots with the XES and XAS in the top row and their 2nd derivatives in the bottom row.

Parameters
----------
xes_exp_names : list of str
    Names of the experimental XES spectra
xes_calc_names : list of str
    Names of the calculated XES spectra
xas_exp_names : list of str
    Names of the experimental XAS spectra
xas_calc_names : list of str
    Names of the calculated XAS spectra
"""
plot(xes_exp_names, xes_calc_names, xas_exp_names, xas_calc_names)
```

#### export_2nd_derivative
```py
"""
Export 2nd derivative of XES and XAS spectra to csv files

Parameters
----------
path : str
    Path to the directory where the files will be saved
name : str
    Name of the files (without extension)
"""
export_2nd_derivative(path, name)
```

#### load_unbroadened
```py
"""
Load unbrodened spectra to determine core hole shift

Parameters
----------
dir : str
    Directory containing the spectra
GS_file : str
    File containing the ground state XAS spectrum
ES_file : str
    File containing the excited state XAS spectrum
GS_binding : float
    Binding energy of the ground state in Ry
GS_fermi : float
    Fermi energy of the ground state in Ry
ES_fermi : float
    Fermi energy of the excited state in Ry
"""
load_unbroadend(dir, GS_file, ES_file, GS_binding, GS_fermi, ES_fermi)
```

#### calc_core_hole_shift
```py
 """
Calculate the core hole shift using all previously loaded unbroadened spectra.
!Warning this might not be accurate!

Returns
-------
float
    Core hole shift in eV
"""
calc_core_hole_shift()
```