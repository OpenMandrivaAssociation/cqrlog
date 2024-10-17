Name:		cqrlog
Version:	2.5.2
Release:	1%{?dist}
Summary:	An amateur radio contact logging program

License:	GPLv2
URL:		https://www.cqrlog.com/
Source0:	https://github.com/ok2cqr/cqrlog/archive/v%{version}/%{name}-%{version}.tar.gz

# Fixes arm builds, translation improvements, and other bug fixes.
Patch0:         cqrlog-install.patch
Patch1:         cqrlog-desktop.patch

#ExclusiveArch:  %{fpc_arches}

BuildRequires:	desktop-file-utils
BuildRequires:	fpc >= 3.0.4
BuildRequires:	lazarus >= 1.8
BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:  pkgconfig(hamlib)
BuildRequires:  trustedqsl-devel
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gtk+-x11-2.0)
BuildRequires:  gtk+3-devel
BuildRequires:  appstream-util

Requires:	mariadb-server
Requires:       openssl
Requires:       tqsllib


%description
CQRLOG is an advanced ham radio logger based on MySQL database. Provides radio
control based on hamlib libraries (currently support of 140+ radio types and 
models), DX cluster connection, QRZ callbook (web version), a grayliner, 
internal QSL manager database support and a most accurate country resolution 
algorithm based on country tables developed by OK1RR. CQRLOG is intended for 
daily general logging of HF, CW & SSB contacts and strongly focused on easy 
operation and maintenance.

%prep
%autosetup -p1

chmod -x src/azidis3.pas
chmod -x src/gline2.pas
chmod -x src/odbec.pas
chmod -x src/aziloc.pas
chmod -x src/znacmech.pas
chmod -x tools/cqrlog-apparmor-fix
chmod -x voice_keyer/voice_keyer.sh

%build
%make_build

%install
%make_install

desktop-file-validate %{buildroot}%{_datadir}/applications/cqrlog.desktop

# Fix icon location
for size in 32 48 64 128 256; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
    mv images/icon/${size}x${size}/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
done

for file in $(find %{buildroot}%{_datadir}/%{name} -name "*.txt"); do
    sed -i 's/\r//' $file
done
sed -i 's/\r//' %{buildroot}%{_datadir}/%{name}/ctyfiles/CountryDel.tab
sed -i 's/\r//' %{buildroot}%{_datadir}/%{name}/ctyfiles/MASTER.SCP

iconv -f iso8859-1 -t utf-8 %{buildroot}%{_datadir}/%{name}/ctyfiles/eqsl.txt > %{buildroot}%{_datadir}/%{name}/ctyfiles/eqsl.txt.conv && mv -f %{buildroot}%{_datadir}/%{name}/ctyfiles/eqsl.txt.conv %{buildroot}%{_datadir}/%{name}/ctyfiles/eqsl.txt


%check
appstream-util validate-relax --nonet \
    %{buildroot}/%{_datadir}/appdata/*.appdata.xml


%files
%license COPYING
%doc README.md AUTHORS CHANGELOG
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/cqrlog.1.*
