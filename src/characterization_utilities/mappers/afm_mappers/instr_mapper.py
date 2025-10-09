instr_mapper = {'name': 'name'}

sensor_mapper = {
    'attached_to': 'attached_to',
    'measurement': 'measurement',
    'model': 'model',
    'name': 'name',
}

positioner_mapper = {'name': 'name', 'description': 'description'}

spm_positioner_mapper = positioner_mapper.update({'set_point': 'set_point'})

piezomaterial_mapper = {'name': 'name', 'type': 'type'}

calibration_mapper = {
    'description': 'description',
    'physical_quantity': 'physical_quantity',
}

piezo_calibration_mapper = calibration_mapper.update(
    {
        'calibration_date': 'calibration_date',
        'calibration_type': 'calibration_type',
        'calibration_name': 'calibration_name',
    }
)

detector_mapper = {
    'detector_type': 'detector_type',
    'calibration_date': 'calibration_date',
}

cantilever_mapper = {
    'cantilever_shape': 'cantilever_shape',
    'cantilever_coating': 'cantilever_coating',
    'cantilever_resonance_frequency': 'cantilever_resonance_frequency',
}

oscillator_mapper = {'oscillator_excitation': 'oscillator_excitation'}

lockin_mapper = {'amplitude_excitation': 'amplitude_excitation'}
