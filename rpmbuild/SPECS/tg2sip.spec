Name:           tg2sip
Version:        1.3.0
Release:        1%{?dist}
Summary: TG2SIP is a Telegram<->SIP voice gateway. It can be used to forward incoming telegram calls to your SIP PBX or make SIP->Telegram calls.       

License:        GPL-2.0 License
ExclusiveArch:  x86_64
URL:            https://github.com/Infactum/tg2sip
Source0:        cmake-3.22.3-linux-x86_64.sh
Source1:        v1.8.0.tar.gz
Source2:        2.12.tar.gz 
Source3:        v1.9.2.tar.gz
Source4:        v1.3.0.tar.gz
Source5:        config_site.h
Source6:        tdlib_header.patch
Source7:        tdlib_threadname.patch
Source8:        CMakeLists.txt

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

Requires: zlib-devel
Requires: openssl-devel
Requires: libpng-devel
Requires: libjpeg-devel
Requires: opus-devel

%description
TG2SIP is a Telegram<->SIP voice gateway. It can be used to forward incoming telegram calls to your SIP PBX or make SIP->Telegram calls.

%prep
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/src
cd $RPM_BUILD_ROOT/usr/src
cp %{SOURCE0} .
sh %{SOURCE0} --prefix=$RPM_BUILD_ROOT/usr --exclude-subdir

tar zxvf %{SOURCE1} 
cd td-1.8.0
mkdir build
cd build

cd $RPM_BUILD_ROOT/usr/src

tar zxvf %{SOURCE2}
cd $RPM_BUILD_ROOT/usr/src/pjproject-2.12
cp %{SOURCE5} pjlib/include/pj

cd $RPM_BUILD_ROOT/usr/src
tar zxvf %{SOURCE3}
cd spdlog-1.9.2
mkdir build

cd $RPM_BUILD_ROOT/usr/src
tar zxvf %{SOURCE4}
cd tg2sip-1.3.0
cp %{SOURCE8} .

%build
sh %{SOURCE0} --prefix=$RPM_BUILD_ROOT/usr --exclude-subdir

cd $RPM_BUILD_ROOT/usr/src/td-1.8.0/build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --target install

%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
