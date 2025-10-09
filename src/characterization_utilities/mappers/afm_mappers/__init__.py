from characterization_utilities.mappers.afm_mappers.entry_mapper import (
    mapper as emapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    cantilever_mapper as cspmmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    detector_mapper as dmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    instr_mapper as imapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    lockin_mapper as lmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    oscillator_mapper as omapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    piezo_calibration_mapper as pcalmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    piezomaterial_mapper as pmatmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    positioner_mapper as posmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    sensor_mapper as sensmapper,
)
from characterization_utilities.mappers.afm_mappers.instr_mapper import (
    spm_positioner_mapper as spmposmapper,
)
from characterization_utilities.mappers.afm_mappers.sample_mapper import (
    comp_mapper as cmapper,
)
from characterization_utilities.mappers.afm_mappers.sample_mapper import (
    sample_mapper as smapper,
)
from characterization_utilities.mappers.afm_mappers.user_mapper import (
    mapper as umapper,
)

__all__ = ['emapper', 'umapper', 'smapper', 'cmapper']

mapperManager = {
    'Entry': {'mapper': emapper},
    'User': {'NX_class': 'NXuser', 'name': 'user', 'mapper': umapper},
    'Sample': {'NX_class': 'NXsample', 'name': 'sample', 'mapper': smapper},
    'SampleComponent': {'NX_class': 'NXsample_component', 'mapper': cmapper},
    'History': {'NX_class': 'NXhistory', 'mapper': {'identifierNAME': 'lab_id'}},
    'ActivityStep': {
        'NX_class': 'NXactivity',
        'mapper': {'description': 'description', 'start_time': 'start_time'},
    },
    'AFMSystem': {'NX_class': 'NXinstrument', 'mapper': imapper},
    'Sensor': {'NX_class': 'NXsensor', 'mapper': sensmapper},
    'PiezoSensor': {'NX_class': 'NXsensor', 'mapper': sensmapper},
    'PiezoConfig': {'NX_class': 'NXpiezo_config_spm'},
    'Positioner': {'NX_class': 'NXpositioner', 'mapper': posmapper},
    'Positioner_spm': {'NX_class': 'NXpositioner_spm', 'mapper': spmposmapper},
    'PiezoMaterial': {'NX_class': 'NXpiezoelectric_material', 'mapper': pmatmapper},
    'PiezoCalibration': {'NX_class': 'NXcalibration', 'mapper': pcalmapper},
    'Detector': {'NX_class': 'NXdetector', 'mapper': dmapper},
    'Cantilever': {'NX_class': 'NXcantilever_spm', 'mapper': cspmmapper},
    'Oscillator': {'NX_class': 'NXcomponent', 'mapper': omapper},
    'Lockin': {'NX_class': 'NXlockin', 'mapper': lmapper},
}
