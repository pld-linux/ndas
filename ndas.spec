#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

Summary:	Linux NDAS driver
Summary(pl.UTF-8):	Linuksowy sterownik NDAS
Name:		ndas
Version:	1.1
%define         subver 24
Release:	1
License:	Custom License (see EULA.txt)
Group:		Base/Kernel
Source0:	http://code.ximeta.com/dev/current/linux/%{name}-%{version}-%{subver}.tar.gz
# Source0-md5:	ccedb4db57f302674ebe93bf148d7188
Patch0:		%{name}-Makefile.patch
URL:		http://www.ximeta.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux NDAS driver.

%description -l pl.UTF-8
Linuksowy sterownik NDAS.

# kernel subpackages.

%package -n kernel%{_alt_kernel}-block-ndas
Summary:	Linux driver for NDAS
Summary(pl.UTF-8):	Sterownik dla Linuksa do NDAS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%requires_releq_kernel
Requires(postun):	%releq_kernel

%description -n kernel%{_alt_kernel}-block-ndas
This is driver for NDAS for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-block-ndas -l pl.UTF-8
Sterownik dla Linuksa do NDAS.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n %{name}-%{version}-%{subver}
%patch0 -p1

%build
%if %{with userspace}
%{__make} ndas-admin \
	ndas-um-cc="%{__cc}" \
	ndas-addon-extra-cflags="%{rpmcflags}" \
	ndas-app-ldflags="%{rpmldflags}"
%endif

%if %{with kernel}
%build_kernel_modules -m ndas_sal,ndas_core,ndas_block,ndas_emu
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sbindir}
install ndasadmin $RPM_BUILD_ROOT%{_sbindir}/ndasadmin
%endif

%if %{with kernel}
%install_kernel_modules -m ndas_sal,ndas_core,ndas_block,ndas_emu -d kernel/drivers/block
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-block-ndas
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-block-ndas
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%doc EULA.txt README
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndasadmin
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-block-ndas
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/block/*.ko*
%endif
