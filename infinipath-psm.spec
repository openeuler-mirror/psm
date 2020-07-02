Name:           infinipath-psm
Version:        3.3
Release:        10
License:        GPLv2 or BSD
Summary:        Libraries for Intel Performance Scaled Messaging
URL:            https://github.com/01org/psm
Source0:        https://codeload.github.com/intel/psm/zip/4abbc60
ExclusiveArch:  x86_64
BuildRequires:  libuuid-devel
Obsoletes:      infinipath-libs <= %{version}-%{release}
Requires:       udev
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# Add udev rules for psm
Source1:        ipath.rules
# Fix indentation misleading
Patch0001:      misleading-indentation.patch
# Add base cflags
Patch0002:      adjust-base-cflags.patch
# Remove executable permissions for header files
Patch0003:      remove-executable-permissions-for-header-files.patch
# Add sysmacros.h for build
Patch0004:      0001-Include-sysmacros.h.patch
# Extend buffer for uvalue and pvalue
Patch0005:      0001-Extend-buffer-for-uvalue-and-pvalue.patch
# Extend fdesc array
Patch0006:      extend-fdesc-array.patch
# Fix stringop-truncation build error
Patch0007:      fix-stringop-truncation-build-error.patch

%description
PSM API is Intel's low-level user-level communications interface for the True Scale family of products.
PSM users are enabled with mechanisms necessary to implement higher level communications interfaces in
parallel environments.

%package        devel
Summary:        Files for Intel PSM development
Requires:       %{name} = %{version}-%{release}
Obsoletes:      infinipath-devel <= %{version}-%{release}
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description    devel
Development files for Intel PSM.

%prep
%autosetup -n psm-4abbc60 -p1
find libuuid -type f -not -name 'psm_uuid.[c|h]' -not -name Makefile -exec rm -f '{}' \;

%build
%{set_build_flags}
%make_build PSM_USE_SYS_UUID=1 PSM_HAVE_SCIF=0 MIC=0 CC=gcc

%install
%make_install PSM_HAVE_SCIF=0 MIC=0
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/60-ipath.rules

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

%files
%doc README COPYING
%{_sysconfdir}/udev/rules.d/60-ipath.rules
%{_libdir}/{libpsm_infinipath.so.*,libinfinipath.so.*}

%files devel
%{_libdir}/{libpsm_infinipath.so,libinfinipath.so}
%{_includedir}/{psm.h,psm_mq.h}

%changelog
* Thu Jul 02 2020 senlin <xiasenlin1@huawei.com> - 3.3-10
- Fix stringop-truncation build error

* Mon Mar 16 2020 Ling Yang <lingyang2@huawei.com> - 3.3-9
- Fixed URL

* Mon Mar 16 2020 Ling Yang <lingyang2@huawei.com> - 3.3-8
- Fixed build error

* Fri Mar 13 2020 Ling Yang <lingyang2@huawei.com> - 3.3-7
- Package Init
