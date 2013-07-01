Name:           libsndfile
Version:        1.0.25
Release:        0
License:        LGPL-2.1+
Summary:        C library for reading and writing sound files
Group:          Multimedia/Audio
BuildRequires:  pkgconfig(alsa)
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  pkg-config
BuildRequires:  speex-devel
BuildRequires:  sqlite-devel
Url:            http://www.mega-nerd.com/libsndfile/
Source:         libsndfile-%{version}.tar.gz
Source2:        baselibs.conf
Source1001: 	libsndfile.manifest

%description
Libsndfile is a C library for reading and writing sound files, such as
AIFF, AU, and WAV files, through one standard interface.  It can
currently read and write 8, 16, 24, and 32-bit PCM files as well as
32-bit floating point WAV files and a number of compressed formats.


%package devel
Summary:        Development package for the libsndfile library
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       glibc-devel
Requires:       libstdc++-devel

%description devel
This package contains the files needed to compile programs that use the
libsndfile library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%define warn_flags -W -Wall -Wstrict-prototypes -Wpointer-arith -Wno-unused-parameter
autoreconf --force --install
CFLAGS="%{optflags} %{warn_flags}"
export CFLAGS
%configure --disable-silent-rules \
	--disable-static \
    --enable-sqlite \
	--with-pic \
    --enable-experimental
make %{?_smp_mflags}

%check
pushd src
make check
popd

%install
%make_install
# remove programs; built in another spec file
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_mandir}/man1
# remove binaries from examples directory
make -C examples distclean
rm -rf %{buildroot}%{_datadir}/doc/libsndfile1-dev

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files 
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/libsndfile.so.1*

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libsndfile.so
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/*.pc

%changelog
