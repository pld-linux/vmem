Summary:	libvmem and libvmmalloc - malloc-like volatile allocations
Summary(pl.UTF-8):	libvmem i libvmmalloc - ulotne alokacje w stylu malloca
Name:		vmem
Version:	1.8
Release:	1
License:	BSD
Group:		Applications/System
#Source0Download: https://github.com/pmem/vmem/releases
Source0:	https://github.com/pmem/vmem/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	345d01bc5f115c09590cddaf52b195ad
URL:		http://pmem.io/vmem/
BuildRequires:	autoconf >= 2.50
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.673
Conflicts:	pmdk-libs < 1.8
ExclusiveArch:	%{x8664} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libvmem and libvmmalloc are a couple of libraries for using persistent
memory for malloc-like volatile uses. They have historically been a
part of PMDK (<https://pmem.io/pmdk>) despite being solely for
volatile uses.

%description -l pl.UTF-8
libvmem i libvmmalloc to para bibliotek pozwalająca na wykorzystywanie
pamięci nieulotnej do zastosowań ulotnych w stylu malloca.
Historycznie były częścią PMDK (<https://pmem.io/pmdk>) mimo tego, że
mają wyłącznie ulotne zastosowania.

%package devel
Summary:	Header files for VMEM libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek VMEM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	pmdk-devel < 1.8

%description devel
Header files for VMEM libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek VMEM.

%package static
Summary:	Static VMEM libraries
Summary(pl.UTF-8):	Statyczne biblioteki VMEM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	pmdk-static < 1.8

%description static
Static VMEM libraries.

%description static -l pl.UTF-8
Statyczne biblioteki VMEM.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} -j1 \
	CC="%{__cc}" \
	includedir=%{_includedir} \
	libdir=%{_libdir} \
	prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	includedir=%{_includedir} \
	libdir=%{_libdir} \
	prefix=%{_prefix}

# debug libraries - needed for anything?
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/vmem_debug

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%attr(755,root,root) %{_libdir}/libvmem.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvmem.so.1
%attr(755,root,root) %{_libdir}/libvmmalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvmmalloc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvmem.so
%attr(755,root,root) %{_libdir}/libvmmalloc.so
%{_includedir}/libvmem.h
%{_includedir}/libvmmalloc.h
%{_pkgconfigdir}/libvmem.pc
%{_pkgconfigdir}/libvmmalloc.pc
%{_mandir}/man3/vmem_*.3*
%{_mandir}/man7/libvmem.7*
%{_mandir}/man7/libvmmalloc.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libvmem.a
%{_libdir}/libvmmalloc.a
