#######################################################################################
#         FILE CON FUNZIONI UTILI NELLA GENERAZIONE DEI FILE NEXUS A PARTIRE          #
#               DA DIZIONARI O PER PARSARE GLI ARCHIVI DA CUI SI PARTE                #
#######################################################################################

from datetime import datetime

import h5py

from characterization_utilities.mappers import load_mapper_manager

# Definizione utile per la scritture dei datetimes

dt = h5py.string_dtype(encoding='utf-8')


# La prossima funzione ci permette di generare i gruppi dei nostri file hdf5.


def create_group_to_fill(TYPE, where, name):
    group = where.create_group(name)
    group.attrs['NX_class'] = TYPE
    return group


# Adesso che sappiamo generare i gruppi possiamo in teoria preoccuparci di scrivere
# le quantità in questi gruppi. Prima però le prossima funzione sarà utile per estrarre
# dall'archivio le quantità con il loro valore e l'unità di misura relativa.


def extract_values_with_units(section):
    results = {}
    for name, qdef in section.m_def.all_quantities.items():
        if section.m_is_set(name):
            results[name] = {
                'value': section.m_get(name),
                'unit': getattr(qdef, 'unit', None),
            }
    return results


# Questa funzione ci permette di scrivere correttamente i dati dalla struttura ad
# archivio di nomad alla struttura nexus. Quindi fondamentalmente è il building block
# con cui gli ELNs vengono tradotti in dati nexus. Potremmo avere quantità stringa
# che vengono lette e scritte come dataset del gruppo (facendo solo attenzione al tipo,
# perché le date richiedono una precisa formattazione e ciò che viene da campi RichText
# ha una formattazione html). I valori numerici senza unità di misura possono essere
# trattati come le stringhe. Abbiamo poi la possibilità di avere grandezze scalari con
# unità di misura, oppure grandezze vettoriali (simili alle scalari ma con un versore
# direzione associato). Ci sono delle quantità che iniziano con m_ che non vogiamo né
# mappare né accedere ai valori altrimenti avremmo gravi bugs sul nostro NOMAD. Infine,
# ci potrebbero essere delle sezioni che dobbiamo mappare a sezioni NeXus e in quel
# caso una volta ottenuto il tipo lo usiamo per ottenere la classe NeXus corrispondente
# dal mapper menager e richiamare la giusta routine di mapping.


def write_data(data_archive, where, mapper: dict, MM: dict, logger) -> None:
    vals = extract_values_with_units(data_archive)
    for k, v in vals.items():
        val = v['value']
        unit = v['unit']
        if k in mapper:
            if isinstance(val, datetime):
                val = str(val)
                where.create_dataset(mapper[k], data=val, dtype=dt)
            elif isinstance(val, str) and ('<p>' in val or '</p>' in val):
                val = val.replace('<p>', '').replace('</p>', '')
                where.create_dataset(mapper[k], data=val)
            else:
                where.create_dataset(mapper[k], data=val)
                if unit is not None:
                    where[mapper[k]].attrs['units'] = str(unit)
    for name, sub_def in data_archive.m_def.all_sub_sections.items():
        subsections = data_archive.m_get_sub_sections(sub_def)
        if not subsections:
            continue

        cls_name = sub_def.sub_section.section_cls.__name__
        if cls_name not in MM.keys():
            continue

        sub_mapper = MM[cls_name]['mapper']
        partial_name = MM[cls_name].get('name', None)
        nx_class = MM[cls_name].get('NX_class', None)

        for i, sub in enumerate(subsections):
            if sub is None:
                continue
            subgrp = create_group_to_fill(
                nx_class, where, f'{partial_name}_{i}' if partial_name else name
            )
            write_data(sub, subgrp, sub_mapper, MM, logger)


# Funzione che richiama la precedente e che crea davvero il nexus generandone l'entry.


def instanciate_nexus(output_file, data_archive, nxdl: str, logger) -> None:
    # carico il manager giusto
    MM = load_mapper_manager(nxdl)
    # l’entry mapper lo prendo dal manager
    # supponendo che tu abbia sempre una voce "Entry" o simile
    entry_mapper = MM.get('Entry', {}).get('mapper', None)
    if entry_mapper is None:
        raise RuntimeError(f'Nessun entry mapper definito per {nxdl}')
    with h5py.File(output_file, 'w') as f:
        entry = f.create_group('entry')
        entry.attrs['NX_class'] = 'NXentry'
        entry.create_dataset('definition', data=nxdl)
        if data_archive is not None:
            write_data(data_archive, entry, entry_mapper, MM, logger)


# Supporto quantità vettoriali rimosso da rivedere
