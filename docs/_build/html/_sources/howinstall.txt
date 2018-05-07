How install
===========

SOBA package instalation
------------------------

To install SOBA the best option is to use the package management system PIP. For this, we execute the following command.

.. code:: bash

        $ pip install soba

In case of error, this other command should be used, ensuring to have installed python 3 version and pip 3 version.

.. code:: bash

        $ pip3 install soba

First run
---------

Now let's execute an example. In this first execution we opted for the continuous model. First, we must first download the repository of the github SOBA project and access to the example directory.

.. code:: bash

        $ git clone https://github.com/gsi-upm/soba

        $ cd soba/projects/examples

Then, execute the run file. 

.. code:: bash

        $ python continuousExample.py

or

.. code:: bash

        $ python3 continuousExample.py

Different options are provided for execution:
	
1. Visual mode

.. code:: bash

        $ python3 continuousExample.py -v

1.1 Launching REST Server

.. code:: bash

        $ python3 continuousExample.py -v -s

1.2 Using RAMEN tool

.. code:: bash

        $ python3 continuousExample.py -v -r

2. Batch mode

.. code:: bash

        $ python3 continuousExample.py -b

2.1 Launching REST Server

.. code:: bash

        $ python3 continuousExample.py -b -s

2.2 Using RAMEN tool

.. code:: bash

        $ python3 continuousExample.py -b -r