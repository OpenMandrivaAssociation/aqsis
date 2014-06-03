%define major 1
%define libname	%mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	RenderMan-compliant 3D rendering solution
Name:		aqsis
Version:	1.8.2
Release:	2
License:	GPLv2+i
Group:		Graphics
Url:		http://www.aqsis.org/
Source0:	http://downloads.sourceforge.net/aqsis/%{name}-%{version}.tar.gz

BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	flex
BuildRequires:	xsltproc
BuildRequires:	boost-devel
BuildRequires:	qt4-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	zlib-devel

%description
Tha Aqsis rendering system consists of a set of libraries and applications for
creating high-quality computer imagery using the Pixar RenderMan Interface.

%package -n %{libname}
Summary:	Aqsis library
Group:		System/Libraries

%description -n %{libname}
The Aqsis library.

%package -n %{devname}
Summary:	Development files for Aqsis
Group:		Development/C++
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
The Aqsis library developpement files.

%prep
%setup -q

%build
%cmake \
    -DAQSIS_USE_QT:BOOL=ON \
    -DAQSIS_USE_OPENEXR:BOOL=ON \
    -DAQSIS_BOOST_LIB_SUFFIX:STRING=-mt \
    -DCMAKE_CMAKE_BUILD_TYPE=Release \
    -DAQSIS_ENABLE_TESTING:BOOL=OFF \
    -DAQSIS_USE_PLUGINS:BOOL=ON \
    -DAQSIS_USE_TIMERS:BOOL=ON \
    -DSYSCONFDIR:STRING=%{_sysconfdir} \
    -DLIBDIR="%{_libdir}" \
    -DDEFAULT_DISPLAYPATH="%{_libdir}/%{name}"

%make

%install
%makeinstall_std -C build

%files
%doc AUTHORS README
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/aqsis.xml
%{_datadir}/pixmaps/*.png
%{_iconsdir}/hicolor/*/mimetypes/*.png

%files -n %{libname}
%{_libdir}/%{name}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*

