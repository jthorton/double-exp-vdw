import os

from absolv.models import (
    EquilibriumProtocol,
    SimulationProtocol,
    State,
    System,
    TransferFreeEnergySchema,
)
from absolv.runners.equilibrium import EquilibriumRunner
from openff.evaluator.datasets import PhysicalPropertyDataSet, PhysicalProperty
from openff.toolkit.typing.engines.smirnoff import ForceField
from openmm import unit
from tqdm import tqdm
from openff.evaluator.substances import Component


def main():
    """
    Create the input files for the aqueous/non-aqueous solvation free energies for the DE-FF.
    """

    MNSOL_DATASET = "../../../data-set-curation/physical-property/physical-data-sets/mnsol-filtered.json"
    HYDRATION_DATASET = (
        "../../../data-set-curation/physical-property/physical-data-sets/fsolv-filtered.json"
    )
    mnsol = PhysicalPropertyDataSet.from_json(MNSOL_DATASET)
    freesolv: PhysicalPropertyDataSet = PhysicalPropertyDataSet.from_json(
        HYDRATION_DATASET
    )
    solvation_schemas = []
    hydration_schemas = []

    for entry in freesolv.properties:
        entry: PhysicalProperty
        solute = [
            component.smiles
            for component in entry.substance.components
            if component.role == Component.Role.Solute
        ][0]

        solvent = [
            component.smiles
            for component in entry.substance
            if component.role == Component.Role.Solvent
        ][0]
        schema = TransferFreeEnergySchema(
            system=System(
                solutes={solute: 1}, solvent_a=None, solvent_b={solvent: 1000}
            ),
            state=State(
                temperature=entry.thermodynamic_state.temperature.m * unit.kelvin,
                pressure=entry.thermodynamic_state.pressure.m * unit.kilopascal,
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
                    1.00,
                    1.00,
                    1.00,
                    1.00,
                    1.00,
                    0.95,
                    0.90,
                    0.80,
                    0.70,
                    0.60,
                    0.50,
                    0.40,
                    0.35,
                    0.30,
                    0.25,
                    0.20,
                    0.15,
                    0.10,
                    0.05,
                    0.00,
                ],
                lambda_electrostatics=[
                    1.00,
                    0.75,
                    0.50,
                    0.25,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                ],
                sampler="repex",
                production_protocol=SimulationProtocol(
                    n_steps_per_iteration=500, n_iterations=2000
                ),
            ),
        )
        hydration_schemas.append(schema)

    for entry in mnsol.entries:
        solute = [
            component.smiles
            for component in entry.substance.components
            if component.role == Component.Role.Solute
        ][0]
        solvent = [
            component.smiles
            for component in entry.substance
            if component.role == Component.Role.Solvent
        ][0]
        schema = TransferFreeEnergySchema(
            system=System(
                solutes={solute: 1}, solvent_a=None, solvent_b={solvent: 1000}
            ),
            state=State(
                temperature=entry.thermodynamic_state.temperature.m * unit.kelvin,
                pressure=entry.thermodynamic_state.pressure.m * unit.kilopascal,
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
                    1.00,
                    1.00,
                    1.00,
                    1.00,
                    1.00,
                    0.95,
                    0.90,
                    0.80,
                    0.70,
                    0.60,
                    0.50,
                    0.40,
                    0.35,
                    0.30,
                    0.25,
                    0.20,
                    0.15,
                    0.10,
                    0.05,
                    0.00,
                ],
                lambda_electrostatics=[
                    1.00,
                    0.75,
                    0.50,
                    0.25,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                ],
                sampler="repex",
                production_protocol=SimulationProtocol(
                    n_steps_per_iteration=500, n_iterations=2000
                ),
            ),
        )
        solvation_schemas.append(schema)

    print(f"Number of hydration calculations {len(hydration_schemas)}")
    print(f"Number of solvation calculations {len(solvation_schemas)}")
    # make the DEXP inputs
    alchemical_potential = (
        "lambda_sterics*(CombinedEpsilon*ScaledRepulsionFactor*RepulsionExp-CombinedEpsilon*ScaledAttractionFactor*AttractionExp);"
        "RepulsionExp=exp(ScaledAlpha-ScaledAlpha*ExpDistance);"
        "AttractionExp=exp(ScaledBeta-ScaledBeta*ExpDistance);"
        "ExpDistance=r/CombinedR;"
        "ScaledAttractionFactor=ScaledAlpha / ScaledAlphaMinBeta;"
        "ScaledRepulsionFactor=ScaledBeta / ScaledAlphaMinBeta;"
        "ScaledAlphaMinBeta=ScaledAlpha-ScaledBeta;"
        "ScaledAlpha=1.1 + lambda_sterics * (alpha - 1.1);"
        "ScaledBeta=1.0 + lambda_sterics * (beta - 1.0);"
        "CombinedR=r_min1+r_min2;"
        "CombinedEpsilon=epsilon1*epsilon2;"
    )
    root_path = "dexp-hydration"
    os.makedirs(os.path.join(root_path, "schemas"))
    dexp_force_field = ForceField(
        "dexp_all_fit_v1.offxml", load_plugins=True, allow_cosmetic_attributes=True
    )
    dexp_force_field.to_file(
        os.path.join(root_path, "force-field.offxml"), discard_cosmetic_attributes=True
    )
    for i, schema in tqdm(
        enumerate(hydration_schemas),
        desc="DEXP hydration",
        ncols=80,
        total=len(hydration_schemas),
    ):
        schema_name = f"{i + 1}.json"
        with open(os.path.join(root_path, "schemas", schema_name), "w") as file:
            file.write(schema.json(indent=2))

        directory = os.path.join(root_path, "staging", f"schema_{i + 1}")
        os.makedirs(directory, exist_ok=True)
        EquilibriumRunner.setup(
            schema=schema,
            force_field=dexp_force_field,
            directory=directory,
            custom_alchemical_potential=alchemical_potential,
        )

    root_path = "dexp-solvation"
    os.makedirs(os.path.join(root_path, "schemas"))
    dexp_force_field.to_file(
        os.path.join(root_path, "force-field.offxml"), discard_cosmetic_attributes=True
    )
    for i, schema in tqdm(
        enumerate(solvation_schemas),
        desc="DEXP solvation",
        ncols=80,
        total=len(solvation_schemas),
    ):
        schema_name = f"{i + 1}.json"
        with open(os.path.join(root_path, "schemas", schema_name), "w") as file:
            file.write(schema.json(indent=2))

        directory = os.path.join(root_path, "staging", f"schema_{i + 1}")
        os.makedirs(directory, exist_ok=True)
        EquilibriumRunner.setup(
            schema=schema,
            force_field=dexp_force_field,
            directory=directory,
            custom_alchemical_potential=alchemical_potential,
        )


if __name__ == "__main__":
    main()
