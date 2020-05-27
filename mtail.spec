# FIXME:
%undefine _missing_build_ids_terminate_build

%global upstream_version 3.0.0-rc35
%global _version %(v=%{upstream_version}; echo ${v/-/_})

Name:       mtail
Version:    %{_version}
Release:    2%{?dist}
Summary:    Extract whitebox monitoring data from application logs for collection in a timeseries database
License:    ASL 2.0
URL:        https://github.com/google/mtail
%undefine   _disable_source_fetch
Source0:    https://github.com/google/%{name}/archive/v%{upstream_version}.tar.gz
%define     SHA256SUM0 5fc3fd12b88f37a556b0ef63e7766bc4a7da957fe3b169dd3d2153b310c37bec
Source1:    mtail.service
Source2:    mtail.sysconfig


BuildRequires: golang
BuildRequires: go-bindata
%if 0%{?el7}
# git 1.8 from el7 has a problem fetching some go dependencies
# git224 can be found in IUS repository https://ius.io/
BuildRequires: git224
%else
BuildRequires: git
%endif

%{?systemd_requires}
BuildRequires: systemd

%description
mtail is a tool for extracting metrics from application logs to be exported
into a timeseries database or timeseries calculator for alerting and
dashboarding.

It fills a monitoring niche by being the glue between applications that do not
export their own internal state (other than via logs) and existing monitoring
systems, such that system operators do not need to patch those applications to
instrument them or writing custom extraction code for every such application.

%prep
echo "%SHA256SUM0 %SOURCE0" | sha256sum -c -
%setup -n %{name}-%{upstream_version} -q

%build
make %{name}

%install
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -D -m 644 %SOURCE1 %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 644 %SOURCE2 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/%{name}

%changelog
* Wed May 27 2020 François Charlier <fcharlie@redhat.com> 3.0.0_rc35-3
- Add sysconfig configuration
- Add systemd service file

* Tue May 26 2020 François Charlier <fcharlie@redhat.com> 3.0.0_rc35-2
- Allow building on EL7

* Tue May 26 2020 François Charlier <fcharlie@redhat.com> 3.0.0_rc35-1
- Initial packaging
