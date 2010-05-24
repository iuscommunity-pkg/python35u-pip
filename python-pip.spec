%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname pip

Name:           python-%{srcname}
Version:        0.7.1
Release:        4%{?dist}
Summary:        Pip installs packages.  Python packages.  An easy_install replacement

Group:          Development/Libraries
License:        MIT
URL:            http://pip.openplans.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
Requires:       python-setuptools

%description

Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

pip is meant to improve on easy_install.bulletin boards, etc.).

%prep
%setup -q -n %{srcname}-%{version}
%{__sed} -i '1d' pip/__init__.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip
%{python_sitelib}/pip*

%changelog
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1. of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Tue Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Mon Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

