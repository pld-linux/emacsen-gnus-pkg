%bcond_without	xemacs	# Build without XEmacs support
%bcond_without	emacs	# Build without GNU Emacs support
%bcond_without	pdf_doc	# Don't build PDF documentation
%define		_the_name gnus
Summary:	An Emacs/XEmacs newsreader and mail client
Summary(pl):	Czytnik grup dyskusyjnych i klient poczty dla Emacsa/XEmacsa
Name:		emacsen-gnus-pkg
Version:	5.10.6
Release:	3
License:	GPL
Group:		Applications/Networking
Source0:	http://www.gnus.org/dist/%{_the_name}-%{version}.tar.gz
# Source0-md5:	8b510e5d2530f92af371eb64f828b257
Patch0:		%{name}-destdir.patch
URL:		http://www.gnus.org/
%if %{with pdf_doc}
BuildRequires:	texinfo-texi2dvi
BuildRequires:	tetex-latex
BuildRequires:	tetex-makeindex
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-pdftex
%endif
%if %{with emacs}
BuildRequires:	emacs
%endif
%if %{with xemacs}
BuildRequires:	xemacs
BuildRequires:	xemacs-mail-lib-pkg
BuildRequires:	xemacs-eterm-pkg
BuildRequires:	xemacs-sh-script-pkg
BuildRequires:	xemacs-os-utils-pkg
BuildRequires:	xemacs-dired-pkg
BuildRequires:	xemacs-mh-e-pkg
BuildRequires:	xemacs-mailcrypt-pkg
BuildRequires:	xemacs-fsf-compat-pkg
BuildRequires:	xemacs-texinfo-pkg
%endif
Requires:	gnus-elisp-code = %{version}-%{release}
Requires:	starttls
Conflicts:	xemacs-gnus-pkg
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
You can read news (and mail) from within GNU Emacs or XEmacs by using
Gnus. The news can be gotten by any nefarious means you can think of
-- NNTP, local spool or your mbox file.

This package contains files common to both GNU Emacs and XEmacs.

%description -l pl
Dziêki pakietowi Gnus mo¿esz czytaæ newsy i pocztê z u¿yciem GNU
Emacsa lub XEmacsa. Gnus mo¿e pobieraæ listy z najró¿niejszych ¼róde³,
w tym z serwera NNTP, lokalnego spoola jak i plików mbox.

Ten pakiet zawiera pliki Gnusa wspólne dla GNU Emacsa i XEmacsa.

%define version_of() %{expand:%%(rpm -q %1 --queryformat '%%%%{version}-%%%%{release}')}

%if %{with emacs}
%package emacs
Summary:	Gnus elisp files for GNU Emacs
Summary(pl):	Kod elisp Gnusa dla GNU Emacsa
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	emacs = %{version_of emacs}
Provides:	gnus-elisp-code = %{version}-%{release}

%description emacs
This package contains compiled elisp files needed to run Gnus on GNU Emacs

%description emacs -l pl
Pakiet zawiera skompilowane pliki elisp z kodem Gnusa dla GNU Emacsa.

%package emacs-el
Summary:	Gnus elisp source files for GNU Emacs
Summary(pl):	Kod ¼ród³owy elisp Gnusa dla GNU Emacsa
Group:		Applications/Networking
Requires:	%{name}-emacs = %{version}-%{release}

%description emacs-el
This package contains source elisp files needed to run Gnus on GNU Emacs

%description emacs-el -l pl
Pakiet zawiera ¼ród³owe pliki elisp z kodem Gnusa dla GNU Emacsa.
%endif


%if %{with xemacs}
%package xemacs
Summary:	Gnus elisp files for XEmacs
Summary(pl):	Kod elisp Gnusa dla XEmacsa
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	xemacs = %{version_of xemacs}
Requires:	xemacs-mail-lib-pkg
Requires:	xemacs-eterm-pkg
Requires:	xemacs-sh-script-pkg
Requires:	xemacs-os-utils-pkg
Requires:	xemacs-dired-pkg
Requires:	xemacs-mh-e-pkg
Requires:	xemacs-mailcrypt-pkg
Requires:	xemacs-fsf-compat-pkg
Provides:	gnus-elisp-code = %{version}-%{release}

%description xemacs
This package contains compiled elisp files needed to run Gnus on XEmacs

%description xemacs -l pl
Pakiet zawiera skompilowane pliki elisp z kodem Gnusa dla XEmacsa.

%package xemacs-el
Summary:	Gnus elisp source files for XEmacs
Summary(pl):	Kod ¼ród³owy elisp Gnusa dla XEmacsa
Group:		Applications/Networking
Requires:	%{name}-xemacs = %{version}-%{release}

%description xemacs-el
This package contains source elisp files needed to run Gnus on XEmacs

%description xemacs-el -l pl
Pakiet zawiera pliki ¼ród³owe elisp z kodem Gnusa dla XEmacsa.
%endif


%if %{with pdf_doc}
%package pdf-doc
Summary:	PDF documentation for Gnus
Summary(pl):	Dokumentacja Gnusa w formacie PDF
Group:		Documentation

%description pdf-doc
Documentation for Gnus in PDF format

%description pdf-doc -l pl
Dokumentacja Gnusa w formacie PDF
%endif


%prep
%setup -q -n %{_the_name}-%{version}
%patch0 -p1


%build
mkdir DUMMY

%if %{with xemacs}

%configure \
	--with-xemacs \
	--with-lispdir=%{_datadir}/xemacs-packages/lisp/%{_the_name} \
	--with-etcdir=%{_datadir}/%{_the_name}
%{__make}

%if !%{with emacs} && %{with pdf_doc}
%{__make} -C texi pdf
%endif

%{__make} DESTDIR=`pwd`/DUMMY install
%{__make} distclean

%endif

%if %{with emacs}

%configure \
	--with-emacs \
	--with-lispdir=%{_emacs_lispdir}/%{_the_name} \
	--with-etcdir=%{_datadir}/%{_the_name}
%{__make}

%if %{with pdf_doc}
%{__make} -C texi pdf
%endif

%{__make} DESTDIR=`pwd`/DUMMY install

%endif

%install
rm -rf $RPM_BUILD_ROOT
cp -R ./DUMMY $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/xemacs-packages/etc
ln -s ../../gnus $RPM_BUILD_ROOT%{_datadir}/xemacs-packages/etc/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog GNUS-NEWS README todo contrib/
%{_datadir}/%{_the_name}
%{_infodir}/*

%if %{with emacs}
%files emacs
%defattr(644,root,root,755)
%dir %{_emacs_lispdir}/%{_the_name}
%{_emacs_lispdir}/%{_the_name}/*.elc

%files emacs-el
%defattr(644,root,root,755)
%{_emacs_lispdir}/%{_the_name}/*.el
%endif

%if %{with xemacs}
%files xemacs
%defattr(644,root,root,755)
%dir %{_datadir}/xemacs-packages/lisp/%{_the_name}
%{_datadir}/xemacs-packages/lisp/%{_the_name}/*.elc
%{_datadir}/xemacs-packages/etc/%{_the_name}

%files xemacs-el
%defattr(644,root,root,755)
%{_datadir}/xemacs-packages/lisp/%{_the_name}/*.el
%endif

%if %{with pdf_doc}
%files pdf-doc
%defattr(644,root,root,755)
%doc texi/*.pdf
%endif
