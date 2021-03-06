#
# spec file for package ceph-deploy
#

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#################################################################################
# common
#################################################################################
Name:           ceph-deploy
Version:        1.5.32
Release:        1%{?dist}
Summary:        Admin and deploy tool for Ceph
License:        MIT
Group:          System/Filesystems
URL:            http://ceph.com/
# fcami - TODO => fix source URL (github? pypi.python.org?)
#         NB: upstream's 1.5.31.tar.bz2 tarball is identical to github's, except
#             for minor egg_info metadata.
Source0:        https://pypi.io/packages/source/c/%{name}/%{name}-%{version}.tar.gz
# fcami - this patch disables using upstream's repositories by default
Patch0:         ceph-deploy_do-not-use-upstream-repos.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-mock
%if 0%{?suse_version}
BuildRequires:  python-pytest
%else
BuildRequires:  pytest
%endif
BuildRequires:  git
#Requires:      lsb-release
#Requires:      ceph
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%else
BuildArch:      noarch
%endif

#################################################################################
# specific
#################################################################################
%if 0%{defined suse_version}
%py_requires
%endif

%description
An easy to use admin tool for deploy ceph storage clusters.

%prep
#%%setup -q -n %%{name}
%setup -q
%patch0 -p1 -b .disable-repos

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -m 0755 -D scripts/ceph-deploy $RPM_BUILD_ROOT/usr/bin

%check
python setup.py test

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%{_bindir}/ceph-deploy
%{python_sitelib}/*

%changelog
* Tue Jul 19 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.5.32-1
- Upstream 1.5.32
- Drop useless requirements on python-distribute, python-virtualenv and tox
- Run unit tests

* Fri Jan 22 2016 François Cami <fcami@redhat.com> - 1.5.31-1
- initial CentOS release
- use upstream (ceph.com) ceph-deploy.spec, add dist tag
- disable using upstream repositories by default

