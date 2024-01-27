# A field of hornets

[![GPLv3 License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/saeedghsh/hornet_field/blob/master/LICENSE)  
[![black](https://github.com/saeedghsh/hornet_field/actions/workflows/formatting.yml/badge.svg?branch=master)](https://github.com/saeedghsh/hornet_field/actions/workflows/formatting.yml)
[![pylint](https://github.com/saeedghsh/hornet_field/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/saeedghsh/hornet_field/actions/workflows/pylint.yml)
[![mypy](https://github.com/saeedghsh/hornet_field/actions/workflows/type-check.yml/badge.svg?branch=master)](https://github.com/saeedghsh/hornet_field/actions/workflows/type-check.yml)
[![pytest](https://github.com/saeedghsh/hornet_field/actions/workflows/pytest.yml/badge.svg?branch=master)](https://github.com/saeedghsh/hornet_field/actions/workflows/pytest.yml)

In the "Survivorship Bias" episode of the "You Are Not So Smart" podcast, an
analogy was made about bomber crew in WWII being like shirtless runners in a
field full of hornets. They might get through unharmed once or twice. But they
are bound to get stung if they keep going back and forth.

Got me thinking what is the probability of the shirtless person getting through
and if he has any chance of applying skill to survive or was it all stochastic
chance.

So here it goes, a stupidly unrelated simulation:
* A field.
* A group of hornet agents that move in the field.
* A traveling agent that aims at getting from one side of the field to the
  other side.

<p align="center">
    <img src="https://github.com/saeedghsh/hornet_field/blob/master/images/hornet_field.gif">
</p>

* Behavior Mode (for both traveler and hornet) is derived from Cartesian product of:
  * sensing capability: {with and without}
  * motion planning: {random, intelligent (rule-based, heuristic, algorithmic
    AI, etc) , intelligent-learning-based}
* Adversarial Learning Mode: also train the attacker agents and iterate


## Tests, coverage, linter, formatter, static type check, ...
```bash
$ black . --check
$ isort . --check-only
$ mypy . --explicit-package-bases
$ pylint $(git ls-files '*.py')
$ xvfb-run --auto-servernum pytest
```

# License
```
Copyright (C) Saeed Gholami Shahbandi
```

NOTE: Portions of this code/project were developed with the assistance of
ChatGPT, a product of OpenAI.  
Distributed with a GNU GENERAL PUBLIC LICENSE; see
[LICENSE](https://github.com/saeedghsh/hornet_field/blob/master/LICENSE).  
