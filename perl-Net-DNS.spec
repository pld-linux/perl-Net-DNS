#
# Conditional build:
%bcond_without	tests 		# do not perform "make test"
%bcond_with	libresolv	# link against libresolv (creates architecture-dependent package)
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Net
%define	pnam	DNS
Summary:	Net::DNS - Perl interface to the DNS resolver
Summary(pl):	Net::DNS - interfejs perlowy do resolvera DNS
Name:		perl-Net-DNS
Version:	0.47
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	749a04eb4377e889ed58d004536a9117
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
	%{!?with_libresolv:	--no-xs} \
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
%{perl_vendorarch}/%{pdir}/%{pnam}.pm
%{perl_vendorarch}/%{pdir}/%{pnam}
%{perl_vendorarch}/auto/%{pdir}/%{pnam}/%{pnam}.bs
%attr(755,root,root) %{perl_vendorarch}/auto/%{pdir}/%{pnam}/%{pnam}.so
%else
%{perl_vendorlib}/%{pdir}/%{pnam}.pm
%{perl_vendorlib}/%{pdir}/%{pnam}
%endif

%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
