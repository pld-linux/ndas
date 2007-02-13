#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	0.1
Summary:	Linux NDAS driver
Summary(pl.UTF-8):	Linuksowy sterownik NDAS
Name:		ndas
Version:	1.0.3
%define         _subver 101
Release:	%{_rel}
License:	GPL/BSD/other (!!)
Group:		Base/Kernel
Source0:	http://code.ximeta.com/download/%{version}/%{_subver}/linux/%{name}-%{version}-%{_subver}.tar.gz
# Source0-md5:	2e25c00fbc65af5f14d4e44d85f282f6
Patch0:		%{name}-Makefile.patch
URL:		http://www.ximeta.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
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
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-block-ndas
This is driver for NDAS for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-block-ndas -l pl.UTF-8
Sterownik dla Linuksa do NDAS.

Ten pakiet zawiera moduł jądra Linuksa.

%package -n kernel%{_alt_kernel}-smp-block-ndas
Summary:	Linux SMP driver for NDAS
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do NDAS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-block-ndas
This is driver for NDAS for Linux.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-block-ndas -l pl.UTF-8
Sterownik dla Linuksa do NDAS.

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -n %{name}-%{version}-%{_subver}
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

%post	-n kernel%{_alt_kernel}-smp-block-ndas
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-block-ndas
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndasadmin
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-block-ndas
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/block/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-block-ndas
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/block/*.ko*
%endif
%endif
