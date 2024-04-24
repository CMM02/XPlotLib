from XPlotLib.BandgapAnalyzer import BandgapAnalyzer
from matplotlib.testing.decorators import image_comparison

base_dir = 'tests/BandgapAnalyzer/data/'

@image_comparison(baseline_images=['bandgap'], remove_text=True,
                  extensions=['png'], style='mpl20')
def test_plot_bandgap():
    bandgapAnalyzer = BandgapAnalyzer()
    bandgapAnalyzer.load_exp_spectra(f'{base_dir}Ti3O5_O_XES.csv', 'xes', ['XES'])
    bandgapAnalyzer.load_exp_spectra(f'{base_dir}Ti3O5_O_XAS.csv', 'xas', ['TEY', 'PFY'])
    bandgapAnalyzer.load_calc_spectra(f'{base_dir}Ti3O5-brd_O_XES.csv', 'xes', 'XES calc')
    bandgapAnalyzer.load_calc_spectra(f'{base_dir}Ti3O5-brd_O_XAS.csv', 'xas' , 'XAS calc')
    bandgapAnalyzer.load_calc_spectra(f'{base_dir}Ti3O5-brd_O_XANES.csv', 'xas', 'XANES calc')
    bandgapAnalyzer.set_title('Ti3O5 Bandgap Analysis')
    bandgapAnalyzer.smoothen('xes', 'XES', 15, 3, [526, 533], show=False)
    bandgapAnalyzer.smoothen('xas', 'TEY', 15, 3, [528, 530], show=False)
    bandgapAnalyzer.smoothen('xas', 'PFY', 15, 3, [528, 530], show=False)
    bandgapAnalyzer.set_xlims([515, 535], [520, 540])
    bandgapAnalyzer.add_arrow('xes', (528.8, 0.15), (531.8, 0.35), '528.8 eV')
    bandgapAnalyzer.add_arrow('xas', (529, 1.7), (526, 1.7), '529.1 eV')
    bandgapAnalyzer.plot(['XES'], ['XES calc'], ['PFY'], ['XANES calc'])
