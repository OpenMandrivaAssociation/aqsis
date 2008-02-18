#define snapshot	2006-12-23
%define lib_name_orig	libaqsis
%define major 1
%define libname	%mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	RenderMan-compliant 3D rendering solution
Name:		aqsis
Version:	1.2.0
Release:	%mkrel 2
License:	GPLv2+
Url:		http://www.aqsis.org/
Group:		Graphics
#Source:		%{name}-%{version}-%{snapshot}.tar.bz2
Source:		http://downloads.sourceforge.net/aqsis/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	%{libname} = %{version}-%{release}
BuildRequires:	liblog4cpp-devel
BuildRequires:	mesaglu-devel
BuildRequires:	mesaglut-devel
BuildRequires:	tiff-devel
BuildRequires:	X11-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	scons
BuildRequires:	libxslt-proc
BuildRequires:	OpenEXR-devel
BuildRequires:	zlib-devel
BuildRequires:	boost-devel

%description
Tha Aqsis rendering system consists of a set of libraries and applications for
creating high-quality computer imagery using the Pixar RenderMan Interface.

%package -n %{libname}
Summary:	Aqsis library
Group:		System/Libraries

%description -n %{libname}
The Aqsis library.

%package -n %{develname}
Summary:	Development files for Aqsis
Group:		Development/C++
Requires:	%{libname} >= %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d
Provides:	%mklibname %{name} 1 -d

%description -n %{develname}
The Aqsis library developpement files.

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
scons %{?_smp_mflags} destdir=%{buildroot} \
                install_prefix=%{_prefix} \
                sysconfdir=%{_sysconfdir} \
		libdir=%{_libdir} \
                no_rpath=true \
                build

%install
rm -rf %{buildroot}
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
scons install

chmod a+rx %{buildroot}%{_datadir}/%{name}/content/ribs/*/*/*.sh
sed -i 's|/usr/bin/bash|/bin/bash|' %{buildroot}%{_datadir}/%{name}/content/ribs/*/*/*.sh

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%doc AUTHORS README ReleaseNotes
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/*
%exclude %{_datadir}/%{name}/content/ribs/*/*/*.bat

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
