from characterization_utilities.convert.em_convert.utils import (
    Matcher,
    SectionHeader,
)

meas_instrument = Matcher(
    SectionHeader(
        path='./instrument/', type_class='NXem_instrument', is_repeatable=False
    ),
    {'fields': {'name': {'alias': 'Make'}, 'type': {'get': (lambda x: 'fib')}}},
)
meas_instr_fabr = Matcher(
    SectionHeader(
        path='./instrument/fabrication/',
        type_class='NXfabrication',
        is_repeatable=False,
    ),
    {
        'fields': {
            'vendor': {'alias': 'Make'},
        }
    },
)
instr_program = Matcher(
    SectionHeader(
        path='./instrument/program', type_class='NXprogram', is_repeatable=False
    ),
    {
        'fields': {
            'program': {
                'alias': 'Software',
            }
        }
    },
)
event_instr_detector = Matcher(
    SectionHeader(
        path='./eventID/instrument/detector*/',
        type_class='NXdetector',
        is_repeatable=False,
    ),
    {
        'fields': {'name': {'alias': '60000.Detector'}},
    },
)
instr_ebeam = Matcher(
    SectionHeader(
        path='./instrument/ebeam_column',
        type_class='NXebeam_column',
        is_repeatable=False,
    ),
    {},
)
meas_event = Matcher(
    SectionHeader(path='./eventID/', type_class='NXem_event_data', is_repeatable=False),
    {},
)
event_instrument = Matcher(
    SectionHeader(
        path='./eventID/instrument', type_class='NXem_instrument', is_repeatable=False
    ),
    {},
)
event_instr_optics = Matcher(
    SectionHeader(
        path='./eventID/instrument/optics',
        type_class='NXem_optical_system',
        is_repeatable=False,
    ),
    {
        'fields': {
            'working_distance': {
                'alias': '60000.Focus/WD',
                'unit': 'm',
            },
            'probe_current': {
                'alias': '60000.ProbeCurrent',
                'unit': 'A',
            },
            'field_of_view': {
                'alias': '60000.FoV',
                'unit': 'm'
            },
        }
    },
)
event_instr_ebeam = Matcher(
    SectionHeader(
        path='./eventID/instrument/ebeam_column',
        type_class='NXebeam_column',
        is_repeatable=False,
    ),
    {
        'fields': {
            'operation_mode': {'alias': '60000.ActiveMode'},
        }
    },
)

event_instr_ebeam_scan = Matcher(
    SectionHeader(
        path='./eventID/instrument/ebeam_column/scan_controller',
        type_class='NXscan_controller',
        is_repeatable=False,
    ),
    {
        'fields': {
            'dwell_time': {
                'alias': '60000.PixelDwelltime',
                'unit': 's'
            }
        }
    },
)

event_instr_ebeam_source = Matcher(
    SectionHeader(
        path='./eventID/instrument/ebeam_column/electron_source/',
        type_class='NXsource',
        is_repeatable=False,
    ),
    {
        'fields': {
            'voltage': {'alias': '60000.AccVoltage', 'unit': 'V'},
        }
    },
)

matchers = [
    meas_instrument,
    meas_instr_fabr,
    event_instr_detector,
    instr_program,
    instr_ebeam,
    meas_event,
    event_instrument,
    event_instr_ebeam,
    event_instr_ebeam_scan,
    event_instr_ebeam_source,
    event_instr_optics,
]
