
# Conditional build:
%bcond_without tests 	# do not perform "make test"
# link against libresolv (creates architecture-dependent package)
%bcond_with libresolv	

%include	/usr/lib/rpm/macros.perl
%define	pdir	Net
%define	pnam	DNS
Summary:	Net::DNS - Perl interface to the DNS resolver
Summary(pl):	Net::DNS - interfejs do resolvera DNS
Name:		perl-Net-DNS
Version:	0.41
Release:	1
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	e766ff5b707f562a05c42a7cd8491852
BuildRequires:	perl-devel >= 5.6
%if %{with tests}
BuildRequires:	perl-Digest-MD5 >= 2.12
BuildRequires:	perl-Digest-HMAC >= 1.00
BuildRequires:	perl-MIME-Base64 >= 2.11
BuildRequires:	perl-Test-Simple >= 0.18
BuildRequires:	perl-Test-Pod >= 0.95
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
%if !%{with libresolv}
BuildArch:	noarch
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Net::DNS is a DNS resolver implemented in Perl. It allows the
programmer to perform nearly any type of DNS query from a Perl script.

%description -l pl
Net::DNS jest resolverem DNS, zaimplementowanym w Perlu. Pozwala
programi¶cie na wykonanie niemal ka¿dego typu zapytania DNS ze skryptu
Perla.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL </dev/null \
	%{?with_libresolv:	--xs} \
	%{!?_with_libresolv:	--pm} \
	INSTALLDIRS=vendor

%{__make} \
	%{?with_libresolv: OPTIMIZE="%{rpmcflags}"}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README TODO
%if %{with libresolv}
%{perl_vendorarch}/Net/DNS.pm
%{perl_vendorarch}/Net/DNS
%{perl_vendorarch}/auto/Net/DNS/DNS.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Net/DNS/DNS.so
%else
%{perl_vendorlib}/Net/DNS.pm
%{perl_vendorlib}/Net/DNS
%endif

%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
