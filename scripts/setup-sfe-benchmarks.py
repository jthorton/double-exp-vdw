import os.path
from glob import glob

from absolv.models import (
    EquilibriumProtocol,
    SimulationProtocol,
    State,
    System,
    TransferFreeEnergySchema,
)
from nonbonded.library.models.datasets import DataSet
from openff.toolkit.typing.engines.smirnoff import ForceField
from openmm import unit
from tqdm import tqdm


def main():

    data_sets = [
        DataSet.parse_file(
            os.path.join(
                "..",
                "data-set-curation",
                "physical-property",
                "benchmarks",
                "sage-fsolv-test-v1.json",
            )
        ),
        DataSet.parse_file(
            os.path.join(
                "..",
                "data-set-curation",
                "physical-property",
                "benchmarks",
                "sage-mnsol-test-v1.json",
            )
        ),
    ]
    schemas = []

    for entry in (entry for data_set in data_sets for entry in data_set.entries):

        solute = [
            component.smiles
            for component in entry.components
            if component.role == "Solute"
        ][0]
        solvent = [
            component.smiles
            for component in entry.components
            if component.role == "Solvent"
        ][0]

        schema = TransferFreeEnergySchema(
            system=System(
                solutes={solute: 1}, solvent_a=None, solvent_b={solvent: 1000}
            ),
            state=State(
                temperature=298.15 * unit.kelvin, pressure=1.0 * unit.atmosphere
            ),
            alchemical_protocol_a=EquilibriumProtocol(
                lambda_sterics=[1.0, 1.0, 1.0, 1.0, 1.0],
                lambda_electrostatics=[1.0, 0.75, 0.5, 0.25, 0.0],
                sampler="repex",
                production_protocol=SimulationProtocol(
                    n_steps_per_iteration=500, n_iterations=2000
                ),
            ),
            alchemical_protocol_b=EquilibriumProtocol(
                lambda_sterics=[
                    1.00, 1.00, 1.00, 1.00, 1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50,
                    0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.00,
                ],
                lambda_electrostatics=[
                    1.00, 0.75, 0.50, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                ],
                sampler="repex",
                production_protocol=SimulationProtocol(
                    n_steps_per_iteration=500, n_iterations=2000
                ),
            ),
        )
        schemas.append(schema)

    force_field_paths = glob(
        os.path.join(
            "..",
            "inputs-and-results",
            "optimizations",
            "*",
            "result",
            "optimize",
            "force-field.offxml",
        )
    )

    for force_field_path in tqdm(force_field_paths, desc="force field"):

        root_name = force_field_path.split(os.sep)[-4]
        root_path = os.path.join(
            "..",
            "inputs-and-results",
            "benchmarks",
            "transfer-free-energies",
            root_name,
        )

        os.makedirs(os.path.join(root_path, "schemas"))

        force_field = ForceField(
            force_field_path, load_plugins=True, allow_cosmetic_attributes=True
        )
        force_field.to_file(
            os.path.join(root_path, "force-field.offxml"),
            discard_cosmetic_attributes=True,
        )

        for i, schema in enumerate(schemas):

            with open(os.path.join(root_path, "schemas", f"{i + 1}.json"), "w") as file:
                file.write(schema.json(indent=2))


if __name__ == "__main__":
    main()
