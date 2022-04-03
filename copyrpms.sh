#!/usr/bin/env bash

cp /var/lib/rpmbuild/RPMS/x86_64/*.rpm /rpms
chown ${USERID}:${GROUPID} /rpms/*.rpm
