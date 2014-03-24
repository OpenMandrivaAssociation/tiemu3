%define		Werror_cflags %nil

Summary:	TiEmu is a TI89(Ti)/92(+)/V200 emulator
Name:		tiemu3
Version:	3.04svn
Release:	%mkrel 0.3
Source:		tiemu-%{version}.tar.xz
Group: 		Emulators
License:	GPL
BuildRequires:	libticables-devel
BuildRequires:	libticonv-devel
BuildRequires:	libtifiles-devel
BuildRequires:	libticalcs-devel
BuildRequires:	glib2-devel >= 2.6.0
BuildRequires:	gtk2-devel >= 2.6.0
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	ncurses-devel
BuildRequires:	desktop-file-utils >= 0.10
BuildRequires:	bison >= 1.28
BuildRequires:	flex >= 2.5.4
BuildRequires:	texinfo >= 4.4
BuildRequires:	dbus-devel >= 0.60
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	groff
BuildRequires:	qt3-devel
BuildRequires:	libglade2.0-devel
Requires:	xdg-utils >= 1.0.0
Conflicts:	tiemu > %{version}
Provides:	tiemu = %{version}

%description
TiEmu is a TI89(Ti)/92(+)/V200 emulator.

%prep
%setup -q -n tiemu-%{version}

%build
# source /etc/profile.d/qt.sh
# sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itcl/configure.in
# sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itcl/configure
# sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itk/configure.in
# sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itk/configure
CFLAGS="%{optflags}" ./configure --prefix=%{_prefix} --libdir=%{_libdir} --mandir=%{_mandir} --disable-nls --enable-shared-tcl-tk --enable-shared-itcl --with-dbus --without-kde
make

%install
mkdir -p $RPM_BUILD_ROOT
%makeinstall_std

# don't package unneeded empty directory
# rmdir $RPM_BUILD_ROOT%{_libdir}/insight1.0
# don't package Tcl/Tk stuff which conflicts with the system versions
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tclsh.1* $RPM_BUILD_ROOT%{_mandir}/man1/wish.1*
rm -rf $RPM_BUILD_ROOT%{_mandir}/man3
rm -rf $RPM_BUILD_ROOT%{_mandir}/mann
rm -rf $RPM_BUILD_ROOT/usr/man/mann
rm -f $RPM_BUILD_ROOT%{_libdir}/tclConfig.sh $RPM_BUILD_ROOT%{_libdir}/tkConfig.sh
# don't package these either, they won't conflict, but they aren't useful either
rm -f $RPM_BUILD_ROOT%{_bindir}/tclsh8.4 $RPM_BUILD_ROOT%{_bindir}/wish8.4
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

mkdir -p ${RPM_BUILD_ROOT}/usr/share/applications
cat >${RPM_BUILD_ROOT}/usr/share/applications/tiemu.desktop <<EOF
[Desktop Entry]
Name=TiEmu
Comment=TI89(Ti)/92(+)/V200 emulator
GenericName=TI89(Ti)/92(+)/V200 emulator
Encoding=UTF-8
Version=1.0
Type=Application
Exec=/usr/bin/tiemu
Icon=/usr/share/tiemu/pixmaps/icon.xpm
Terminal=false
Categories=Development;
EOF
desktop-file-install --delete-original --vendor lpg     \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}/usr/share/applications/tiemu.desktop

find %{buildroot} -perm 0555 | xargs chmod 0755

%files
%{_bindir}/tiemu
%{_mandir}/man1/tiemu*
%{_datadir}/insight*
%{_datadir}/redhat/gui
%{_datadir}/tiemu
%{_datadir}/applications/lpg-tiemu.desktop
%{_datadir}/tcl8.4
%{_datadir}/tk8.4
%{_datadir}/itcl3.2
%{_datadir}/itk3.2
%{_datadir}/iwidgets4.0.1
%{_libdir}/itcl3.2
%{_libdir}/itk3.2
%{_libdir}/libitcl3.2.so
%{_libdir}/libitk3.2.so
%{_libdir}/libtcl8.4.so
%{_libdir}/libtk8.4.so
%{_libdir}/tk8.4/pkgIndex.tcl

