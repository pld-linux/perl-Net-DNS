#
# Conditional build:
# _without_tests - do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Net
%define	pnam	DNS
Summary:	Net::DNS - Perl interface to the DNS resolver
Summary(pl):	Net::DNS - interfejs do resolvera DNS
Name:		perl-Net-DNS
Version:	0.32
Release:	1
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	ftp://ftp.cpan.org/pub/CPAN/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
BuildRequires:	perl >= 5.6
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl-Digest-MD5 >= 2.12
BuildRequires:	perl-Digest-HMAC >= 1.00
BuildRequires:	perl-MIME-Base64 >= 2.11
BuildRequires:	perl-Test-Simple >= 0.18
%endif
BuildRequires:	rpm-perlprov >= 3.0.3-16
BuildArch:	noarch
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
perl Makefile.PL
%{__make}

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
%{perl_sitelib}/Net/DNS.pm
%{perl_sitelib}/Net/DNS
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
