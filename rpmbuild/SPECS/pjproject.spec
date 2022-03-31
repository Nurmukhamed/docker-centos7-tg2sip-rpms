#
# spec file for package pjproject
#

Name:          pjproject
Version:       2.9
Release:       1
Summary:       Free and open source multimedia communication library
License:       GPL-2.0
Group:         Applications/Communications
Url:           http://www.pjsip.org
Source0:       %{version}.tar.gz
BuildRequires: gcc-c++ openssl-devel alsa-lib-devel

%package devel
Summary:       Development package for pjproject
Group:         Development/Productivity/Telephony/Servers

%description
PJSIP is a free and open source multimedia communication libary written in
C language implementing standard based protocols such as SIP, SDP, RTP,
STUN, TURN, ICE.

%description devel
Development package for pjproject.

%prep
rm -fR %{buildroot}
%setup -q

%build
# "--disable-libwebrtc" is to avoid the bug of debugedit.
# "--disable-libyuv" is to avoid the comile error for CentOS-6 (invalid types ... for array subscript at row_common.cc)
%configure --enable-shared --disable-sdl --disable-ffmpeg --disable-v4l2 \
  --disable-openh264 --enable-ssl --disable-libwebrtc --disable-libyuv
# disable parallel build due to race condition
# %{?_smp_mflags}
make all

%install
%make_install

%files
%{_libdir}/*.so.2

%files devel
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*

