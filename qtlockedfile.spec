%global commit0	   5a07df503a6f01280f493cbcc2aace462b9dee57
%global commitdate 20150629

%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global _qt5_headerdir %{_includedir}/qt5/

Summary:	QFile extension with advisory locking functions
Name:		qtlockedfile
Version:	2.4
Release:	28.%{commitdate}git%{shortcommit0}%{?dist}

License:	GPLv3 or LGPLv2 with exceptions
URL:		http://doc.qt.digia.com/solutions/4/qtlockedfile/qtlockedfile.html
Source0:	https://github.com/qtproject/qt-solutions/archive/%{commit0}.tar.gz#/%{name}-%{commit0}.tar.gz
Source1:	qtlockedfile.prf
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source2:	LICENSE.LGPL
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source3:	LGPL_EXCEPTION
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source4:	LICENSE.GPL3

BuildRequires:	qt5-qtbase-devel

%description
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

%package qt5
Summary:	QFile extension with advisory locking functions (Qt5)

%description qt5
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.
This is a special build against Qt5.

%package qt5-devel
Summary:	Development files for %{name}-qt5
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	qt5-qtbase-devel

%description qt5-devel
This package contains libraries and header files for developing applications
that use QtLockedFile with Qt5.


%prep
%setup -qn qt-solutions-%{commit0}/%{name}
# use versioned soname
sed -i s,head,%{version}, common.pri
# do not build example source
sed -i /example/d %{name}.pro
mkdir licenses
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} licenses


%build
# Does not use GNU configure
./configure -library
%{qmake_qt5}
%make_build

%install
# libraries
mkdir -p %{buildroot}%{_libdir}
cp -ap lib/* %{buildroot}%{_libdir}

# headers
mkdir -p %{buildroot}%{_qt5_headerdir}/QtSolutions
cp -ap src/qtlockedfile.h src/QtLockedFile %{buildroot}%{_qt5_headerdir}/QtSolutions
install -p -D -m644 %{SOURCE1} %{buildroot}%{_libdir}/qt5/mkspecs/features/qtlockedfile.prf

%files
%license licenses/*
%doc README.TXT

%files qt5
%license licenses/*
%doc README.TXT
# Caution! do not include any unversioned .so symlink (belongs to -devel)
%{_qt5_libdir}/libQt5Solutions_LockedFile*.so.*

%files qt5-devel
%doc doc/html/ example/
%{_qt5_headerdir}/QtSolutions/
%{_qt5_libdir}/libQt5Solutions_LockedFile*.so
%{_libdir}/qt5/mkspecs/features/qtlockedfile.prf
