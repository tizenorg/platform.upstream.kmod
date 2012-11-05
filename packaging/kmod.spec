Name:           kmod
Version:        9
Release:        0
License:        LGPL-2.1+ and GPL-2.0+
%define lname	libkmod
Summary:        Utilities to load modules into the kernel
Url:            http://www.politreco.com/2011/12/announce-kmod-2/
Group:          System/Kernel

#Git-Web:	http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
#Git-Clone:	git://git.kernel.org/pub/scm/utils/kernel/kmod/kmod
Source:         %{name}-%{version}.tar.xz
Source2:        %{name}-%{version}.tar.sign
Patch1:         kmod-so-version.diff
Patch2:         fix-32bits.diff

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.21
BuildRequires:  xz
BuildRequires:  pkgconfig(liblzma) >= 4.99
BuildRequires:  pkgconfig(zlib)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

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
Group:          System/Kernel
Conflicts:      module-init-tools
Requires(pre):	filesystem

%description compat
kmod is a set of tools to handle common tasks with Linux kernel
modules like insert, remove, list, check properties, resolve
dependencies and aliases.

This package contains traditional name symlinks (lsmod, etc.)

%package -n %lname
License:        LGPL-2.1+
Summary:        Library to interact with Linux kernel modules
Group:          System/Libraries

%description -n %lname
libkmod was created to allow programs to easily insert, remove and
list modules, also checking its properties, dependencies and aliases.

%package -n libkmod-devel
License:        LGPL-2.1+
Summary:        Development files for libkmod
Group:          Development/Libraries/C and C++
Requires:       %lname = %{version}

%description -n libkmod-devel
libkmod was created to allow programs to easily insert, remove and
list modules, also checking its properties, dependencies and aliases.

This package contains the development headers for the library found
in %lname.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
autoreconf -fi
# The extra --includedir gives us the possibility to detect dependent
# packages which fail to properly use pkgconfig.
%configure \
   --with-xz \
   --with-zlib \
   --includedir=%{_includedir}/%{name}-%{version} \
   --with-rootlibdir=%{_libdir} \
   --bindir=%{_bindir}
make %{?_smp_mflags}

%check
make check

%install
%make_install
rm -f %{buildroot}/%{_libdir}/*.la

# kmod-compat
mkdir -p %{buildroot}/%{_sbindir}
ln -s %{_bindir}/kmod %{buildroot}/%{_bindir}/lsmod
for i in depmod insmod lsmod modinfo modprobe rmmod; do
	ln -s %{_bindir}/kmod %{buildroot}/%{_sbindir}/$i
done;


%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/kmod
%{_mandir}/man5/modules.dep.bin.5*

%files -n %lname
%defattr(-,root,root)
%{_libdir}/libkmod.so.2*

%files -n libkmod-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%files compat
%defattr(-,root,root)
%{_bindir}/lsmod
%{_sbindir}/depmod
%{_sbindir}/insmod
%{_sbindir}/lsmod
%{_sbindir}/modinfo
%{_sbindir}/modprobe
%{_sbindir}/rmmod
%{_mandir}/man5/depmod.d.5*
%{_mandir}/man5/modprobe.d.5*
%{_mandir}/man5/modules.dep.5*
%{_mandir}/man8/depmod.8*
%{_mandir}/man8/insmod.8*
%{_mandir}/man8/lsmod.8*
%{_mandir}/man8/modinfo.8*
%{_mandir}/man8/modprobe.8*
%{_mandir}/man8/rmmod.8*

%changelog
