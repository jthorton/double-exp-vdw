import pandas
from nonbonded.library.models.authors import Author
from nonbonded.library.models.datasets import DataSet
from openff.evaluator.datasets.curation.components import filtering, selection, thermoml
from openff.evaluator.datasets.curation.components.selection import State, TargetState
from openff.evaluator.datasets.curation.workflow import (
    CurationWorkflow,
    CurationWorkflowSchema,
)


def main():

    data_frame = CurationWorkflow.apply(
        pandas.DataFrame(),
        CurationWorkflowSchema(
            component_schemas=[
                thermoml.ImportThermoMLDataSchema(cache_file_name="thermoml.csv"),
                filtering.FilterByNComponentsSchema(n_components=[1]),
                filtering.FilterDuplicatesSchema(),
                filtering.FilterByPropertyTypesSchema(property_types=["Density"]),
                filtering.FilterByTemperatureSchema(
                    minimum_temperature=280.0, maximum_temperature=370
                ),
                filtering.FilterByPressureSchema(
                    minimum_pressure=99.9, maximum_pressure=101.4
                ),
                filtering.FilterBySmilesSchema(smiles_to_include=["O"]),
                selection.SelectDataPointsSchema(
                    target_states=[
                        TargetState(
                            property_types=[
                                ("Density", 1),
                            ],
                            states=[
                                State(
                                    temperature=temperature,
                                    pressure=101.325,
                                    mole_fractions=(1.0,),
                                )
                                for temperature in [
                                    281.15,
                                    298.15,
                                    313.15,
                                    329.15,
                                    345.15,
                                    361.15,
                                ]
                            ],
                        )
                    ]
                ),
            ]
        ),
        n_processes=4,
    )

    density_data = DataSet.from_pandas(
        data_frame,
        identifier="vdw-ff-train-water-rho",
        authors=[
            Author(name="Simon Boothroyd", email="empty@empty.com", institute="None")
        ],
        description="A data set of densities of pure water measured at ambient "
        "pressure and temperatures that span most of the liquid range.",
    )

    density_data.to_file(f"{density_data.id}.json")


if __name__ == "__main__":
    main()
