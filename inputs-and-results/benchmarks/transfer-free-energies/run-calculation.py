import os.path

import click
from absolv.models import TransferFreeEnergySchema
from absolv.runners.equilibrium import EquilibriumRunner
from openff.toolkit.typing.engines.smirnoff import ForceField


@click.option(
    "--input",
    "-i",
    "schema_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--force-field",
    "-ff",
    "force_field_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.command()
def main(schema_path, force_field_path):

    schema = TransferFreeEnergySchema.parse_file(schema_path)
    schema_name = os.path.splitext(os.path.split(schema_path)[-1])[0]

    force_field = ForceField(
        force_field_path, load_plugins=True, allow_cosmetic_attributes=True
    )

    directory = os.path.join("staging", schema_name)
    os.makedirs(directory, exist_ok=True)

    EquilibriumRunner.setup(schema, force_field, directory=directory)
    EquilibriumRunner.run(directory=directory, platform="CUDA")

    result = EquilibriumRunner.analyze(directory=directory)
    print(result)

    os.makedirs("results", exist_ok=True)

    with open(os.path.join("results", f"{schema_name}.json"), "w") as file:
        file.write(result.json(indent=2))


if __name__ == "__main__":
    main()
