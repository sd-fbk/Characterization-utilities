from characterization_utilities.mappers.em_mappers.entry_mapper import mapper as emapper
from characterization_utilities.mappers.em_mappers.sample_mapper import (
    comp_mapper as cmapper,
)
from characterization_utilities.mappers.em_mappers.sample_mapper import (
    smapper,
)
from characterization_utilities.mappers.em_mappers.user_mapper import mapper as umapper

__all__ = ['emapper', 'umapper', 'smapper', 'cmapper']

mapperManager = {
    'Entry': {'mapper': emapper},
    'User': {'NX_class': 'NXuser', 'name': 'user', 'mapper': umapper},
    'Sample': {'NX_class': 'NXsample', 'name': 'sample', 'mapper': smapper},
    'SampleComponent': {'NX_class': 'NXsample_component', 'mapper': cmapper},
    'History': {'NX_class': 'NXhistory', 'mapper': {'lab_id': 'identifierNAME'}},
    'ActivityStep': {
        'NX_class': 'NXactivity',
        'mapper': {'description': 'description', 'start_time': 'start_time'},
    },
}
