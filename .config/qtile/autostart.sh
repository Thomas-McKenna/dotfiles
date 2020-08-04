#! /bin/bash
fava ~/Sync/Accounting/2020.beancount --host=0.0.0.0 &
picom -b &    #compositor
cmst & # Connection Manager
# nitrogen --restore & # background manager. swapped to feh for random background functionality. see cycle_pictures.sh
