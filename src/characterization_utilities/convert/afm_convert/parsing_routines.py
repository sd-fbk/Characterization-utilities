import h5py
import numpy as np


def xyz_parser(xyz_file):
    dati = np.loadtxt(xyz_file)
    return dati


def afm_data_parser(output_file, data_file, measured):
    with h5py.File(output_file, 'a') as f:
        entry = f['entry']
        data = entry.create_group('data')
        data.attrs['NX_class'] = 'NXdata'
        data.attrs['signal'] = 'z'
        data.attrs['axes'] = ['x', 'y']
        dati = xyz_parser(data_file)
        x, y, z = dati[:, 0], dati[:, 1], dati[:, 2]
        data.create_dataset('x', data=x)
        data['x'].attrs['units'] = 'm'
        data.create_dataset('y', data=y)
        data['y'].attrs['units'] = 'm'
        data.create_dataset('z', data=z)
        if measured == 'height':
            data['z'].attrs['units'] = 'm'
        elif measured == 'phase':
            data['z'].attrs['units'] = 'deg'
        data.create_dataset('title', data='Title for plot')
