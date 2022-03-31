Name:           tg2sip
Version:        1.3.0
Release:        1%{?dist}
Summary: TG2SIP is a Telegram<->SIP voice gateway. It can be used to forward incoming telegram calls to your SIP PBX or make SIP->Telegram calls.       

License:        GPL-2.0 License
ExclusiveArch:  x86_64
URL:            https://github.com/Infactum/tg2sip
Source0:        cmake-3.22.3-linux-x86_64.sh
Source1:        v1.3.0.tar.gz
Source2:        CMakeLists.txt
Source3:        tg2sip.service

BuildRequires:       devtoolset-7-gcc
BuildRequires:       devtoolset-7-gcc-c++
BuildRequires:       make
BuildRequires:       git
BuildRequires:       wget
BuildRequires:       zlib-devel
BuildRequires:       openssl-devel
BuildRequires:       gperf
BuildRequires:       pkgconfig
BuildRequires:       ccache
BuildRequires:       gperf
BuildRequires:       unzip 
BuildRequires:       libpng-devel
BuildRequires:       libjpeg-devel
BuildRequires:       epel-release
BuildRequires:       opus-devel
BuildRequires:       patchelf
BuildRequires:       td-devel
BuildRequires:       td
BuildRequires:       spdlog-devel
BuildRequires:       systemd-rpm-macros

Requires: zlib
Requires: openssl
Requires: libpng
Requires: libjpeg
Requires: opus
Requires: td
Requires: spdlog

Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/bin/getent
Provides:	group(tg2sip)
Provides:	user(tg2sip)

%description
TG2SIP is a Telegram<->SIP voice gateway. It can be used to forward incoming telegram calls to your SIP PBX or make SIP->Telegram calls.

%prep
source /opt/rh/devtoolset-7/enable

rm -rf %{_builddir}
mkdir -p %{_builddir}/usr/src
cd %{_builddir}/usr/src

cp %{SOURCE0} .
sh %{SOURCE0} --prefix=%{_builddir}/usr --exclude-subdir

tar zxf %{SOURCE1}
cd %{name}-%{version}

# fixing package versions
sed -i "s%find_package(Td 1.7.10 REQUIRED)%find_package(Td 1.8.0 REQUIRED)%" CMakeLists.txt
sed -i "s%find_package(spdlog 0.17 REQUIRED)%find_package(spdlog 1.9.2 REQUIRED)%" CMakeLists.txt
sed -i "s%find_package(spdlog 0.17)%find_package(spdlog 1.9.2)%" ./libtgvoip/CMakeLists.txt

mkdir build

%build
source /opt/rh/devtoolset-7/enable

cd %{_builddir}/usr/src/%{name}-%{version}/build
cmake -DCMAKE_BUILD_TYPE=Release -DUSE_SYSTEM_CIMG=0 ..
cmake --build .

rm -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}/lib/systemd/system
%{__install} -d %{buildroot}%{_sharedstatedir}/%{name}

%{__install} -p -m 0755 %{_builddir}/usr/src/%{name}-%{version}/build/tg2sip %{buildroot}%{_bindir}/tg2sip
%{__install} -p -m 0755 %{_builddir}/usr/src/%{name}-%{version}/build/gen_db %{buildroot}%{_bindir}/gen_db
%{__install} -p -m 0644 %{_builddir}/usr/src/%{name}-%{version}/build/settings.ini %{buildroot}%{_sharedstatedir}/%{name}/settings.ini
%{__install} -p -m 0644 %{SOURCE3} %{buildroot}/lib/systemd/system

%clean
rm -rf %{_builddir}/usr/src/%{name}-%{version}

%pre
/usr/bin/getent group %{name} || /usr/sbin/groupadd -g 288 %{name}
/usr/bin/getent passwd %{name} || /usr/sbin/useradd -g 288 -u 288 -r -d /var/lib/%{name} -s /sbin/nologin %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
if [ "$1" = 0 ]; then
	%userremove %{name}
	%groupremove %{name}
fi
%systemd_postun_with_restart %{name}.service

%files
%attr(755,%{name},%{name}) %{_bindir}/%{name}
%attr(755,%{name},%{name}) %{_bindir}/gen_db
%attr(775,%{name},%{name}) %{_sharedstatedir}/%{name}
%attr(664,%{name},%{name}) %{_sharedstatedir}/%{name}/settings.ini
%attr(755,%{name},%{name}) /lib/systemd/system/%{name}.service

%changelog
* Thu Mar 31 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.3.0-1
- source to use devtoolset-7
- less output from rsync, tar command
* Tue Mar 29 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.3.0-1
- Initial spec file
