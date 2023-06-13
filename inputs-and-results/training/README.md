# Training


Contained within this directory are the main inputs and outputs
for training the DE-FF force field against both physical property and QC data.

Training runs and their description:

1. `non-bonded`: Non-bonded training of the DE general force field including the optimised DE-TIP4P-B68 water model.

2. `bonded`: Training of the bonded parameters for the output of the `non-bonded` training. The dataset covers all elements except for {F, P, S, I}.

3. `example-non-bonded` : Contains a notebook ([physical-property-fitting.ipynb](example-non-bonded/physical-property-fitting.ipynb)) demonstrating the set up and training of a DE-FF to a toy physical property dataset. 

4. `additional-training`: Contains a collection of other exploratory bonded and non-bonded training runs.
