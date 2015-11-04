
=========================
Senlin Resources for Heat
=========================

Copy *.py files to your heat folder

  cp client/senlin.py /opt/stack/heat/heat/engine/clients/os/
  mkdir /opt/stack/heat/heat/engine/resources/openstack/senlin
  cp resources/senlin/*.py /opt/stack/heat/heat/engine/resources/openstack/senlin/
  cp setup.cfg /opt/stack/heat/

Reinstall heat services

  cd /opt/stack/heat/
  sudo python setup.py develop

Restart heat services
