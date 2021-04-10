==========
Production
==========


Configuration
=============


Create environment file
-----------------------

Copy ``settings.env.dist`` file to ``settings.env`` and make the
necessary changes:

.. code-block:: shell

   $ cp ./settings.env.dist ./settings.env


Logging
=======


Application logging
-------------------

.. code-block:: shell

   $ sudo touch /var/log/branch.log
   $ sudo chown www-data:www-data /var/log/branch.log
   $ sudo chmod g+w /var/log/branch.log


Gunicorn logging
----------------

.. code-block:: shell

   # Create logging directory for gunicorn
   $ sudo mkdir /var/log/gunicorn
   $ sudo chown www-data:www-data /var/log/gunicorn

   # Create gunicorn log files
   $ sudo touch /var/log/gunicorn/branch.access.log
   $ sudo touch /var/log/gunicorn/branch.error.log
   $ sudo chown www-data:www-data /var/log/gunicorn/branch.*.log

   # Setup logrotate
   $ sudo cp ./provision/etc/logrotate.d/branch-* /etc/logrotate.d/


Start Web Server
================


Install socket/service
----------------------

.. code-block:: shell

   $ sudo ln -s $(pwd)/provision/etc/systemd/system/branch.service /etc/systemd/system/
   $ sudo ln -s $(pwd)/provision/etc/systemd/system/branch.socket /etc/systemd/system/


Enable socket/service
---------------------

.. code-block:: shell

   $ sudo systemctl start branch.socket
   $ sudo systemctl enable branch.socket
   $ sudo systemctl start branch.service
   $ sudo systemctl enable branch.service


Test gunicorn socket
--------------------

.. code-block:: shell

   $ systemctl status branch.socket
   $ file /run/branch.sock
   $ journalctl -u branch.socket

   # Change localhost to address from ALLOWED_HOSTS
   $ curl --unix-socket /run/branch.sock localhost


Test gunicorn service
---------------------

.. code-block:: shell

   $ systemctl status branch.service
   $ journalctl -u branch.service
