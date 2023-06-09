import copy
import functools
import json
import logging
from collections import defaultdict
from multiprocessing import Pool
from tempfile import NamedTemporaryFile
from pathlib import Path
from openff.qcsubmit.results import (
    OptimizationResultCollection, TorsionDriveResultCollection,
)
from openff.qcsubmit.results.filters import (
    ConformerRMSDFilter, ConnectivityFilter,
    ElementFilter,
    HydrogenBondFilter,
    RecordStatusFilter,
    ResultRecordFilter,
)
from openff.toolkit.typing.engines.smirnoff import ForceField
from openff.toolkit.utils import UndefinedStereochemistryError
from qcportal import FractalClient
from qcportal.models import TorsionDriveRecord
from qcportal.models.records import RecordStatusEnum
from tqdm import tqdm


class UndefinedStereoFilter(ResultRecordFilter):
    def _filter_function(self, result, record, molecule) -> bool:

        has_stereochemistry = True

        molecule = copy.deepcopy(molecule)
        molecule._conformers = [molecule.conformers[0]]

        try:

            with NamedTemporaryFile(suffix=".sdf") as file:
                molecule.to_file(file.name, "SDF")
                molecule.from_file(file.name)

        except UndefinedStereochemistryError:
            has_stereochemistry = False

        return has_stereochemistry


def label_ids(record_and_molecule, force_field, parameter_types):
    record, molecule = record_and_molecule

    full_labels = force_field.label_molecules(molecule.to_topology())[0]

    parameter_ids = set()

    for parameter_type in parameter_types:

        parameter_labels = full_labels[parameter_type]

        for indices, parameter in parameter_labels.items():

            if isinstance(record, TorsionDriveRecord) and {*indices[1:3]} != {
                *record.keywords.dihedrals[0][1:3]
            }:
                continue

            parameter_ids.add(parameter.id)

    return [*parameter_ids]


def select_parameters(training_set, parameter_types, output_path, force_field):
    # Print out coverage information.
    coverage = defaultdict(int)

    with Pool(8) as pool:

        for parameter_ids in tqdm(
                pool.imap(
                    functools.partial(
                        label_ids, force_field=force_field, parameter_types=parameter_types
                    ),
                    training_set.to_records(),
                ),
                total=training_set.n_results,
        ):

            for parameter_id in parameter_ids:
                coverage[parameter_id] += 1

    # Save out the SMIRKS which should be trained against this set.
    with open(output_path, "w") as file:

        selected_parameters = defaultdict(list)

        for parameter_type in parameter_types:

            for parameter_id, count in coverage.items():

                found_parameters = force_field.get_parameter_handler(
                    parameter_type
                ).get_parameter({"id": parameter_id})

                if count < 5 or len(found_parameters) == 0:
                    continue

                selected_parameters[parameter_type].append(found_parameters[0].smirks)

        json.dump(selected_parameters, file)


def main():
    logging.basicConfig(level=logging.INFO)
    Path("./data-sets").mkdir(parents=True, exist_ok=True)

    initial_forcefield = ForceField('force-field_7.offxml', load_plugins=True, allow_cosmetic_attributes=True)

    default_filters = [
        RecordStatusFilter(status=RecordStatusEnum.complete),
        ConnectivityFilter(tolerance=1.2),
        UndefinedStereoFilter(),
        ElementFilter(
            # The elements supported by SMIRNOFF
            allowed_elements=["H", "C", "N", "O", "Cl", "Br"]
        ),
    ]

    # Pull down the main torsion drive and optimization sets and filter out any records
    # which have not completed or which inadvertently contain intra-molecular h-bonds.
    client = FractalClient()

    torsion_set = TorsionDriveResultCollection.from_server(
        client=client,
        datasets=[
            "OpenFF Gen 2 Torsion Set 1 Roche 2",
            "OpenFF Gen 2 Torsion Set 2 Coverage 2",
            "OpenFF Gen 2 Torsion Set 3 Pfizer Discrepancy 2",
            "OpenFF Gen 2 Torsion Set 4 eMolecules Discrepancy 2",
            "OpenFF Gen 2 Torsion Set 5 Bayer 2",
            "OpenFF Gen 2 Torsion Set 6 supplemental 2",
            "OpenFF Amide Torsion Set v1.0"
        ],
        spec_name="default",
    )

    # Drop record ids with inconsistent optimization histories or which cause failures
    # in ForceBalance.
    torsion_set.entries[client.address] = [
        entry
        for entry in torsion_set.entries[client.address]
        if entry.record_id
           not in [
               "6098580",
               "2703504",
               "2703505",
               "18045478",
           ]
    ]

    torsion_set = torsion_set.filter(
        HydrogenBondFilter(method="baker-hubbard"), *default_filters
    )

    with open("data-sets/reduced-set-td-set.json", "w") as file:
        file.write(torsion_set.json())

    select_parameters(
        torsion_set,
        parameter_types=["ProperTorsions"],
        output_path="data-sets/reduced-set-proper-torsions-params-smirks.json",
        force_field=initial_forcefield
    )

    optimization_set = OptimizationResultCollection.from_server(
        client=FractalClient(),
        datasets=[
            "OpenFF Gen 2 Opt Set 1 Roche",
            "OpenFF Gen 2 Opt Set 2 Coverage",
            "OpenFF Gen 2 Opt Set 3 Pfizer Discrepancy",
            "OpenFF Gen 2 Opt Set 4 eMolecules Discrepancy",
            "OpenFF Gen 2 Opt Set 5 Bayer",
        ],
        spec_name="default",
    )

    optimization_set = optimization_set.filter(
        ConformerRMSDFilter(max_conformers=10),
        *default_filters,

    )

    with open("data-sets/reduced-set-opt-set.json", "w") as file:
        file.write(optimization_set.json())

    select_parameters(
        optimization_set,
        parameter_types=["Angles"],
        output_path="data-sets/reduced-set-angles-params-smirks.json",
        force_field=initial_forcefield,
    )
    
    select_parameters(
        optimization_set,
        parameter_types=["Bonds"],
        output_path="data-sets/reduced-set-bonds-params-smirks.json",
        force_field=initial_forcefield,
    )


if __name__ == "__main__":
    main()
