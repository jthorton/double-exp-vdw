from openff.qcsubmit.results import OptimizationResultCollection, TorsionDriveResultCollection
from openff.toolkit.topology import Molecule
from tqdm import tqdm

def remove_elf_failures(training_set, output_to_save):
    entries = list(training_set.entries['https://api.qcarchive.molssi.org:443/'])
    failed_entries = []
    index_to_delete = []
    inchi_keys = []
    for i, entry in tqdm(enumerate(entries)):
        mol = Molecule.from_mapped_smiles(entry.cmiles, allow_undefined_stereo=True)
        inkey = mol.to_inchikey()
        if inkey in inchi_keys:
            pass
        else:
            inchi_keys.append(inkey)
            try:
                mol.assign_partial_charges(partial_charge_method='am1bccelf10')
            except:
                print(entry.record_id)
                failed_entries.append(entry.record_id)
                index_to_delete.append(i)

    for i in sorted(index_to_delete, reverse=True):
        training_set.entries['https://api.qcarchive.molssi.org:443/'].pop(i)

    with open(output_to_save, "w") as file:
        file.write(training_set.json())


def main():

    # torsion_training_set = TorsionDriveResultCollection.parse_file(
    #     "data-sets/1-2-0-td-set.json"
    # )
    # output_to_save = "data-sets/1-2-0-td-set-filtered-out-elf-failures.json"
    # remove_elf_failures(torsion_training_set, output_to_save)

    optimization_training_set = OptimizationResultCollection.parse_file(
        "data-sets/1-2-0-opt-set.json"
    )
    output_to_save = "data-sets/1-2-0-opt-set-filtered-out-elf-failures.json"
    remove_elf_failures(optimization_training_set, output_to_save)


if __name__ == "__main__":
    main()
