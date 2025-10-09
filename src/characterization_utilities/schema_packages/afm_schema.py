import os
from typing import (
    TYPE_CHECKING,
)

import numpy as np

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )


from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Datetime, MEnum, Package, Quantity, Section, SubSection

from characterization_utilities.convert.afm_convert.parsing_routines import (
    afm_data_parser,
)
from characterization_utilities.convert.common import instanciate_nexus
from characterization_utilities.schema_packages.character import (
    CharactEquipment,
    CharacterizationStep,
    Samplebase,
    SampleComponentbase,
)
from characterization_utilities.schema_packages.dataconverter import (
    CharacterizationStepConverter,
)

m_package = Package(name='Classes to define an ELN for AFM steps')


class SampleComponent(SampleComponentbase):
    m_def = Section(
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'description',
                    'chemical_formula',
                    'datetime',
                    'component_id',
                    'datetime',
                ],
            },
        }
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class Sample(Samplebase):
    m_def = Section(
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'description',
                    'chemical_formula',
                    'lab_id',
                    'datetime',
                    'id_wafer_parent',
                    'shapeType',
                    'is_simulation',
                    'type',
                    'physical_form',
                    'situation',
                    'atom_types',
                    'notes',
                ],
            },
        }
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


# LO strumento non è detto che si debba definire sempre, dipende dai casi, ad esempio
# nel sem non lo abbiamo messo perché i suoi dati erano già nei tiff. Inoltre per gli
# strumenti di caratterizzazione non ho definito capabilities perché è molto più
# rilevante e NeXus richiede questo definire i parametri relativi allo step.


class Calibration(ArchiveSection):
    m_def = Section()

    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )

    physical_quantity = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})


class Positioner(ArchiveSection):
    m_def = Section()

    name = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})

    description = Quantity(type=str, a_eln={'component': 'RichTextEditQuantity'})


class Positioner_spm(Positioner):
    m_def = Section()

    set_point = Quantity(
        type=np.float64,
        description='force applied to the tip',
        a_eln={
            'component': 'NumberEditQuantity',
        },
        unit='A',
    )


class Lockin(ArchiveSection):
    m_def = Section()

    amplitude_excitation = Quantity(
        type=np.float64,
        description="""
        The reference amplitude (also called driver amplitude) of the cantilever.
        Here, the amplitude excitation voltage may be the same as the oscillator
        excitation voltage.
        """,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'V'},
        unit='V',
    )

    cantilever_phase_positioner = SubSection(
        section_def=Positioner,
        description='The phase positioner of the cantilever.',
        repeats=False,
    )

    cantilever_amplitude_positioner = SubSection(
        section_def=Positioner,
        description='The amplitude positioner of the cantilever.',
        repeats=False,
    )

    cantilever_frequency_positioner = SubSection(
        section_def=Positioner,
        description='The frequency positioner of the cantilever.',
        repeats=False,
    )


class Oscillator(ArchiveSection):
    m_def = Section()

    oscillator_excitation = Quantity(
        type=np.float64,
        description="""
        Oscillator excitation also referred as driving voltage for excitation of
        cantilever oscillator. This excitation may initially set the amplitude,
        frequency, or phase of the cantilever oscillation depending on the experiment
        condition.        
        """,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'V'},
        unit='V',
    )

    phase_lock_loop = SubSection(section_def=Lockin, repeats=False)


class Cantilever(ArchiveSection):
    m_def = Section()

    cantilever_shape = Quantity(
        type=str,
        description='the model of the cantilever',
        a_eln={
            'component': 'StringEditQuantity',
        },
    )
    cantilever_coating = Quantity(
        type=str,
        description='the material of the probing tip',
        a_eln={
            'component': 'StringEditQuantity',
        },
    )
    cantilever_resonance_frequency = Quantity(
        type=np.float64,
        description="""
        Nominal free resonance frequency of the cantilever in air, in kHz.
        """,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'kHz'},
        unit='kHz',
    )

    cantilever_oscillator = SubSection(section_def=Oscillator, repeats=False)


class Detector(ArchiveSection):
    m_def = Section()

    detector_type = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})

    calibration_date = Quantity(
        type=Datetime, a_eln={'component': 'DateTimeEditQuantity'}
    )


class Sensor(ArchiveSection):
    m_def = Section()

    attached_to = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})
    measurement = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})
    model = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})
    name = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})


class PiezoMaterial(ArchiveSection):
    m_def = Section()

    name = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})
    type = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})


class PiezoCalibration(Calibration):
    m_def = Section()

    calibration_name = Quantity(type=str, a_eln={'component': 'StringEditQuantity'})

    calibration_type = Quantity(
        type=MEnum('active', 'passive'), a_eln={'component': 'EnumEditQuantity'}
    )

    calibration_date = Quantity(
        type=Datetime, a_eln={'component': 'DateTimeEditQuantity'}
    )


class PiezoConfig(ArchiveSection):
    m_def = Section()

    piezo_material = SubSection(section_def=PiezoMaterial, repeats=False)

    calibration = SubSection(section_def=PiezoCalibration, repeats=False)


class PiezoSensor(Sensor):
    m_def = Section()

    piezo_configuration = SubSection(section_def=PiezoConfig, repeats=False)

    positioner_spm = SubSection(section_def=Positioner_spm, repeats=False)


class AFMSystem(CharactEquipment):
    m_def = Section(
        a_eln={
            'hide': [
                'datetime',
            ],
            'properties': {
                'order': [
                    'name',
                    'lab_id',
                    'description',
                    'affiliation',
                    'institution',
                    'product_model',
                    'manufacturer_name',
                    'inventary_code',
                    'is_bookable',
                    'automatic_loading',
                    'contamination_class',
                    'notes',
                    'afm_tip',
                    'afm_mode',
                    'afm_setpoint',
                ],
            },
        }
    )

    cantilever = SubSection(section_def=Cantilever, repeats=False)

    photo_detector = SubSection(section_def=Detector, repeats=False)

    XY_piezo_sensor = SubSection(section_def=PiezoSensor, repeats=False)

    height_piezo_sensor = SubSection(section_def=PiezoSensor, repeats=False)

    tip_temp_sensor = SubSection(section_def=Sensor, repeats=False)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class AFMStepConverter(CharacterizationStep, CharacterizationStepConverter):
    m_def = Section(
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'step_id',
                    'description',
                    'affiliation',
                    'location',
                    'institution',
                    'facility',
                    'laboratory',
                    'id_item_processed',
                    'starting_date',
                    'ending_date',
                    'step_type',
                    'definition_of_process_step',
                    'afm_mode',
                    'nxdl',
                    'input_data_files',
                    'output',
                    'export',
                    'nexus_view',
                    'notes',
                ]
            },
        },
    )

    afm_mode = Quantity(
        type=MEnum(
            'contact mode',
            'tapping mode',
            'non-contact mode',
            'Kelvin probe',
            'electric force',
            'lateral force mode',
        ),
        description='if proxy or in contact, if linear or scanning',
        a_eln={
            'component': 'EnumEditQuantity',
        },
    )
    #    afm_tip = Quantity(
    #        type=str,
    #        description='the model of the probing tip',
    #        a_eln={
    #            'component': 'StringEditQuantity',
    #        },
    #    )
    #    afm_fb_gain = Quantity(
    #        type=np.float64,
    #        description='piezoelectric parameter',
    #        a_eln={
    #            'component': 'NumberEditQuantity',
    #        },
    #        unit='nm',
    #    )
    #    afm_tip_resonance = Quantity(
    #        type=np.float64,
    #        description='tip calibration parameter',
    #        a_eln={
    #            'component': 'NumberEditQuantity',
    #        },
    #        unit='MHz',
    #    )

    #    PENSO CHE LA TIP RESONANCE SIA LA CANTILEVER RESONANCE FREQUENCY VEDI

    #    afm_tip_phase = Quantity(
    #        type=np.float64,
    #        description='tip calibration parameter',
    #        a_eln={
    #            'component': 'NumberEditQuantity',
    #        },
    #        unit='nm',
    #    )
    #    afm_laser_intensity = Quantity(
    #        type=np.float64,
    #        description='the laser source hitting the photodiode',
    #        a_eln={
    #            'component': 'NumberEditQuantity',
    #        },
    #        unit='mA',
    #    )
    #    Questi parametri non so dove collocarli nello schema perché non trovo la sua
    #    posizione in NeXus. Inoltre controllare l'unità di misura perché un'intensità è
    #    un'energia su area fratto tempo e non una corrente. In caso cambiare nome.
    #    Comunque la classe potrebbe subire modifiche dato che il gruppo NeXus per gli
    #    scanning probe microscopy dovrebbe subire modifiche in futuro.

    #    afm_fb_gain_o = Quantity(
    #        type=np.float64,
    #        description='tip parameter',
    #        a_eln={
    #            'component': 'NumberEditQuantity',
    #        },
    #        unit='nm',
    #    )
    #    Verificare se questo parametro è del positioner_spm e viene chiamato da nexus
    #    come tip_lift con descrizione "If the tip is lifted from the stable point".
    #    In quel caso aggiungerlo nella classe del Positioner_spm

    # Quando i parametri verranno collocati correttamente inserire poi il mapping dei
    # nomi da quelli dati in questo schema al nexus per poterli convertire verso nexus.

    samples = SubSection(section_def=Sample, repeats=True)
    instrument = SubSection(section_def=AFMSystem, repeats=False)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        files_list = self.input_data_files
        raw_path = archive.m_context.raw_path()

        if self.output:
            output_file = os.path.join(raw_path, self.output)
            if self.nxdl:
                # list_dict = archive.data.__dict__
                instanciate_nexus(output_file, archive.data, self.nxdl, logger)
                if files_list is not None and len(files_list) > 0:
                    for file in files_list:
                        afm_data_parser(
                            output_file, os.path.join(raw_path, file), 'phase'
                        )
                try:
                    archive.m_context.process_updated_raw_file(
                        self.output, allow_modify=True
                    )
                except Exception as e:
                    logger.error(
                        'could not trigger processing', mainfile=self.output, exc_info=e
                    )
                else:
                    logger.info('triggered processing', mainfile=self.output)
                self.nexus_view = f'../upload/archive/mainfile/{self.output}#/data'


m_package.__init_metainfo__()
