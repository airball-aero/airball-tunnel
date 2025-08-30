from common.calibration import Calibration
from common.sweep import read_channels
from common.plotter import Plotter

(s01d, _) = read_channels('../data/c01_10.csv',
                          '../data/esp32_scanner.cal')
(s03d, _) = read_channels('../data/c03_10.csv',
                          '../data/esp32_scanner.cal')

p = Plotter()
p.add_data(s01d.asymmetry(), 6)
p.add_data(s03d.asymmetry(), 6)

p.show()
