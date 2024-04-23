from XPlotLib.DOSAnalyzer import DOSAnalyzer
import pandas as pd
import pytest
import filecmp
from matplotlib.testing.decorators import image_comparison

base_dir = 'tests/DOSAnalyzer/'


def load_dos(dosAnalyzer):
    dir = base_dir + 'data/'
    sites = {'4': 'O1', '5': 'O2', '6': 'O3', '7': 'O4','8': 'O5'}
    binding_energies = {}
    calc_energies = pd.read_csv(f'{dir}Ti3O5_calculation_energies.csv', index_col=0)
    for atom in sites.values():
        binding_energies[atom] = calc_energies.filter(like=atom, axis=0)['GS_bindingEnergy'].values[0]

    dosAnalyzer.set_shift(22.5, 22)

     #load GS data
    GS_names = sites.copy()
    for site, site_name in sites.items():
        GS_names[site] = f'{site_name}_GS'
    dosAnalyzer.load_dos(dir, f'Ti3O5_DOS_O_GS', GS_names, binding_energies)
    # load ES data
    for site_name in sites.values():
        dosAnalyzer.load_single_dos(dir, f'Ti3O5_DOS_{site_name}_ES', f'{site_name}_ES', binding_energies[site_name])
    # # load broadened spectra
    dosAnalyzer.load_spectrum(f'{dir}Ti3O5-brd_O_XES.csv', name=f'Ti3O5 calc XES', spec_type='XES')
    dosAnalyzer.load_spectrum(f'{dir}Ti3O5-brd_O_XANES.csv', name=f'Ti3O5 calc XAS', spec_type='XAS')
    # # load measurements
    dosAnalyzer.load_spectrum(f'{dir}Ti3O5_O_XES.csv', name=f'Ti3O5 exp XES', spec_type='XES', skiprows=2)
    dosAnalyzer.load_spectrum(f'{dir}Ti3O5_O_XAS.csv', name=f'Ti3O5 exp XAS', spec_type='XAS', skiprows=2)

def test_load_dos(capfd):
    dosAnlyzer = DOSAnalyzer()
    load_dos(dosAnlyzer)
    expected = """DOS to choose from:\nO1_GS_s\nO1_GS_p\nO1_GS_PX\nO1_GS_PY\nO1_GS_PZ\nO2_GS_s\nO2_GS_p\nO2_GS_PX\nO2_GS_PY\nO2_GS_PZ\nO3_GS_s\nO3_GS_p\nO3_GS_PX\nO3_GS_PY\nO3_GS_PZ\nO4_GS_s\nO4_GS_p\nO4_GS_PX\nO4_GS_PY\nO4_GS_PZ\nO5_GS_s\nO5_GS_p\nO5_GS_PX\nO5_GS_PY\nO5_GS_PZ\nO1_ES_s\nO1_ES_p\nO1_ES_PX\nO1_ES_PY\nO1_ES_PZ\nO2_ES_s\nO2_ES_p\nO2_ES_PX\nO2_ES_PY\nO2_ES_PZ\nO3_ES_s\nO3_ES_p\nO3_ES_PX\nO3_ES_PY\nO3_ES_PZ\nO4_ES_s\nO4_ES_p\nO4_ES_PX\nO4_ES_PY\nO4_ES_PZ\nO5_ES_s\nO5_ES_p\nO5_ES_PX\nO5_ES_PY\nO5_ES_PZ\n"""
    dosAnlyzer.print_dos_options()
    out, err = capfd.readouterr()    
    assert out == expected

def configure_dos(dosAnalyzer):
    load_dos(dosAnalyzer)
    dosAnalyzer.set_active_dos(xes_names=['O1_GS_p', 'O2_GS_p', 'O3_GS_p', 'O4_GS_p', 'O5_GS_p'], xas_names=['O1_ES_p', 'O2_ES_p', 'O3_ES_p', 'O4_ES_p', 'O5_ES_p'])
    dosAnalyzer.set_custom_dos_scale(1.5, 1.5)
    dosAnalyzer.set_title('Ti3O5 DOS Analysis') 


@image_comparison(baseline_images=['normal_dos'], remove_text=True,
                  extensions=['png'], style='mpl20')
def test_plot_dos():
    dosAnalyzer = DOSAnalyzer()
    configure_dos(dosAnalyzer)
    dosAnalyzer.plot_dos()

@image_comparison(baseline_images=['staggerd_dos'], remove_text=True,
                  extensions=['png'], style='mpl20')
def test_plot_dos_staggered():
    dosAnalyzer = DOSAnalyzer()
    configure_dos(dosAnalyzer)
    dosAnalyzer.plot_dos(staggered=True)

def test_export_dos():
    dosAnalyzer = DOSAnalyzer()
    configure_dos(dosAnalyzer)
    dosAnalyzer.export_dos(f'{base_dir}actual/', 'Ti3O5_DOS_Analysis')
    assert filecmp.cmp(f'{base_dir}expected/Ti3O5_DOS_Analysis_XAS.csv', f'{base_dir}actual/Ti3O5_DOS_Analysis_XAS.csv')
    assert filecmp.cmp(f'{base_dir}expected/Ti3O5_DOS_Analysis_XES.csv', f'{base_dir}actual/Ti3O5_DOS_Analysis_XES.csv')
