%global with_tests 0

%global srcname pip

%global bashcompdir %(b=$(pkg-config --variable=completionsdir bash-completion 2>/dev/null); echo ${b:-%{_sysconfdir}/bash_completion.d})
%if "%{bashcompdir}" != "%{_sysconfdir}/bash_completion.d"
%global bashcomp2 1
%endif

%global ius_suffix 35u

Name:           python%{ius_suffix}-%{srcname}
Version:        8.1.1
Release:        1.ius%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            https://pip.pypa.io
Source0:        https://pypi.io/packages/source/p/pip/%{srcname}-%{version}.tar.gz

# to get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout %%{version} && tar -czvf pip-%%{version}-tests.tar.gz tests/
%if 0%{?with_tests}
Source1:        pip-%{version}-tests.tar.gz
%endif

BuildArch:      noarch
BuildRequires:  bash-completion
BuildRequires:  python%{ius_suffix}-devel
BuildRequires:  python%{ius_suffix}-setuptools
%if 0%{?with_tests}
BuildRequires:  python%{ius_suffix}-mock
BuildRequires:  python%{ius_suffix}-pytest
BuildRequires:  python%{ius_suffix}-pretend
BuildRequires:  python%{ius_suffix}-freezegun
BuildRequires:  python%{ius_suffix}-scripttest
BuildRequires:  python%{ius_suffix}-virtualenv
%endif
Requires:       python%{ius_suffix}-setuptools


%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?with_tests}
tar -xf %{SOURCE1}
%endif

find %{srcname} -type f -name \*.py -print0 | xargs -0 sed -i -e '1 {/^#!\//d}'


%build
%{__python35u} setup.py build


%install
%{__python35u} setup.py install -O1 --skip-build --root %{buildroot}

rm -f %{buildroot}%{_bindir}/pip
rm -f %{buildroot}%{_bindir}/pip3

mkdir -p %{buildroot}%{bashcompdir}
PYTHONPATH=%{buildroot}%{python35u_sitelib} \
    %{buildroot}%{_bindir}/pip%{python35u_version} completion --bash \
    > %{buildroot}%{bashcompdir}/pip%{python35u_version}
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 pip%{python35u_version}/" \
    %{buildroot}%{bashcompdir}/pip%{python35u_version}


%if 0%{?with_tests}
%check
py.test-%{python35u_version} -m 'not network'
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc README.rst docs
%attr(755,root,root) %{_bindir}/pip%{python35u_version}
%{python35u_sitelib}/pip*
%{bashcompdir}
%if 0%{?bashcomp2}
%dir %(dirname %{bashcompdir})
%endif


%changelog
* Tue May 03 2016 Ben Harper <ben.harper@rackspace.com> - 8.1.1-1.ius
- Upstream 8.1.1
- update Source0 url to pypi.io see
  https://bitbucket.org/pypa/pypi/issues/438/backwards-compatible-un-hashed-package

* Thu Mar 17 2016 Carl George <carl.george@rackspace.com> - 8.1.0-1.ius
- Latest upstream
- Strip all shebangs

* Fri Mar 04 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.3-1.ius
- Latest upstream
- remove with_rewheel macro

* Thu Feb 11 2016 Carl George <carl.george@rackspace.com> - 8.0.2-3.ius
- Fix patch0, re-enable

* Thu Feb 11 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.2-2.ius
- disable patch0

* Fri Jan 22 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.2-1.ius
- Latest upstream

* Thu Jan 21 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.1-1.ius
- Latest upstream
- Refresh patch0

* Fri Nov 20 2015 Carl George <carl.george@rackspace.com> - 7.1.2-1.ius
- Initial import from Fedora
- Remove subpackage structure and related things
- Use python35u names and macros
- Remove pip and pip3 to allow parallel installs
- Latest upstream

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-3
- Rebuilt for Python3.5 rebuild
- With wheel set to 1

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-2
- Rebuilt for Python3.5 rebuild

* Wed Jul 01 2015 Slavek Kabrda <bkabrda@redhat.com> - 7.1.0-1
- Update to 7.1.0

* Tue Jun 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 7.0.3-3
- Install bash completion
- Ship LICENSE.txt as %%license where available

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 7.0.3-1
- Update to 7.0.3

* Fri Mar 06 2015 Matej Stuchlik <mstuchli@redhat.com> - 6.0.8-1
- Update to 6.0.8

* Thu Dec 18 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Only enable tests on Fedora.

* Mon Dec 01 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Add tests
- Add patch skipping tests requiring Internet access

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

