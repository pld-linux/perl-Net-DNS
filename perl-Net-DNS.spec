#
# Conditional build:
%bcond_without	tests 		# do not perform "make test"
%bcond_without	libresolv	# link against libresolv (creates architecture-dependent package)
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Net
%define		pnam	DNS
Summary:	Net::DNS - Perl interface to the DNS resolver
Summary(pl.UTF-8):	Net::DNS - interfejs perlowy do resolvera DNS
Name:		perl-Net-DNS
Version:	0.62
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	91366517392283a909ee37d3c1c64904
URL:		http://search.cpan.org/dist/Net-DNS/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	perl-Digest-BubbleBabble
BuildRequires:	perl-Digest-HMAC >= 1.00
BuildRequires:	perl-Digest-MD5 >= 2.12
BuildRequires:	perl-IO-Socket-INET6 >= 2.51
BuildRequires:	perl-MIME-Base64 >= 2.11
BuildRequires:	perl-Net-IP >= 1.20
BuildRequires:	perl-Test-Pod >= 0.95
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
# https://rt.cpan.org/Public/Bug/Display.html?id=30316:
# BuildRequires:	FIXME(CVE-unknown)
%if !%{with libresolv}
BuildArch:	noarch
%endif
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

%{__sed} -i -e 's#/''usr/local/bin/perl#/''usr/bin/perl#' demo/* contrib/*

%build
%{__perl} Makefile.PL </dev/null \
	%{!?with_libresolv:--no-xs} \
	--no-online-tests \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	%{?with_libresolv:OPTIMIZE="%{rpmcflags}"}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{perl_vendorlib}/Net/DNS/Resolver

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# get rid of pod documentation
%if %{with libresolv}
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/Net/DNS/*.pod
%else
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/Net/DNS/*.pod
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README TODO
%{perl_vendorlib}/Net/DNS
%if %{with libresolv}
%{perl_vendorarch}/Net/DNS.pm
%{perl_vendorarch}/Net/DNS
%{perl_vendorarch}/auto/Net/DNS/DNS.bs
%dir %{perl_vendorarch}/auto/Net/DNS
%attr(755,root,root) %{perl_vendorarch}/auto/Net/DNS/DNS.so
%else
%{perl_vendorlib}/Net/DNS.pm
%endif

%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
