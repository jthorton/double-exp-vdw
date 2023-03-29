import functools
import json
import os.path
from multiprocessing import Pool
from pathlib import Path

from openff.bespokefit.optimizers.forcebalance import ForceBalanceInputFactory
from openff.bespokefit.schema.fitting import OptimizationSchema, OptimizationStageSchema
from openff.bespokefit.schema.optimizers import ForceBalanceSchema
from openff.bespokefit.schema.smirnoff import AngleHyperparameters, AngleSMIRKS, BondHyperparameters, \
    BondSMIRKS, ProperTorsionHyperparameters, ProperTorsionSMIRKS
from openff.bespokefit.schema.targets import (
    OptGeoTargetSchema,
    TorsionProfileTargetSchema, )
from openff.qcsubmit.results import (OptimizationResultCollection, TorsionDriveResultCollection)
from openff.qcsubmit.results.filters import SMARTSFilter
from openff.toolkit.typing.engines.smirnoff import ForceField


def main():
    Path("./schemas/optimizations/").mkdir(parents=True, exist_ok=True)

    torsion_training_set = TorsionDriveResultCollection.parse_file(
        "data-sets/reduced-set-td-set.json"
    )
    optimization_training_set = OptimizationResultCollection.parse_file(
        "data-sets/reduced-set-opt-set.json"
    )



    # to pick initial values and parameters to optimize
    # enter
    custom_force_field = 'force-field.offxml'
    initial_force_field = ForceField('force-field_7.offxml', load_plugins=True, allow_cosmetic_attributes=True)
    initial_force_field.to_file(custom_force_field)

    # Define the parameters to train
    with open("data-sets/reduced-set-angles-params-smirks.json") as file:
        angle_smirks = json.load(file)
    with open("data-sets/reduced-set-bonds-params-smirks.json") as file:
        bond_smirks = json.load(file)
    with open("data-sets/reduced-set-proper-torsions-params-smirks.json") as file:
        torsion_smirks = json.load(file)

    target_parameters = [
        *[
            AngleSMIRKS(smirks=smirks, attributes={"k", "angle"})
            for smirks in angle_smirks["Angles"]
        ],
        *[
            BondSMIRKS(smirks=smirks, attributes={"k", "length"})
            for smirks in bond_smirks["Bonds"]
        ],
        *[
            ProperTorsionSMIRKS(
                smirks=smirks,
                attributes={
                    f"k{i + 1}"
                    for i in range(
                        len(
                            initial_force_field.get_parameter_handler("ProperTorsions")
                            .parameters[smirks]
                            .k
                        )
                    )
                },
            )
            for smirks in torsion_smirks["ProperTorsions"]
        ],
    ]

    # Define the full schema for the optimization.

    optimization_schema = OptimizationSchema(
        id="reduced-set-targets",
        initial_force_field=os.path.abspath(custom_force_field),
        # Define the optimizer / ForceBalance specific settings.
        stages=[
            OptimizationStageSchema(
                optimizer=ForceBalanceSchema(
                    max_iterations=50,
                    step_convergence_threshold=0.01,
                    objective_convergence_threshold=0.1,
                    gradient_convergence_threshold=0.1,
                    n_criteria=2,
                    initial_trust_radius=-1.0,
                    extras={"wq_port": "55145", "asynchronous": "True"},
                ),
                # Define the torsion profile targets to fit against.
                targets=[
                    TorsionProfileTargetSchema(
                        reference_data=torsion_training_set,
                        energy_denominator=1.0,
                        energy_cutoff=5.0,
                        extras={"remote": "1"},
                    ),
                    OptGeoTargetSchema(
                        reference_data=optimization_training_set,
                        weight=0.1,
                        extras={"batch_size": 1, "remote": "1"},
                    ),
                ],
                # Define the parameters to refit and the priors to place on them.
                parameters=target_parameters,
                parameter_hyperparameters=[
                    AngleHyperparameters(priors={'k': 100, 'length': 20}),
                    BondHyperparameters(priors={'k': 100, 'length': 0.1}),
                    ProperTorsionHyperparameters(priors={'k': 15})
                ],
    )])

    with open(
            os.path.join(
                "./schemas", "optimizations", f"{optimization_schema.id}.json"
            ),
            "w",
    ) as file:
        file.write(optimization_schema.json())

    # Generate the ForceBalance inputs
    ForceBalanceInputFactory.generate(
        os.path.join(
            optimization_schema.id
        ),
        optimization_schema.stages[0],
        ForceField(optimization_schema.initial_force_field, load_plugins=True, allow_cosmetic_attributes=True)
    )

if __name__ == "__main__":
    main()
