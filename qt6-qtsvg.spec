# FIXME: qt6-qtdeclarative doesn't build on S390x
# BUG: https://bugreports.qt.io/browse/QTBUG-93101
ExcludeArch: s390x

%global qt_module qtsvg

#global unstable 1
%if 0%{?unstable}
%global prerelease rc2
%endif

Summary: Qt6 - Support for rendering and displaying SVG
Name:    qt6-%{qt_module}
Version: 6.2.2
Release: 1%{?dist}

License: LGPLv3 or GPLv2+
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

# filter plugin provides
%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1

BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

%description
Scalable Vector Graphics (SVG) is an XML-based language for describing
two-dimensional vector graphics. Qt provides classes for rendering and
displaying SVG drawings in widgets and on other paint devices.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build
%cmake_qt6

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%files
%license dist/changes-5.7.0 LICENSE.GPL2 LICENSE.GPL3 LICENSE.LGPLv3
%{_qt6_libdir}/libQt6Svg.so.6*
%{_qt6_libdir}/libQt6SvgWidgets.so.6*
%{_qt6_plugindir}/iconengines/libqsvgicon.so
%{_qt6_plugindir}/imageformats/libqsvg.so

%files devel
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_datadir}/modules/*.json
%{_qt6_headerdir}/QtSvg/
%{_qt6_headerdir}/QtSvgWidgets/
%{_qt6_libdir}/libQt6Svg.so
%{_qt6_libdir}/libQt6Svg.prl
%{_qt6_libdir}/libQt6SvgWidgets.so
%{_qt6_libdir}/libQt6SvgWidgets.prl
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtSvgTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Gui/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Svg/
%{_qt6_libdir}/cmake/Qt6Svg/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6SvgWidgets/
%{_qt6_libdir}/cmake/Qt6SvgWidgets/*.cmake
%dir  %{_qt6_libdir}/qt6/examples/svg
%{_qt6_libdir}/qt6/examples/svg/*
%{_qt6_libdir}/metatypes/qt6*_metatypes.json

%changelog
* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0
- 6.0.0
