Name:           spdlog-devel
Version:        1.9.2
Release:        1%{?dist}
Summary:        Very fast, header-only/compiled, C++ logging library.

License:        MIT License
ExclusiveArch:  x86_64
URL:            https://github.com/gabime/spdlog
Source0:        cmake-3.22.3-linux-x86_64.sh
Source1:        v1.9.2.tar.gz

BuildRequires:       devtoolset-7-gcc
BuildRequires:       devtoolset-7-gcc-c++

%description
Very fast, header-only/compiled, C++ logging library.

%prep
source /opt/rh/devtoolset-7/enable

rm -rf %{_builddir}
mkdir -p %{_builddir}/usr

cd %{_builddir}
cp %{SOURCE0} .
sh %{SOURCE0} --prefix=%{_builddir}/usr --exclude-subdir

cd %{_builddir}
tar zxf %{SOURCE1}
cd spdlog-1.9.2
mkdir build

%build
source /opt/rh/devtoolset-7/enable

cd %{_builddir}/spdlog-1.9.2/build
cmake -DCMAKE_BUILD_TYPE=Release -DSPDLOG_BUILD_EXAMPLES=OFF -DSPDLOG_BUILD_TESTING=OFF -DCMAKE_INSTALL_PREFIX=%{_builddir}/%{_prefix} ..
cmake --build . --target install
#find %{_builddir}%{_libdir} -type f
#find %{_builddir}%{_includedir} -type f

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_libdir}/pkgconfig
%{__install} -d %{buildroot}%{_libdir}/cmake/spdlog

%{__install} -d %{buildroot}%{_includedir}
%{__install} -d %{buildroot}%{_includedir}/spdlog
%{__install} -d %{buildroot}%{_includedir}/spdlog/cfg
%{__install} -d %{buildroot}%{_includedir}/spdlog/sinks
%{__install} -d %{buildroot}%{_includedir}/spdlog/details
%{__install} -d %{buildroot}%{_includedir}/spdlog/fmt
%{__install} -d %{buildroot}%{_includedir}/spdlog/fmt/bundled

rsync -az %{_builddir}%{_libdir}/ %{buildroot}%{_libdir}/
rsync -az %{_builddir}%{_includedir}/ %{buildroot}%{_includedir}/

%files
%defattr(-,root,root,-)
%doc
%{_includedir}/spdlog/*.h
%{_includedir}/spdlog/cfg/*.h
%{_includedir}/spdlog/sinks/*.h
%{_includedir}/spdlog/details/*.h
%{_includedir}/spdlog/fmt/*.h
%{_includedir}/spdlog/fmt/bundled/*.h
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/spdlog/*.cmake

%changelog
* Thu Mar 31 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.9.2-1
- source to use devtoolset-7
- less output from rsync, tar command
* Tue Mar 29 2022 Nurmukhamed Artykaly <nurmukhamed.artykaly@hdfilm.kz> 1.9.2-1
- Initial spec file
