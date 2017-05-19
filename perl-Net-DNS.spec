# TODO: verify ignore-resolv_conf-open-errors patch (remove or update)
#
# Conditional build:
%bcond_with	tests		# perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Net
%define		pnam	DNS
Summary:	Net::DNS - Perl interface to the DNS resolver
Summary(pl.UTF-8):	Net::DNS - interfejs perlowy do resolvera DNS
Name:		perl-Net-DNS
Version:	1.10
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Net/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	4fa45b0dfe79667453c1553e16e52c2a
Patch0:		%{name}-ignore-resolv_conf-open-errors.patch
URL:		http://search.cpan.org/dist/Net-DNS/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	perl-Digest-BubbleBabble >= 0.01
BuildRequires:	perl-Digest-HMAC >= 1.03
BuildRequires:	perl-Digest-MD5 >= 2.13
BuildRequires:	perl-Digest-SHA >= 5.23
BuildRequires:	perl-IO-Socket-INET6 >= 2.51
BuildRequires:	perl-MIME-Base64 >= 2.11
BuildRequires:	perl-Test-Pod >= 0.95
BuildRequires:	perl-Test-Simple >= 0.52
BuildRequires:	perl(Time::Local) >= 1.19
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	perl-Digest-HMAC >= 1.03
Requires:	perl-Digest-MD5 >= 2.13
Requires:	perl-Digest-SHA >= 5.23
Requires:	perl-MIME-Base64 >= 2.11
Requires:	perl(Time::Local) >= 1.19
# not autodetected
Provides:	perl(Net::DNS::DomainName1035) = 1456
Provides:	perl(Net::DNS::DomainName2535) = 1456
Conflicts:	perl-Net-DNS-SEC < 1.01
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Net::DNS is a DNS resolver implemented in Perl. It allows the
programmer to perform nearly any type of DNS query from a Perl script.

%description -l pl.UTF-8
Net::DNS jest resolverem DNS, zaimplementowanym w Perlu. Pozwala
programiście na wykonanie niemal każdego typu zapytania DNS ze skryptu
Perla.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
#patch0 -p1

%{__sed} -i -e 's#/''usr/local/bin/perl#/''usr/bin/perl#' demo/* contrib/*

%build
%{__perl} Makefile.PL </dev/null \
	--no-online-tests \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# get rid of pod documentation
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/Net/DNS/*.pod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/Net/DNS.pm
%{perl_vendorlib}/Net/DNS/*.pm
%{perl_vendorlib}/Net/DNS/RR
%{perl_vendorlib}/Net/DNS/Resolver
%{_mandir}/man3/Net::DNS*.3pm*
%{_examplesdir}/%{name}-%{version}
