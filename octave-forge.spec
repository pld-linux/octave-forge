Summary:	Extensions for GNU Octave
Summary(pl):	Rozszerzenia dla GNU Octave
Name:		octave-forge
Version:	2004.07.07
Release:	0.1
License:	GPL
Group:		Applications/Math
Source0:	http://dl.sourceforge.net/octave/%{name}-%{version}.tar.gz
# Source0-md5:	28ac7f738801b6928a062a58b0417746
Patch0:		%{name}-make.patch
URL:		http://octave.sourceforge.net/
BuildRequires:	GiNaC-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	gcc-g77
BuildRequires:	hdf5-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	octave-devel >= 2:2.1.57
BuildRequires:	qhull-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Set of custom scripts, functions and extensions for GNU Octave.
octave-forge (http://octave.sf.net/) is a community project for
collaborative development of octave extensions. If you have a large
package that you want to open up to collaborative development, or a
couple of m-files that you want to contribute to an existing package,
octave-forge is the place to do it.

%description -l pl
Zestaw dodatkowych skryptów, funkcji i rozszerzeñ dla GNU Octave.
octave-forge (http://octave.sf.net/) to spo³eczny projekt do wspólnego
rozwijania rozszerzeñ octave. Je¶li mamy pakiet, który chcemy otworzyæ
w celu wspólnego rozwijania albo zbiór plików .m, które chcemy wnie¶æ
do istniej±cego pakietu, octave-forge jest odpowiednim miejscem.

%prep
%setup -q
%patch0 -p1

%build
export CXXFLAGS="%{rpmcflags} -fno-use-cxa-atexit"
./autogen.sh
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	MPATH="$RPM_BUILD_ROOT$( octave-config --m-site-dir )/%{name}" \
	OPATH="$RPM_BUILD_ROOT$( octave-config --oct-site-dir )/%{name}" \
	XPATH="$RPM_BUILD_ROOT$( octave-config --oct-site-dir )" \
	ALTMPATH="$RPM_BUILD_ROOT$( octave-config --m-site-dir )/%{name}" \
	ALTOPATH="$RPM_BUILD_ROOT$( octave-config --oct-site-dir )/%{name}" \
	mandir="$RPM_BUILD_ROOT%{_mandir}" \
	bindir="$RPM_BUILD_ROOT%{_bindir}"
find $RPM_BUILD_ROOT -name PKG_ADD -print0 | xargs -0 rm -f

mv $RPM_BUILD_ROOT%{_bindir}/mex $RPM_BUILD_ROOT%{_bindir}/mex-octave           

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f "%{_datadir}/octave/site/m/startup/octaverc" ] && \
	! grep -q "octave-forge" "%{_datadir}/octave/site/m/startup/octaverc"
then
	echo "LOADPATH = [ '$( octave-config --oct-site-dir)/octave-forge:$( octave-config --m-site-dir)/octave-forge/:', LOADPATH ];" >> "%{_datadir}/octave/site/m/startup/octaverc"
fi

%postun
if [ "$1" = "0" ]; then
	umask 027
	grep -E -v "octave-forge" "%{_datadir}/octave/site/m/startup/octaverc" > "%{_datadir}/octave/site/m/startup/octaverc.tmp"
	mv -f "%{_datadir}/octave/site/m/startup/octaverc.tmp" "%{_datadir}/octave/site/m/startup/octaverc"
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README RELEASE-NOTES TODO
%doc doc/*.html doc/coda/*.sgml doc/coda/appendices/*.sgml
%doc doc/coda/oct/*.sgml doc/coda/standalone/*.sgml
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
%( octave-config --m-site-dir )/%{name}
%( octave-config --oct-site-dir )/%{name}
