FROM centos:7 as build

MAINTAINER Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz>

WORKDIR /root

# Update packages
RUN yum -y update 

# Install centos-release-scl
RUN yum -y install centos-release-scl yum-utils which bash man man-pages &&\
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo &&\
    yum-config-manager --enable rhel-server-rhscl-7-rpms &&\
    yum install -y devtoolset-7-gcc devtoolset-7-gcc-c++ &&\
    source /opt/rh/devtoolset-7/enable

RUN yum -y install epel-release &&\
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7

# Install additional packages
RUN yum install -y \
        make \
        git \
        wget \
        glibc-devel \
        zlib-devel \
        openssl-devel \
        gperf \
        pkgconfig \
        ccache \
        gperf \
        unzip \
        libpng-devel \
        libjpeg-devel \
        opus-devel \
        patchelf \
        ccache \
        gcc-c++ \
        openssl-devel \
        alsa-lib-devel \
        systemd-rpm-macros
# Install rpm-build packages
RUN yum install -y \
        rpm-build \
        rpm-devel \
        rpmlint \
        coreutils \
        diffutils \
        patch \
        rpmdevtools &&\
    rpmdev-setuptree

# Copy rpmbuild to container
COPY ./rpmbuild /root/rpmbuild

# Download sources to build rpms
RUN cd /root/rpmbuild/SOURCES &&\
    bash ./download.sh &&\
    sh ./cmake-3.22.3-linux-x86_64.sh --prefix=/usr --exclude-subdir

# TDLib 
FROM build as tdlib-build

# Build TDLib library
RUN rpmbuild -bb /root/rpmbuild/SPECS/td.spec

# Pjproject
FROM build as pjproject-build

# Build Pjproject library
# building debuginfo package occurs fail, so we dont need debuginfo packages
RUN rpmbuild --define "debug_package %{nil}" -bb /root/rpmbuild/SPECS/pjproject.spec

#SPDLog
FROM build as spdlog-build

RUN rpmbuild -bb /root/rpmbuild/SPECS/spdlog.spec

# TG2SIP
FROM build as tg2sip-build

COPY --from=tdlib-build /root/rpmbuild/RPMS/x86_64/td-1.8.0-1.el7.x86_64.rpm /root/rpmbuild/RPMS/x86_64/
COPY --from=tdlib-build /root/rpmbuild/RPMS/x86_64/td-devel-1.8.0-1.el7.x86_64.rpm /root/rpmbuild/RPMS/x86_64/
COPY --from=pjproject-build /root/rpmbuild/RPMS/x86_64/pjproject-2.9-1.x86_64.rpm /root/rpmbuild/RPMS/x86_64/
COPY --from=pjproject-build /root/rpmbuild/RPMS/x86_64/pjproject-devel-2.9-1.x86_64.rpm /root/rpmbuild/RPMS/x86_64/
COPY --from=spdlog-build /root/rpmbuild/RPMS/x86_64/spdlog-devel-1.9.2-1.el7.x86_64.rpm /root/rpmbuild/RPMS/x86_64/
COPY CMakeLists.txt /root/rpmbuild/SOURCES 
RUN yum -y localinstall /root/rpmbuild/RPMS/x86_64/*.rpm 

RUN rpmbuild -bb /root/rpmbuild/SPECS/tg2sip.spec

FROM centos:7 as final
# Update packages
RUN yum -y update &&\
    mkdir -p /var/lib/rpmbuild/RPMS/x86_64

COPY --from=tdlib-build /root/rpmbuild/RPMS/x86_64/td-1.8.0-1.el7.x86_64.rpm /var/lib/rpmbuild/RPMS/x86_64/
COPY --from=tdlib-build /root/rpmbuild/RPMS/x86_64/td-devel-1.8.0-1.el7.x86_64.rpm /var/lib/rpmbuild/RPMS/x86_64/
COPY --from=pjproject-build /root/rpmbuild/RPMS/x86_64/pjproject-2.9-1.x86_64.rpm /var/lib/rpmbuild/RPMS/x86_64/
COPY --from=pjproject-build /root/rpmbuild/RPMS/x86_64/pjproject-devel-2.9-1.x86_64.rpm /var/lib/rpmbuild/RPMS/x86_64/
COPY --from=spdlog-build /root/rpmbuild/RPMS/x86_64/spdlog-devel-1.9.2-1.el7.x86_64.rpm /var/lib/rpmbuild/RPMS/x86_64/
COPY --from=tg2sip-build /root/rpmbuild/RPMS/x86_64/tg2sip-1.3.0-1.el7.x86_64.rpm /var/lib/rpmbuild/RPMS/x86_64/
COPY copyrpms.sh /usr/local/bin/

RUN yum -y localinstall \
    /var/lib/rpmbuild/RPMS/x86_64/td-1.8.0-1.el7.x86_64.rpm \
    /var/lib/rpmbuild/RPMS/x86_64/pjproject-2.9-1.x86_64.rpm \
    /var/lib/rpmbuild/RPMS/x86_64/spdlog-devel-1.9.2-1.el7.x86_64.rpm \
    /var/lib/rpmbuild/RPMS/x86_64/tg2sip-1.3.0-1.el7.x86_64.rpm &&\
    find /var/lib/rpmbuild -type d -exec chmod 755 {} \; &&\
    find /var/lib/rpmbuild -type f -exec chmod 644 {} \; &&\
    chmod +x /usr/local/bin/copyrpms.sh 

#USER 288:288
WORKDIR /var/lib/tg2sip
CMD ["/usr/bin/tg2sip"]
