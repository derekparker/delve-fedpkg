# Run tests in check section
%bcond_without check

# https://github.com/derekparker/delve
%global goipath         github.com/derekparker/delve
Version:                1.1.0

%global common_description %{expand:
Delve is a debugger for the Go programming language. The goal of the project 
is to provide a simple, full featured debugging tool for Go. Delve should be 
easy to invoke and easy to use. Chances are if you're using a debugger, things 
aren't going your way. With that in mind, Delve should stay out of your way as 
much as possible.}

%gometa

Name:           delve
Release:        1%{?dist}
Summary:        A debugger for the Go programming language
# Detected licences
# - Expat License at 'LICENSE'
License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

Patch1: ./eval-symlink-in-test.patch
Patch2: ./test-fixture-vendor-to-internal.patch

BuildRequires: golang(github.com/cosiner/argv)
BuildRequires: golang(github.com/mattn/go-isatty)
BuildRequires: golang(github.com/peterh/liner)
BuildRequires: golang(github.com/pkg/profile)
BuildRequires: golang(github.com/sirupsen/logrus)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(golang.org/x/arch/x86/x86asm)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(golang.org/x/sys/windows)
BuildRequires: golang(gopkg.in/yaml.v2)

%description
%{common_description}


%package -n %{goname}-devel
Summary:       %{summary}
BuildArch:     noarch

%description -n %{goname}-devel
%{common_description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.


%prep
%forgesetup

%patch1 -p1
%patch2 -p1

rm -rf vendor/


%build
%gobuildroot
%gobuild -o _bin/dlv %{goipath}/cmd/dlv


%install
%goinstall
install -Dpm 0755 _bin/dlv %{buildroot}%{_bindir}/dlv


%if %{with check}
%check
%gochecks
%endif


%files
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md
%doc Documentation/*
%{_bindir}/dlv


%files -n %{goname}-devel -f devel.file-list
%license LICENSE


%changelog
* Fri Nov 2 2018 Derek Parker <deparker@redhat.com> - 1.1.0-1
- First package for Fedora
