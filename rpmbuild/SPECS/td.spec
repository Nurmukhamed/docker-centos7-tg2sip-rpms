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

Requires:       zlib-devel
Requires:       openssl-devel
Requires:       libpng-devel
Requires:       libjpeg-devel
Requires:       opus-devel

%description
TDLib (Telegram Database library) is a cross-platform library for building Telegram clients. It can be easily used from almost any programming language.

%package        devel
Summary:        Headers and libraries for building apps that using TDLib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications that use the TDLib.

%prep
rm -rf %{_builddir}
mkdir -p %{_builddir}%{_prefix}
cd %{_builddir}
cp %{SOURCE0} .
sh %{SOURCE0} --prefix=%{_builddir}%{_prefix} --exclude-subdir

tar zxvf %{SOURCE1} 
cd %{name}-%{version}
mkdir build

%build

cd %{_builddir}/%{name}-%{version}/build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_builddir}%{_prefix} ..
cmake --build . --target install

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_libdir}pkgconfig
%{__install} -d %{buildroot}%{_libdir}cmake/Td

%{__install} -d %{buildroot}%{_includedir}
%{__install} -d %{buildroot}%{_includedir}td
%{__install} -d %{buildroot}%{_includedir}td/telegram
%{__install} -d %{buildroot}%{_includedir}td/tl

rsync -avz %{_builddir}%{_prefix}/lib/ %{buildroot}%{_libdir}/
rsync -avz %{_builddir}%{_prefix}/include/ %{buildroot}%{_includedir}/

%files
%defattr(-,root,root,-)
%doc
%{_libdir}/*.so.*
%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/%{name}
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/Td/*.cmake

%changelog
