How install
===========

SOBA package instalation
------------------------

First of all, it is necessary to have the SOBA package installed. For this, we execute the following command.

.. code:: bash

        $ pip install soba

In case of error, this other command should be used, ensuring to have installed python 3 version and pip 3 version.

.. code:: bash

        $ pip3 install soba

SEBA Github repository
----------------------

To use the SEBA software, we must first download the repository of the github SOBA project and access its directory.

.. code:: bash

        $ git clone https://github.com/gsi-upm/soba

        $ cd soba/projects/seba

Then, execute the run file. 

.. code:: bash

        $ python run.py

or

.. code:: bash

        $ python3 run.py

Different options are provided for execution:
	
1. Visual mode

.. code:: bash

        $ python3 run.py -v

  1.1 Launching REST Server

.. code:: bash

        $ python3 run.py -v -s

  1.2 Using RAMEN tool

.. code:: bash

        $ python3 run.py -v -r

2. Batch mode

.. code:: bash

        $ python3 run.py -b

  2.1 Launching REST Server

.. code:: bash

        $ python3 run.py -s

  2.2 Using RAMEN tool

.. code:: bash

        $ python3 run.py -r
