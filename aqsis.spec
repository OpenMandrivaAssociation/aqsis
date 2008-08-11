%define lib_name_orig	libaqsis
%define major 1
%define libname	%mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	RenderMan-compliant 3D rendering solution
Name:		aqsis
Version:	1.4.0
Release:	%mkrel 2
License:	GPLv2+
Group:		Graphics
Url:		http://www.aqsis.org/
Source0:	http://downloads.sourceforge.net/aqsis/%{name}-%{version}.tar.bz2
Requires:	%{libname} = %{version}-%{release}
BuildRequires:	mesaglu-devel
BuildRequires:	mesaglut-devel
BuildRequires:	tiff-devel
BuildRequires:	libjpeg-devel
BuildRequires:	X11-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	cmake
BuildRequires:	libxslt-proc
BuildRequires:	OpenEXR-devel
BuildRequires:	zlib-devel
BuildRequires:	boost-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
# (tpg) this is needec, because upstream didn't cleaned tarball
# next release should be ok
rm -rf build

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%cmake \
    -DAQSIS_USE_FLTK:BOOL=ON \
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
rm -rf %{buildroot}

pushd build
%makeinstall_std
popd

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%doc AUTHORS README ReleaseNotes
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/aqsis.xml
%{_datadir}/pixmaps/*.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
