%define name		aqsis
%define version		1.2.0
#define snapshot	2006-12-23
%define release		%mkrel 1
%define lib_name_orig	libaqsis
%define lib_major	1
%define lib_name	%mklibname %{name} %{lib_major}

Summary:	Open source RenderMan-compliant 3D rendering solution
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:	GPL
Url:		http://www.aqsis.com/
Group:		Graphics
#Source:		%{name}-%{version}-%{snapshot}.tar.bz2
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	%{lib_name} = %{version}
BuildRequires:	liblog4cpp-devel
BuildRequires:	libMesaGLU-devel
BuildRequires:	mesaglut-devel
BuildRequires:	tiff-devel
BuildRequires:	XFree86-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:  fltk-devel
BuildRequires:	scons
BuildRequires:	libxslt-proc
BuildRequires:	OpenEXR-devel
BuildRequires:	zlib-devel
BuildRequires:	boost-devel

%description
Tha Aqsis rendering system consists of a set of libraries and applications for
creating high-quality computer imagery using the Pixar RenderMan Interface.

%package -n %{lib_name}
Summary: Aqsis rendering system
License: GPL/LGPL
Group: System/Libraries

%description -n %{lib_name}
The Aqsis library.

%package -n %{lib_name}-devel
Summary: Aqsis rendering system
License: GPL
Group: Development/C++
Requires: %{lib_name} >= %{version}
Provides: libaqsis-devel = %{version}

%description -n %{lib_name}-devel
The Aqsis library developpement files.

%prep
%setup -q

%build
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS
scons %{?_smp_mflags} destdir=$RPM_BUILD_ROOT \
                install_prefix=%{_prefix} \
                sysconfdir=%{_sysconfdir} \
		libdir=%{_libdir} \
                no_rpath=true \
                build

%install
rm -rf $RPM_BUILD_ROOT
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS
scons install

chmod a+rx $RPM_BUILD_ROOT%{_datadir}/%{name}/content/ribs/*/*/*.sh
sed -i 's|/usr/bin/bash|/bin/bash|' $RPM_BUILD_ROOT%{_datadir}/%{name}/content/ribs/*/*/*.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%doc AUTHORS COPYING INSTALL README ReleaseNotes
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/*
%exclude %{_datadir}/%{name}/content/ribs/*/*/*.bat

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/%{name}
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*


