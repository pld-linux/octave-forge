Summary:	extensions for GNU Octave
Summary(pl):	rozszerzenia dla GNU Octave
Name:		octave-forge
Version:	2003.06.02
Release:	1
License:	GPL
Group:		Applications/Math
Source0:	http://dl.sourceforge.net/octave/%{name}-%{version}.tar.gz
# Source0-md5:	73e24fc661bc94d83535e4387d24cea3
URL:		http://octave.sourceforge.net/
BuildRequires:	octave-devel
BuildRequires:	gcc-g77
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Set of custom scripts, functions and extensions for GNU Octave.

%description -l pl
Zestaw dodatkowych skryptów, funkcji i rozszerzeñ dla GNU Octave.

%prep
%setup -q

%build
./autogen.sh
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	MPATH="$RPM_BUILD_ROOT$( octave-config --m-site-dir )/%{name}" \
	OPATH="$RPM_BUILD_ROOT$( octave-config --oct-site-dir )/%{name}" \
	XPATH="$RPM_BUILD_ROOT$( octave-config --oct-site-dir )" \
	mandir="$RPM_BUILD_ROOT%{_mandir}" \
	bindir="$RPM_BUILD_ROOT%{_bindir}"

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
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
%( octave-config --m-site-dir )/%{name}
%( octave-config --oct-site-dir )/%{name}
