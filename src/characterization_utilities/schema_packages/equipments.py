# class FourPointProbe_System(CharactEquipmentBase, ArchiveSection):
#    m_def = Section(
#        a_eln={
#            'hide': [
#                'lab_id',
#                'datetime',
#            ],
#            'properties': {
#                'order': [
#                    'name',
#                    'lab_id',
#                    'description',
#                    'affiliation',
#                    'institution',
#                    'product_model',
#                    'manufacturer_name',
#                    'inventary_code',
#                    'is_bookable',
#                    'automatic_loading',
#                    'contamination_class',
#                    'notes',
#                    'measured_sheet_resistance_min',
#                    'measured_sheet_resistance_max',
#                    'measured_resistivity_min',
#                    'measured_resistivity_max',
#                    'current_source_min',
#                    'current_source_max',
#                    'probe_head_pin_spacing',
#                    'probe_head_pin_load',
#                    'probe_head_pin_radius',
#                    'needles_composition',
#                    'needles_radius',
#                ],
#            },
#        }
#    )
#    measured_sheet_resistance_min = Quantity(
#        type=np.float64,
#        description='minimum mesaurable sheet resistence',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='Ohm/sq',
#    )
#    measured_sheet_resistance_max = Quantity(
#        type=np.float64,
#        description='maximum mesaurable sheet resistence',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='Ohm/sq',
#    )
#    measured_resistivity_min = Quantity(
#        type=np.float64,
#        description='minimum mesaurable resistivity',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='Ohm*cm',
#    )
#    measured_resistivity_max = Quantity(
#        type=np.float64,
#        description='maximinimum mesaurable resistivity',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='Ohm*cm',
#    )
#    current_source_min = Quantity(
#        type=np.float64,
#        description='minimum applied current',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        unit='A',
#    )
#    current_source_max = Quantity(
#        type=np.float64,
#        description='maximum applied current',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        unit='A',
#    )
#    probe_head_pin_spacing = Quantity(
#        type=np.float64,
#        description='distance among needles',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='mils',
#    )
#    probe_head_pin_load_min = Quantity(
#        type=np.float64,
#        description='minumum applied pin load',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='g',
#    )
#    probe_head_pin_load_max = Quantity(
#        type=np.float64,
#        description='maximum applied pin load',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        # unit='g',
#    )
#    needles_composition = Quantity(
#        type=str,
#        description='needle materials',
#        a_eln={
#            'component': 'StringEditQuantity',
#        },
#    )
#    needles_radius = Quantity(
#        type=np.float64,
#        description='needle tip diameter',
#        a_eln={
#            'component': 'NumberEditQuantity',
#        },
#        unit='mm',
#    )
#
