Name:           td
Version:        1.8.0
Release:        1%{?dist}
Summary:        TDLib (Telegram Database library) is a cross-platform library for building Telegram clients. It can be easily used from almost any programming language.

License:        GPL-2.0 License
ExclusiveArch:  x86_64
URL:            https://github.com/Infactum/tg2sip
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
cp %{SOURCE0} .
sh %{SOURCE0} --prefix=%{_builddir}%{_prefix} --exclude-subdir

tar zxf %{SOURCE1} 
cd %{name}-%{version}
mkdir build

%build
source /opt/rh/devtoolset-7/enable
cd %{_builddir}/%{name}-%{version}/build
%{_builddir}%{_bindir}/cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_builddir}%{_prefix} ..
%{_builddir}%{_bindir}/cmake --build . --target install

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_libdir}pkgconfig
%{__install} -d %{buildroot}%{_libdir}cmake/Td

%{__install} -d %{buildroot}%{_includedir}
%{__install} -d %{buildroot}%{_includedir}td
%{__install} -d %{buildroot}%{_includedir}td/telegram
%{__install} -d %{buildroot}%{_includedir}td/tl

rsync -az %{_builddir}%{_prefix}/lib/ %{buildroot}%{_prefix}/lib/
rsync -az %{_builddir}%{_prefix}/include/ %{buildroot}%{_includedir}/

%files
%defattr(-,root,root,-)
%{_prefix}/lib/*.so.*
%doc
%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_prefix}/lib/*.a
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/cmake/Td/*.cmake
%doc

%changelog
* Thu Mar 31 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.8.0-1
- libdir changed from lib64 to lib
- less output from rsync, tar command
* Tue Mar 29 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.8.0-1
- Initial spec file
