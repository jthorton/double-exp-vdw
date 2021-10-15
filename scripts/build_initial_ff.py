"""Convert openff-2.0.0 to a double exponential style force field with a custom tip4p-de
water model that has been pre-fit."""

from openff.toolkit.typing.engines.smirnoff import ForceField, ParameterList
from simtk import unit
from smirnoff_plugins.handlers.nonbonded import DoubleExponential


def add_tip4p_double_exp(force_field: ForceField):

    double_exp_handler = force_field.get_parameter_handler("DoubleExponential")

    # now add in pre-fit tip4p-de water model parameters
    de_o = double_exp_handler.DEType(
        "[#1]-[#8X2H2+0:1]-[#1]",
        epsilon=0.21104 * unit.kilocalorie_per_mole,
        r_min=3.5204 * unit.angstrom,
        id="tip4p-de-O",
    )
    de_h = double_exp_handler.DEType(
        "[#1:1]-[#8X2H2+0]-[#1]",
        epsilon=0 * unit.kilocalorie_per_mole,
        r_min=1 * unit.angstrom,
        id="tip4p-de-H",
    )

    double_exp_handler._parameters.append(de_o)
    double_exp_handler._parameters.append(de_h)

    # add a library charge to zero the water and then use the virtual site to adjust the
    # charges
    lb_charges = force_field.get_parameter_handler("LibraryCharges")
    lb_charges._parameters = ParameterList(
        [
            lb_charge
            for lb_charge in force_field.get_parameter_handler("LibraryCharges")
            if lb_charge.id is None or "tip3p" not in lb_charge.id
        ]
    )
    lb_charges.add_parameter(
        {
            "smirks": "[#1:1]-[#8X2H2+0:2]-[#1:3]",
            "id": "tip4p-de",
            "charge1": 0 * unit.elementary_charge,
            "charge2": 0 * unit.elementary_charge,
            "charge3": 0 * unit.elementary_charge,
        }
    )

    virtual_site_handler = force_field.get_parameter_handler("VirtualSites")
    virtual_site_handler.add_parameter(
        {
            "smirks": "[#1:1]-[#8X2H2+0:2]-[#1:3]",
            "type": "DivalentLonePair",
            "distance": -0.010743 * unit.nanometers,
            "outOfPlaneAngle": 0.0 * unit.degrees,
            "match": "once",
            "charge_increment1": 0.53254 * unit.elementary_charge,
            "charge_increment2": 0.0 * unit.elementary_charge,
            "charge_increment3": 0.53254 * unit.elementary_charge,
        }
    )
    # Currently required due to OpenFF issue #884
    virtual_site_handler._parameters = ParameterList(virtual_site_handler._parameters)

    # Setup the needed constraints
    constraints = force_field.get_parameter_handler("Constraints")

    for parameter in constraints.parameters:
        parameter.id = parameter.id.replace("tip3p", "tip4p")


def build_double_exp_force_field(
    initial_force_field_path: str = "openff-2.0.0.offxml", water_model: str = "tip4p-de"
) -> ForceField:

    water_models = ["tip3p", "tip4p-de"]
    assert water_model in water_models, f"the allowed water models are {water_models}"

    ff = ForceField(initial_force_field_path, load_plugins=True)

    # create the new double exponential handler and configure with the alpha and beta
    # from the water fits
    double_exp_handler = DoubleExponential(version="0.3")
    double_exp_handler.scale14 = 0.5
    double_exp_handler.alpha = 16.789
    double_exp_handler.beta = 4.592

    # loop over the vdw and transfer the parameters and zero out the old LJ 12-6 terms
    vdw = ff.get_parameter_handler("vdW")

    for lj_parameter in vdw.parameters:

        if "tip3p" in lj_parameter.id:  # Skip TIP3P so we can use the custom TIP4P-DE
            continue

        de_parameter = double_exp_handler.DEType(
            lj_parameter.smirks,
            r_min=(lj_parameter.sigma ** 6 * 2) ** (1 / 6),
            epsilon=lj_parameter.epsilon,
        )
        double_exp_handler._parameters.append(de_parameter)

    ff.deregister_parameter_handler("vdW")

    vdw = ff.get_parameter_handler("vdW")
    vdw.add_parameter(
        {"smirks": "[*:1]", "epsilon": 0.0 * unit.kilocalories_per_mole, "sigma": 1.0 * unit.angstrom}
    )

    # we have to modify this parameter manually as this can cause the long range
    # correction in openmm to fail. This parameter is a place holder with almost zero
    # values, with epsilon mostly transferred to the oxygen here we make the r_min
    # bigger to work but we could probably zero out this term completely?
    problem_parameter = double_exp_handler.parameters["[#1:1]-[#8]"]
    problem_parameter.epsilon = 0.0 * unit.kilojoules_per_mole
    problem_parameter.r_min = 1.0 * unit.angstrom

    ff.register_parameter_handler(double_exp_handler)

    if water_model == "tip4p-de":
        add_tip4p_double_exp(ff)
    elif water_model == "tip3p":
        pass
    else:
        raise NotImplementedError()

    return ff


if __name__ == "__main__":
    ff = build_double_exp_force_field()
    ff.to_file("double-exp-ff.offxml")
