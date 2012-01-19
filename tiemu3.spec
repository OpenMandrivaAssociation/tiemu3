
Name:		tiemu3
Version:	3.03
Release: 	%mkrel 0.1.20081230svn2798.1
Source:		tiemu-%{version}.tar.bz2
Group: 		Emulators
License:	GPL
BuildRequires:	libticables-devel >= 1:1.0.0, libticonv-devel >= 1:1.0.4, libtifiles-devel >= 1:1.0.7, libticalcs-devel >= 1:1.0.7, glib2-devel >= 2.6.0, gtk2-devel >= 2.6.0, libglade2-devel >= 2.4.0, zlib-devel, kdelibs3-devel, libX11-devel, libXext-devel, ncurses-devel, desktop-file-utils >= 0.10, bison >= 1.28, flex >= 2.5.4, texinfo >= 4.4, dbus-devel >= 0.60, dbus-glib-devel >= 0.60, SDL-devel >= 1.2.0, groff
Requires:	tcl >= 8.4, tk >= 8.4, itcl >= 3.3-0.11.RC1, itk >= 3.3-0.8.RC1, iwidgets >= 4.0.1
Conflicts:	tcl < 1:8.5, tk < 1:8.5, itcl < 3.3, itk < 3.3, iwidgets < 4.0.2
Requires:	xdg-utils >= 1.0.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes:	tiemu < %{version}, tiemu-tigcc-debugging < 20050828
Conflicts:	tiemu > %{version}
Provides:	tiemu = %{version}
Summary:	TiEmu is a TI89(Ti)/92(+)/V200 emulator

%description
TiEmu is a TI89(Ti)/92(+)/V200 emulator. This version supports graphical debugging using Insight GDB.

%prep
%setup -q -n tiemu-%{version}

%build
source /etc/profile.d/qt.sh
sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itcl/configure.in
sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itcl/configure
sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itk/configure.in
sed -i 's/MINOR_VERSION=2/MINOR_VERSION=3/g;s/PATCHLEVEL=\.1/PATCHLEVEL=\.0/g' src/gdb/itcl/itk/configure
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --libdir=%{_libdir} --mandir=%{_mandir} --disable-nls --enable-shared-tcl-tk --enable-shared-itcl --with-dbus
make

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# don't package unneeded empty directory
rmdir $RPM_BUILD_ROOT%{_libdir}/insight1.0
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

%post
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%postun
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/bin/tiemu
%{_mandir}/man1/tiemu*
/usr/share/insight*
/usr/share/redhat/gui
/usr/share/tiemu
%{_datadir}/applications/lpg-tiemu.desktop
%{_datadir}/tcl8.4
%{_datadir}/tk8.4
%{_datadir}/itcl3.2
%{_datadir}/itk3.2
%{_datadir}/iwidgets4.0.1
%{_libdir}/itcl3.2
%{_libdir}/itk3.2


