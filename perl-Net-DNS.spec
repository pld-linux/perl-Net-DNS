#
# Conditional build:
# _without_tests 	- do not perform "make test"
# _with_libresolv	- link against libresolv
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Net
%define	pnam	DNS
Summary:	Net::DNS - Perl interface to the DNS resolver
Summary(pl):	Net::DNS - interfejs do resolvera DNS
Name:		perl-Net-DNS
Version:	0.38
Release:	1
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	b33ebbd53029264816ca9fa894b59419
BuildRequires:	perl-devel >= 5.6
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl-Digest-MD5 >= 2.12
BuildRequires:	perl-Digest-HMAC >= 1.00
BuildRequires:	perl-MIME-Base64 >= 2.11
BuildRequires:	perl-Test-Simple >= 0.18
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{?_with_libresolv:0}%{!?_with_libresolv:1}
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
	%{?_with_libresolv:	--xs} \
	%{?!_with_libresolv:	--pm} \
	INSTALLDIRS=vendor

%{__make} %{?_with_libresolv: OPTIMIZE="%{rpmcflags}"}

%{!?_without_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README TODO
%if 0%{?_with_libresolv:1}
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
