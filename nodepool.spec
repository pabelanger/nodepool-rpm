%global srcname nodepool

Name:           %{srcname}
Version:        0.3.1
Release:        1%{?dist}
Summary:        Node pool management for a distributed test infrastructure

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.io/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
# test-requirements.txt
BuildRequires:  python-testscenarios
BuildRequires:  python-testrepository
# requirements.txt
BuildRequires:  python-APScheduler
BuildRequires:  python-gear
BuildRequires:  python-jenkins
BuildRequires:  python-kazoo
BuildRequires:  python-os-client-config
BuildRequires:  python-paramiko
BuildRequires:  python-paste
BuildRequires:  python-PyMySQL
BuildRequires:  python2-shade
BuildRequires:  python-sqlalchemy
BuildRequires:  python-statsd
BuildRequires:  python-voluptuous
BuildRequires:  python-zmq

Requires:  python-APScheduler
Requires:  python-gear
Requires:  python-jenkins
Requires:  python-kazoo
Requires:  python-os-client-config
Requires:  python-paramiko
Requires:  python-paste
Requires:  python-PyMySQL
Requires:  python2-shade
Requires:  python-sqlalchemy
Requires:  python-statsd
Requires:  python-voluptuous
Requires:  python-zmq

%description
Nodepool is a service used by the OpenStack CI team to deploy and manage a pool
of devstack images on a cloud server for use in OpenStack project testing.

%package doc
Summary:       Documentation of Nodepool
BuildRequires:  python-sphinxcontrib-programoutput
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx

%description doc
Documentation of Nodepool.

%prep
%autosetup -n %{srcname}-%{version}
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%py2_build

%install
%py2_install

## generate html docs
%{__python} setup.py build_sphinx
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv

# TODO(pabelanger): Work with upstream to select which tests to run.
#%check
#%{__python2} setup.py testr

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n %{srcname}
%license LICENSE
%doc README.rst
%{_bindir}/*
%{python2_sitelib}/*

%files doc
%license LICENSE
%doc doc/build/html

%pre
getent group nodepool >/dev/null || groupadd -r nodepool
getent passwd nodepool >/dev/null || \
useradd -r -g nodepool -d %{_sharedstatedir}/nodepool -s /sbin/nologin -c "Node pool management for a distributed test infrastructure" nodepool
exit 0

%changelog
* Wed Jan 04 2017 Paul Belanger <pabelanger@redhat.com> 0.0.5-1
- Initial commit
