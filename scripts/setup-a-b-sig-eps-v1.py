import os

from build_initial_ff import build_double_exp_force_field
from nonbonded.library.factories.inputs.optimization import OptimizationInputFactory
from nonbonded.library.models.datasets import DataSet
from nonbonded.library.models.engines import ForceBalance
from nonbonded.library.models.forcefield import ForceField, Parameter
from nonbonded.library.models.projects import Optimization
from nonbonded.library.models.targets import EvaluatorTarget
from nonbonded.library.utilities import temporary_cd
from nonbonded.library.utilities.environments import ChemicalEnvironment

ANALYSIS_ENVIRONMENTS = [
    ChemicalEnvironment.Aqueous,
    ChemicalEnvironment.SecondaryAmine,
    ChemicalEnvironment.CarboxylicAcidSecondaryAmide,
    ChemicalEnvironment.AlkylBromide,
    ChemicalEnvironment.Alcohol,
    ChemicalEnvironment.Aromatic,
    ChemicalEnvironment.ArylChloride,
    ChemicalEnvironment.CarboxylicAcidTertiaryAmide,
    ChemicalEnvironment.AlkylChloride,
    ChemicalEnvironment.CarboxylicAcidEster,
    ChemicalEnvironment.Acetal,
    ChemicalEnvironment.TertiaryAmine,
    ChemicalEnvironment.Ketone,
    ChemicalEnvironment.Aldehyde,
    ChemicalEnvironment.PrimaryAmine,
    ChemicalEnvironment.Heterocycle,
    ChemicalEnvironment.Ether,
    ChemicalEnvironment.Alkene,
    ChemicalEnvironment.Alkane,
]


def main():

    optimization = Optimization(
        project_id="vdw-functional-forms",
        study_id="double-exp-vdw",
        id="a-b-sig-eps-v1",
        name="VdW Parameters (Sigma + Eps + Alpha + Beta) V1",
        description=(
            "An optimization of the vdW parameters of the `openff-2.0.0` force "
            "field + TIP4P-DE against a training set of physical property data."
        ),
        engine=ForceBalance(
            priors={
                "DoubleExponential/Atom/epsilon": 0.1,
                "DoubleExponential/Atom/rmin": 1.0,
                "/DoubleExponential/alpha": 2.0,
                "/DoubleExponential/beta": 2.0,
            }
        ),
        targets=[
            EvaluatorTarget(
                id="phys-prop",
                denominators={
                    "Density": "0.05 g / ml",
                    "EnthalpyOfMixing": "1.6 kJ / mol",
                },
                data_set_ids=["sage-train-v1", "vdw-ff-train-water-rho"],
            )
        ],
        force_field=ForceField.from_openff(build_double_exp_force_field()),
        parameters_to_train=[
            *[
                Parameter(
                    handler_type="DoubleExponential",
                    attribute_name=attribute,
                    smirks=None,
                )
                for attribute in ["alpha", "beta"]
            ],
            *[
                Parameter(
                    handler_type="DoubleExponential",
                    attribute_name=attribute,
                    smirks=smirks,
                )
                for attribute in ["epsilon", "r_min"]
                for smirks in [
                    "[#16:1]",
                    "[#17:1]",
                    "[#1:1]-[#6X3]",
                    "[#1:1]-[#6X3](~[#7,#8,#9,#16,#17,#35])~[#7,#8,#9,#16,#17,#35]",
                    "[#1:1]-[#6X3]~[#7,#8,#9,#16,#17,#35]",
                    "[#1:1]-[#6X4]",
                    "[#1:1]-[#6X4]-[#7,#8,#9,#16,#17,#35]",
                    "[#1:1]-[#7]",
                    # "[#1:1]-[#8]",  # Keep fixed until OpenMM #3277 is resolved.
                    "[#35:1]",
                    "[#6:1]",
                    "[#6X4:1]",
                    "[#7:1]",
                    "[#8:1]",
                    "[#8X2H0+0:1]",
                    "[#8X2H1+0:1]",
                    "[#1]-[#8X2H2+0:1]-[#1]",
                ]
            ],
        ],
        analysis_environments=ANALYSIS_ENVIRONMENTS,
        max_iterations=15,
    )

    with open(
        os.path.join(os.pardir, "schemas", "optimizations", f"{optimization.id}.json"),
        "w",
    ) as file:
        file.write(optimization.json())

    local_reference_data_sets = [
        # Load any data sets not stored on the RESTful API
        DataSet.parse_file(
            os.path.join(
                os.pardir,
                "data-set-curation",
                "physical-property",
                "optimizations",
                "vdw-ff-train-water-rho.json",
            )
        )
    ]

    id_counter = 7347

    for data_set in local_reference_data_sets:
        for entry in data_set.entries:
            entry.id = id_counter
            id_counter += 1

    with temporary_cd(os.path.join(os.pardir, "inputs-and-results", "optimizations")):

        OptimizationInputFactory.generate(
            optimization,
            "double-exp-vdw",
            max_time="168:00",
            evaluator_preset="lilac-dask",
            evaluator_port=8000,
            n_evaluator_workers=60,
            include_results=False,
            reference_data_sets=local_reference_data_sets,
        )


if __name__ == "__main__":
    main()
