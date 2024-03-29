#!/bin/sh

# define path to custom docker environment
#DOCKER_ENVVARS=/etc/apache2/docker_envvars

# write variables to DOCKER_ENVVARS
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
export APACHE_LOG_DIR=/var/log/apache2
export APACHE_LOCK_DIR=/var/lock/apache2
export APACHE_PID_FILE=/var/run/apache2.pid
export APACHE_RUN_DIR=/var/run/apache2
