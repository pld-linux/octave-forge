Summary:	Extensions for GNU Octave
Summary(pl.UTF-8):	Rozszerzenia dla GNU Octave
Name:		octave-forge
Version:	20080831
Release:	0.1
License:	GPL
Group:		Applications/Math
Source0:	http://dl.sourceforge.net/octave/%{name}-bundle-%{version}.tar.gz
# Source0-md5:	680ea705eb7434e219eb4a3eaffd7fba
Patch0:		%{name}-postgresql.patch
Patch1:		%{name}-mysql.patch
URL:		http://octave.sourceforge.net/
BuildRequires:	GiNaC-devel
BuildRequires:	ImageMagick-c++-devel
# for jhandlers which doesn't build :/
#BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	bash
BuildRequires:	blas-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw3-devel
BuildRequires:	ftplib-devel
BuildRequires:	gcc-fortran
BuildRequires:	ghostscript
BuildRequires:	gsl-devel
BuildRequires:	hdf5-devel
BuildRequires:	jar
BuildRequires:	jdk
BuildRequires:	lapack-devel
BuildRequires:	libgcj-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
#BuildRequires:	mysql-devel
BuildRequires:	octave-devel >= 2:2.9.15
BuildRequires:	pcre-devel
#BuildRequires:	postgresql-devel
BuildRequires:	qhull-devel
#BuildRequires:	sqlite3-devel
BuildRequires:	swig >= 1.3.38
BuildRequires:	tetex
BuildRequires:	tetex-dvips
BuildRequires:	texinfo
BuildRequires:	texinfo-texi2dvi
#BuildRequires:	unixODBC-devel
BuildRequires:	xorg-lib-libX11-devel
Requires:	octave >= 2:2.9.15
Requires:	ImageMagick
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Set of custom scripts, functions and extensions for GNU Octave.
octave-forge (http://octave.sf.net/) is a community project for
collaborative development of octave extensions. If you have a large
package that you want to open up to collaborative development, or a
couple of m-files that you want to contribute to an existing package,
octave-forge is the place to do it.

%description -l pl.UTF-8
Zestaw dodatkowych skryptów, funkcji i rozszerzeń dla GNU Octave.
octave-forge (http://octave.sf.net/) to społeczny projekt do wspólnego
rozwijania rozszerzeń octave. Jeśli mamy pakiet, który chcemy otworzyć
w celu wspólnego rozwijania albo zbiór plików .m, które chcemy wnieść
do istniejącego pakietu, octave-forge jest odpowiednim miejscem.

%prep
%setup -q -n %{name}-bundle-%{version}
for d in main extra; do
	cd $d
	for pkg in *.tar.gz ; do
		tar zxf $pkg
	done
	cd ..
done

# needs very old ffmpeg?
rm -rf main/video-1.0.1
# needs jogl, WTF is jogl? java sucks
rm -rf extra/jhandles-0.3.4
# If someone really wants the pain, then uncomment stuff below
rm -rf main/database-1.0.1
#patch0 -p1
#patch1 -p1
#cd main/database-1.0.1/src
#./autogen.sh
#rm mysql_wrap.cpp

%build
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"; export CFLAGS
for d in main extra; do
	cd $d
	for pkg in * ; do
		[ -d $pkg ] || continue
		cd $pkg
		if [ -e src/configure ]; then
			cd src
			%configure
			cd ..
		fi
		%{__make}
		cd ..
	done
	cd ..
done

%install
rm -rf $RPM_BUILD_ROOT

for d in main extra; do
	cd $d
	for pkg in * ; do
		[ -d $pkg ] || continue
		cd $pkg
		%{__make} install \
			DESTDIR=$RPM_BUILD_ROOT
		cd ..
	done
	cd ..
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
octave -q -H --no-site-file --eval "pkg('rebuild');"

%postun
octave -q -H --no-site-file --eval "pkg('rebuild');"

%files
%defattr(644,root,root,755)
%{_libdir}/octave/packages/*
%{_datadir}/octave/packages/*
