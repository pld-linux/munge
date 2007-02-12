Summary:	MUNGE Uid 'N' Gid Emporium - authentication service
Summary(pl.UTF-8):	MUNGE Uid 'N' Gid Emporium - usługa uwierzytelniająca
Name:		munge
Version:	0.5.7
Release:	1
License:	GPL?
Group:		Applications
Source0:	http://download.gna.org/munge/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	50fc85ddded96b13f893568d9f10d713
URL:		http://home.gna.org/munge/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for
creating and validating credentials. It is designed to be highly
scalable for use in an HPC cluster environment. It allows a process to
authenticate the UID and GID of another local or remote process within
a group of hosts having common users and groups. These hosts form a
security realm that is defined by a shared cryptographic key. Clients
within this security realm can create and validate credentials without
the use of root privileges, reserved ports, or platform-specific
methods.

%description -l pl.UTF-8
MUNGE (MUNGE Uid 'N' Gid Emporium) to usługa uwierzytelniająca do
tworzenia i sprawdzania poprawności danych uwierzytelniających. Jest
zaprojektowana jako wysoko skalowalna, przeznaczona do użycia w
środowisku klastrowym HPC. Pozwala procesowi na uwierzytelnienie UID-u
lub GID-u innego lokalnego lub zdalnego procesu w grupie hostów
mających wspólnych użytkowników i grupy. Hosty te tworzą dziedzinę
bezpieczeństwa określoną poprzez współdzielony klucz kryptograficzny.
Klienci wewnątrz tej dziedziny bezpieczeństwa mogą tworzyć i sprawdzać
poprawność danych uwierzytelniających bez wykorzystywania uprawnień
roota, zarezerwowanych portów czy metod zależnych od platformy.

%package libs
Summary:	MUNGE library
Summary(pl.UTF-8):	Biblioteka MUNGE
Group:		Libraries

%description libs
MUNGE library.

%description libs -l pl.UTF-8
Biblioteka MUNGE.

%package devel
Summary:	Header file for MUNGE library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki MUNGE
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header file for MUNGE library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki MUNGE.

%package static
Summary:	Static MUNGE library
Summary(pl.UTF-8):	Statyczna biblioteka MUNGE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MUNGE library.

%description static -l pl.UTF-8
Statyczna biblioteka MUNGE.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT/etc/rc.d/init.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/munge
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/munge
%attr(755,root,root) %{_bindir}/munge
%attr(755,root,root) %{_bindir}/remunge
%attr(755,root,root) %{_bindir}/unmunge
%attr(755,root,root) %{_sbindir}/munged
%{_mandir}/man1/munge.1*
%{_mandir}/man1/remunge.1*
%{_mandir}/man1/unmunge.1*
%{_mandir}/man7/munge.7*
%{_mandir}/man8/munged.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmunge.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmunge.so
%{_includedir}/munge.h
%{_mandir}/man3/munge.3*
%{_mandir}/man3/munge_ctx.3*
%{_mandir}/man3/munge_enum.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmunge.a
