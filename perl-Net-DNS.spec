%define		perl_sitelib	%(eval "`perl -V:installsitelib`"; echo $installsitelib)
Summary:	Net-DNS perl module
Summary(pl):	Modu³ perla Net-DNS
Name:		perl-Net-DNS
Version:	0.12
Release:	3
Copyright:	GPL
Group:		Development/Languages/Perl
Group(pl):	Programowanie/Jêzyki/Perl
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/Net/Net-DNS-%{version}.tar.gz
Patch:		perl-Net-DNS-paths.patch
BuildRequires:	perl >= 5.005_03-10
%requires_eq	perl
Requires:	%{perl_sitearch}
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Net-DNS - Perl interface to the DNS resolver. 

%description -l pl
Net-DNS - interfejs do resolvera DNS.

%prep
%setup -q -n Net-DNS-%{version}
%patch -p1

%build
perl Makefile.PL
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}

make install DESTDIR=$RPM_BUILD_ROOT

install demo/* $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}
cp -a contrib  $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}

(
  cd $RPM_BUILD_ROOT%{perl_sitearch}/auto/Net/DNS
  sed -e "s#$RPM_BUILD_ROOT##" .packlist >.packlist.new
  mv .packlist.new .packlist
)

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man3/* \
        Changes README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {Changes,README,TODO}.gz

%{perl_sitelib}/Net/DNS.pm
%{perl_sitelib}/Net/DNS
%{perl_sitearch}/auto/Net/DNS

%{_mandir}/man3/*

/usr/src/examples/%{name}-%{version}
