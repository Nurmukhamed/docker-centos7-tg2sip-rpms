Name:           td
Version:        1.8.0
Release:        1%{?dist}
Summary:        TDLib (Telegram Database library) is a cross-platform library for building Telegram clients. It can be easily used from almost any programming language.

License:        GPL-2.0 License
ExclusiveArch:  x86_64
URL:            https://github.com/tdlib/td.git
Source0:        cmake-3.22.3-linux-x86_64.sh       
Source1:        v1.8.0.tar.gz

BuildRequires:  devtoolset-7-gcc
BuildRequires:  devtoolset-7-gcc-c++
BuildRequires:  make
BuildRequires:  git
BuildRequires:  wget
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
BuildRequires:  gperf
BuildRequires:  pkgconfig
BuildRequires:  ccache
BuildRequires:  gperf
BuildRequires:  unzip 
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  epel-release
BuildRequires:  opus-devel
BuildRequires:  patchelf
BuildRequires:  rsync

Requires:       zlib
Requires:       openssl
Requires:       libpng
Requires:       libjpeg
Requires:       opus

%description
TDLib (Telegram Database library) is a cross-platform library for building Telegram clients. It can be easily used from almost any programming language.

%package        devel
Summary:        Headers and libraries for building apps that using TDLib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications that use the TDLib.

%prep
source /opt/rh/devtoolset-7/enable

rm -rf %{_builddir}
mkdir -p %{_builddir}%{_prefix}
cd %{_builddir}

sh %{SOURCE0} --prefix=%{_builddir}%{_prefix} --exclude-subdir

tar zxf %{SOURCE1}
cd %{name}-%{version} 
mkdir build

%build
source /opt/rh/devtoolset-7/enable
cd %{_builddir}/%{name}-%{version}/build

%{_builddir}%{_bindir}/cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    -DCMAKE_INSTALL_FULL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_builddir}%{_prefix} ..
%{_builddir}%{_bindir}/cmake --build . --target install -j $(grep -c ^processor /proc/cpuinfo)

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_libdir}/pkgconfig
%{__install} -d %{buildroot}%{_libdir}/cmake/Td

%{__install} -d %{buildroot}%{_includedir}
%{__install} -d %{buildroot}%{_includedir}/td
%{__install} -d %{buildroot}%{_includedir}/td/telegram
%{__install} -d %{buildroot}%{_includedir}/td/tl

rsync -az %{_builddir}%{_libdir}/ %{buildroot}%{_libdir}/
rsync -az %{_builddir}%{_includedir}/ %{buildroot}%{_includedir}/

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%doc
%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/Td/*.cmake
%doc

%changelog
* Sun Apr  3 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.8.0-1
- return to tar gz from git
- working version
* Thu Mar 31 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.8.0-1
- libdir changed from lib64 to lib
- less output from rsync, tar command
* Tue Mar 29 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.8.0-1
- Initial spec file
