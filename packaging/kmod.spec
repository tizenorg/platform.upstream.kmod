Name:           kmod
Version:        15
Release:        0
License:        LGPL-2.1+ and GPL-2.0+
Summary:        Utilities to load modules into the kernel
Url:            http://www.politreco.com/2011/12/announce-kmod-2/
Group:          Base/Libraries
Source:         %{name}-%{version}.tar.xz
Source1001: 	kmod.manifest
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.21
BuildRequires:  xz
BuildRequires:  pkgconfig(liblzma) >= 4.99
BuildRequires:  pkgconfig(zlib)

%description
kmod is a set of tools to handle common tasks with Linux kernel
modules like insert, remove, list, check properties, resolve
dependencies and aliases.

These tools are designed on top of libkmod, a library that is shipped
with kmod. The aim is to be compatible with tools, configurations and
indexes from module-init-tools project.

%package compat
License:        GPL-2.0+
Summary:        Compat symlinks for kernel module utilities
Group:          Base/Libraries
Requires:       kmod
Requires(pre):	filesystem
Provides:       module-init-tools

%description compat
kmod is a set of tools to handle common tasks with Linux kernel
modules like insert, remove, list, check properties, resolve
dependencies and aliases.

This package contains traditional name symlinks (lsmod, etc.)

%package -n libkmod
License:        LGPL-2.1+
Summary:        Library to interact with Linux kernel modules
Group:          Base/Libraries

%description -n libkmod
libkmod was created to allow programs to easily insert, remove and
list modules, also checking its properties, dependencies and aliases.

%package -n libkmod-devel
License:        LGPL-2.1+
Summary:        Development files for libkmod
Group:          Development/Libraries
Requires:       libkmod = %{version}

%description -n libkmod-devel
libkmod was created to allow programs to easily insert, remove and
list modules, also checking its properties, dependencies and aliases.

This package contains the development headers for the library found
in libkmod.

%prep
%setup -q
cp %{SOURCE1001} .

%build
autoreconf -fi
# The extra --includedir gives us the possibility to detect dependent
# packages which fail to properly use pkgconfig.
%configure \
   --with-xz \
   --disable-manpages \
   --with-zlib \
   --includedir=%{_includedir}/%{name}-%{version} \
   --with-rootlibdir=%{_libdir} \
   --bindir=%{_bindir}
make %{?_smp_mflags}

%check
make check

%install
%make_install

# kmod-compat
mkdir -p %{buildroot}/%{_sbindir}
ln -s %{_bindir}/kmod %{buildroot}/%{_bindir}/lsmod
for i in depmod insmod lsmod modinfo modprobe rmmod; do
	ln -s %{_bindir}/kmod %{buildroot}/%{_sbindir}/$i
done;


%post -n libkmod -p /sbin/ldconfig

%postun -n libkmod -p /sbin/ldconfig

%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/kmod
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/kmod

%files -n libkmod
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libkmod.so.2*

%files -n libkmod-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%files compat
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/lsmod
%{_sbindir}/depmod
%{_sbindir}/insmod
%{_sbindir}/lsmod
%{_sbindir}/modinfo
%{_sbindir}/modprobe
%{_sbindir}/rmmod

%changelog
