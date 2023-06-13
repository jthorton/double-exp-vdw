import os.path

import click
from absolv.runners.equilibrium import EquilibriumRunner


@click.option(
    "--input",
    "-i",
    "schema_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.command()
def main(schema_path):
    schema_name = os.path.splitext(os.path.split(schema_path)[-1])[0]
    EquilibriumRunner.run(directory=schema_path, platform="CUDA")

    result = EquilibriumRunner.analyze(directory=schema_path)

    os.makedirs("results", exist_ok=True)
    with open(os.path.join("results", f"{schema_name}.json"), "w") as file:
        file.write(result.json(indent=2))


if __name__ == "__main__":
    main()
