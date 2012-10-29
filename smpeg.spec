Summary:	SDL MPEG Library
Name:		smpeg
Version:	0.4.4
Release:	22
License:	LGPL
Group:		Libraries
# currently developed at http://icculus.org/smpeg/ but no release yet
Source0:	http://mirrors.dotsrc.org/lokigames/open-source/smpeg/%{name}-%{version}.tar.gz
# Source0-md5:	59c76ac704088ef5539210190c4e1fe3
Patch0:		%{name}-acfix.patch
Patch1:		%{name}-gcc.patch
Patch2:		%{name}-optimize.patch
Patch3:		%{name}-am18.patch
Patch4:		%{name}-gcc4.patch
Patch5:		%{name}-gnu-stack.patch
Patch6:		%{name}-fPIC.patch
Patch7:		%{name}-kill-gtk.patch
URL:		http://www.lokigames.com/development/smpeg.php3
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder and
SPLAY, an mpeg audio decoder created by Woo-jae Jung. We have
completed the initial work to wed these two projects in order to
create a general purpose MPEG video/audio player for the Linux OS.

%package libs
Summary:	Shared smpeg libraries
Group:		Libraries

%description libs
Shared smpeg libraries.

%package devel
Summary:	Smpeg header files and development documentation
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files and development documentation for smpeg.

%package gtv
Summary:	gtv MPEG player
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description gtv
gtv MPEG player.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p1

# get only AC_TYPE_SOCKLEN_T, kill the rest (libtool.m4 in particular)
tail -n 23 acinclude.m4 > acinc.tmp
mv -f acinc.tmp acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure \
	--disable-debug		\
	--disable-static	\
	--disable-gtk-player	\
	--disable-opengl-player \
	--enable-mmx

%{__make} \
	CC="%{__cxx}" \
	CCASFLAGS="\$(CFLAGS)"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/plaympeg
%{_mandir}/man1/plaympeg.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smpeg-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_aclocaldir}/*

